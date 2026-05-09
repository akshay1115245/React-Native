# iOS Technical Depth Guide for Engineering Managers

> This document provides deep-dive technical content that an EM - iOS must know or be able to discuss confidently in interviews and with their team.

---

## Swift Concurrency: Complete Mental Model

### The Problem Swift Concurrency Solves

Before Swift 5.5, async code used:
1. Completion handlers → callback hell, error prone
2. Delegate pattern → scattered code
3. Combine → steep learning curve, FRP paradigm

```swift
// OLD: Completion handler pyramid of doom
func loadUser(id: String, completion: @escaping (Result<User, Error>) -> Void) {
    fetchUser(id: id) { result in
        switch result {
        case .success(let user):
            fetchAvatar(url: user.avatarURL) { avatarResult in
                switch avatarResult {
                case .success(let image):
                    fetchPosts(userId: user.id) { postsResult in
                        // Deeply nested, hard to read/maintain
                    }
                case .failure(let error):
                    completion(.failure(error))
                }
            }
        case .failure(let error):
            completion(.failure(error))
        }
    }
}

// NEW: Swift Concurrency - reads like synchronous code
func loadUser(id: String) async throws -> (User, UIImage, [Post]) {
    let user = try await fetchUser(id: id)
    async let avatar = fetchAvatar(url: user.avatarURL)
    async let posts = fetchPosts(userId: user.id)
    return try await (user, avatar, posts) // parallel execution
}
```

### Task Hierarchy & Structured Concurrency

```
Task (root)
├── child Task 1
│   ├── grandchild Task A
│   └── grandchild Task B
└── child Task 2
```

**Cancellation propagates down**: if parent is cancelled, all children are cancelled automatically.

**Error propagation goes up**: if a child throws, the parent's scope handles it.

### Actor Isolation - The Real Model

```swift
// WITHOUT actor - data race possible
class UnsafeCounter {
    var count = 0
    func increment() { count += 1 } // NOT thread-safe
}

// WITH actor - compiler-enforced isolation
actor SafeCounter {
    var count = 0
    func increment() { count += 1 } // Safe - only one caller at a time
    func getCount() -> Int { return count }
}

// Calling from outside requires await
let counter = SafeCounter()
await counter.increment()
let value = await counter.getCount()
```

### MainActor — The UI Thread Contract

```swift
// Marking an entire class as @MainActor
@MainActor
class ViewModel: ObservableObject {
    @Published var items: [Item] = []
    
    // All methods run on main thread
    func updateUI(with items: [Item]) {
        self.items = items // Safe - we're on MainActor
    }
    
    // Use nonisolated for non-UI work
    nonisolated func computeHeavyWork() async -> [Item] {
        // Runs on a background thread
        return await Task.detached(priority: .background) {
            // heavy computation
            return []
        }.value
    }
}
```

---

## UIKit vs SwiftUI: When to Use Each

### Decision Matrix

| Scenario | UIKit | SwiftUI | Notes |
|---|---|---|---|
| Legacy codebase | ✅ | ⚠️ | Interop available but complex |
| iOS 13+ minimum deployment | ⚠️ | ✅ | SwiftUI stable from iOS 14/15 |
| Complex custom animations | ✅ | ⚠️ | UIKit more control |
| Simple declarative UI | ⚠️ | ✅ | SwiftUI shines here |
| Collection with complex layout | ✅ | ⚠️ | UICollectionView more flexible |
| Forms and settings UI | ⚠️ | ✅ | SwiftUI Form is excellent |
| Accessibility | Both | Both | Both support well |
| Watchdog/Memory sensitivity | Both | Both | SwiftUI can be heavier |

### Interoperability Pattern

```swift
// Using a UIKit view inside SwiftUI
struct MapView: UIViewRepresentable {
    @Binding var region: MKCoordinateRegion
    
    func makeUIView(context: Context) -> MKMapView {
        let mapView = MKMapView()
        mapView.delegate = context.coordinator
        return mapView
    }
    
    func updateUIView(_ uiView: MKMapView, context: Context) {
        uiView.setRegion(region, animated: true)
    }
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, MKMapViewDelegate {
        var parent: MapView
        init(_ parent: MapView) { self.parent = parent }
    }
}

// Using a SwiftUI view inside UIKit
class HostingViewController: UIViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        let swiftUIView = MySwiftUIView()
        let hostingController = UIHostingController(rootView: swiftUIView)
        addChild(hostingController)
        view.addSubview(hostingController.view)
        hostingController.didMove(toParent: self)
        // Set up constraints...
    }
}
```

---

## Core Data: Production Patterns

### Proper Stack Setup

```swift
class CoreDataStack {
    static let shared = CoreDataStack()
    
    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "MyModel")
        
        // WAL mode for better concurrency
        let description = container.persistentStoreDescriptions.first!
        description.shouldAddStoreAsynchronously = true
        description.setOption(true as NSNumber, 
                              forKey: NSPersistentHistoryTrackingKey)
        
        container.loadPersistentStores { _, error in
            if let error = error {
                fatalError("Core Data failed: \(error)")
            }
        }
        container.viewContext.automaticallyMergesChangesFromParent = true
        return container
    }()
    
    // Background context for writes
    func newBackgroundContext() -> NSManagedObjectContext {
        let context = persistentContainer.newBackgroundContext()
        context.mergePolicy = NSMergeByPropertyObjectTrumpMergePolicy
        return context
    }
    
    // Perform writes in background
    func performBackgroundTask(_ block: @escaping (NSManagedObjectContext) -> Void) {
        persistentContainer.performBackgroundTask(block)
    }
}
```

### Fetch with Predicate — Performance Patterns

```swift
// Fetch request with index-optimized predicate
func fetchRecentOrders(for userId: String, limit: Int = 50) -> [Order] {
    let request = Order.fetchRequest()
    
    // Use indexed attributes in predicates
    request.predicate = NSPredicate(format: "userId == %@ AND status != %@", 
                                    userId, "cancelled")
    request.sortDescriptors = [NSSortDescriptor(key: "createdAt", ascending: false)]
    request.fetchLimit = limit
    
    // Only fetch what you need
    request.propertiesToFetch = ["orderId", "total", "createdAt", "status"]
    request.resultType = .dictionaryResultType
    
    do {
        return try viewContext.fetch(request)
    } catch {
        logger.error("Fetch failed: \(error)")
        return []
    }
}
```

---

## Networking Layer Architecture

### Production-Grade Network Layer

```swift
// Protocol for testability
protocol NetworkClient {
    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T
}

// Endpoint definition
struct Endpoint {
    let path: String
    let method: HTTPMethod
    let headers: [String: String]
    let body: Encodable?
    let queryItems: [URLQueryItem]?
}

// Real implementation
final class URLSessionNetworkClient: NetworkClient {
    private let session: URLSession
    private let baseURL: URL
    private let tokenProvider: TokenProvider
    
    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        var request = try buildRequest(from: endpoint)
        request.addValue("Bearer \(try await tokenProvider.token())", 
                         forHTTPHeaderField: "Authorization")
        
        let (data, response) = try await session.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }
        
        switch httpResponse.statusCode {
        case 200...299:
            return try JSONDecoder().decode(T.self, from: data)
        case 401:
            throw NetworkError.unauthorized
        case 429:
            throw NetworkError.rateLimited
        default:
            throw NetworkError.serverError(httpResponse.statusCode)
        }
    }
}

// Retry with exponential backoff
extension NetworkClient {
    func requestWithRetry<T: Decodable>(
        _ endpoint: Endpoint,
        maxAttempts: Int = 3
    ) async throws -> T {
        var lastError: Error?
        for attempt in 0..<maxAttempts {
            do {
                return try await request(endpoint)
            } catch NetworkError.serverError(let code) where code >= 500 {
                lastError = NetworkError.serverError(code)
                let delay = Double(pow(2.0, Double(attempt))) // 1s, 2s, 4s
                try await Task.sleep(nanoseconds: UInt64(delay * 1_000_000_000))
            } catch {
                throw error // Don't retry client errors
            }
        }
        throw lastError!
    }
}
```

---

## Testing Strategy for iOS Teams

### Testing Pyramid for iOS

```
        /\
       /  \
      / E2E\       ← XCUITest (few, high value)
     /------\
    /  Integ  \    ← Integration tests (some)
   /------------\
  /  Unit Tests  \ ← Fast, many, no dependencies
 /----------------\
```

### Unit Testing with Mocks

```swift
// Protocol for testability
protocol UserRepository {
    func fetchUser(id: String) async throws -> User
    func saveUser(_ user: User) async throws
}

// Production implementation
final class RemoteUserRepository: UserRepository {
    private let client: NetworkClient
    
    func fetchUser(id: String) async throws -> User {
        try await client.request(.getUser(id: id))
    }
    
    func saveUser(_ user: User) async throws {
        try await client.request(.updateUser(user))
    }
}

// Mock for tests
final class MockUserRepository: UserRepository {
    var fetchedUsers: [String: User] = [:]
    var savedUsers: [User] = []
    var shouldThrowError: Error?
    
    func fetchUser(id: String) async throws -> User {
        if let error = shouldThrowError { throw error }
        return fetchedUsers[id] ?? User.mock()
    }
    
    func saveUser(_ user: User) async throws {
        if let error = shouldThrowError { throw error }
        savedUsers.append(user)
    }
}

// Test
final class ProfileViewModelTests: XCTestCase {
    var sut: ProfileViewModel!
    var repository: MockUserRepository!
    
    override func setUp() {
        repository = MockUserRepository()
        sut = ProfileViewModel(repository: repository)
    }
    
    func testLoadProfile_success_updatesState() async throws {
        // Arrange
        let expectedUser = User(id: "123", name: "Alice", email: "alice@example.com")
        repository.fetchedUsers["123"] = expectedUser
        
        // Act
        await sut.loadProfile(id: "123")
        
        // Assert
        XCTAssertEqual(sut.user, expectedUser)
        XCTAssertFalse(sut.isLoading)
        XCTAssertNil(sut.error)
    }
    
    func testLoadProfile_failure_setsError() async throws {
        // Arrange
        repository.shouldThrowError = NetworkError.unauthorized
        
        // Act
        await sut.loadProfile(id: "123")
        
        // Assert
        XCTAssertNil(sut.user)
        XCTAssertFalse(sut.isLoading)
        XCTAssertNotNil(sut.error)
    }
}
```

---

## Performance Profiling Workflow

### Step-by-Step: Debug a Slow Scroll

1. **Reproduce on device** (not simulator — GPU/CPU behavior differs)
2. **Open Instruments** → Core Animation template
3. **Look for**: frames below 60fps (16.67ms), red bars in Frame Rate track
4. **Common culprits**:
   - Offscreen rendering (blending, shadows, rounded corners with `masksToBounds`)
   - Fat `cellForRowAt` — heavy work on main thread
   - Unoptimized images — wrong size/format
   - Auto Layout constraint solving overhead

5. **Fix: Offscreen rendering**

```swift
// BEFORE: Causes offscreen rendering
cell.avatarView.layer.cornerRadius = 25
cell.avatarView.layer.masksToBounds = true  // offscreen render trigger
cell.avatarView.layer.shadowOffset = CGSize(width: 2, height: 2)
cell.avatarView.layer.shadowOpacity = 0.3

// AFTER: Use CALayer shadow path (no offscreen render) + pre-clipped image
cell.avatarView.layer.cornerRadius = 25
cell.avatarView.layer.masksToBounds = true
// Move shadow to a container view WITHOUT masksToBounds
cell.shadowContainer.layer.shadowPath = UIBezierPath(roundedRect: ...).cgPath
cell.shadowContainer.layer.shadowOpacity = 0.3
```

6. **Fix: Heavy cellForRowAt**

```swift
// BEFORE
func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
    let cell = ...
    // Heavy work on main thread
    let processedImage = ImageProcessor.applyFilter(to: rawImage) // BAD
    let attributedString = buildAttributedString(from: longText)  // BAD
    return cell
}

// AFTER: Pre-compute and cache
func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
    let cell = ...
    let viewModel = viewModels[indexPath.row] // pre-computed
    cell.configure(with: viewModel)           // just assign, no computation
    return cell
}
```

---

## Modular iOS Architecture at Scale

### Module Types

```
App Target
├── Feature Modules (vertical slices)
│   ├── FeatureHome
│   ├── FeatureProfile
│   ├── FeatureCheckout
│   └── FeatureSearch
├── Core Modules (shared infrastructure)
│   ├── Networking
│   ├── Analytics
│   ├── Authentication
│   └── CoreData
└── UI Module
    ├── DesignSystem (colors, fonts, tokens)
    └── SharedComponents (buttons, cards, etc.)
```

### Why Modularize?

1. **Build time**: only recompile changed modules
2. **Team ownership**: teams own specific modules
3. **Testability**: modules are independently testable
4. **Reusability**: share across app and extensions (widget, watchOS)
5. **Enforces boundaries**: prevents unauthorized dependencies

### Dependency Direction Rules

```
Feature → Core, UI      ✅
Core → Core             ✅ (if no cycles)
Feature → Feature       ❌ (use shared abstractions)
Core → Feature          ❌ (inner layer cannot know outer)
UI → Feature            ❌
```

---

## Common iOS EM Technical Interview: What They Really Test

### When They Ask Technical Questions

Companies aren't testing if you can still write production code daily. They are testing:

1. **Credibility**: Can you earn engineers' respect?
2. **Judgment**: Can you make the right technical call?
3. **Communication**: Can you explain complex things simply?
4. **Growth**: Are you current with the platform?
5. **Trade-offs**: Do you understand cost vs. benefit?

### How to Answer Technical Architecture Questions

**Structure:**
1. Restate the problem and clarify constraints
2. Identify key requirements (scale, latency, offline, etc.)
3. Propose a high-level approach
4. Deep-dive into the interesting/hard parts
5. Discuss alternatives and trade-offs
6. Mention what you'd monitor/measure

**Example: "How would you architect offline support for a mobile banking app?"**

> "Great question. Let me clarify scope first — are we talking read-only offline (view last synced balance) or read-write offline (initiate transactions offline)?
>
> For read-write offline in a banking context, I'd treat the local database as the source of truth. I'd use Core Data with CloudKit or a custom sync engine. For outgoing mutations — like payment initiation — I'd queue them in a local `PendingOperations` table with idempotency keys. When connectivity restores, the sync engine replays them.
>
> Conflict resolution in banking is tricky. I'd use an optimistic UI with server-side validation as the authority. Failed conflicts surface as non-dismissible error banners.
>
> I'd instrument this with `NWPathMonitor` for network state and `os_signpost` for sync performance. I'd track sync success rate, queue depth, and conflict frequency as operational metrics."
