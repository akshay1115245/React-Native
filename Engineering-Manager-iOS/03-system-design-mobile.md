# Mobile System Design for iOS Engineering Managers

> A complete guide to answering mobile system design interview questions and leading system design discussions as an EM.

---

## The Mobile System Design Interview Framework

Unlike backend system design (which focuses on servers, databases, and distributed systems), mobile system design focuses on the **client application**. Interviewers want to see how you think about the user experience, client-side architecture, offline behavior, and performance.

### Framework: RADIO

Use this acronym to structure your answer:

| Letter | Step | Focus |
|---|---|---|
| **R** | Requirements | Functional + non-functional |
| **A** | Architecture | High-level components |
| **D** | Data model | Local + remote data structures |
| **I** | Interface | API design, data contracts |
| **O** | Optimization | Performance, caching, offline |

---

## System Design 1: News Feed App (Instagram-like)

### Requirements Clarification

**Functional:**
- Users can scroll through a feed of posts (images + text)
- Users can like and comment on posts
- Feed updates in near-real-time when online
- Read-only offline support (view last synced feed)

**Non-Functional:**
- Smooth scrolling at 60fps
- Fast initial load (< 2 seconds)
- Works on slow 3G networks
- Supports iOS 15+

---

### High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│                  iOS App                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────┐  │
│  │  SwiftUI │  │ViewModel │  │   Repository     │  │
│  │  FeedView│◄─┤ FeedVM   │◄─┤   FeedRepo       │  │
│  └──────────┘  └──────────┘  └────────┬─────────┘  │
│                                        │            │
│                               ┌────────▼──────────┐  │
│                               │   Local Cache      │  │
│                               │  (Core Data/       │  │
│                               │   SQLite)          │  │
│                               └────────┬──────────┘  │
└────────────────────────────────────────┼────────────┘
                                         │
                                  Network Layer
                                         │
                                ┌────────▼─────────┐
                                │   Backend API     │
                                │  (REST/GraphQL)   │
                                └──────────────────┘
```

---

### Data Model

**Local (Core Data entities):**

```swift
// Post entity
@objc(Post)
class Post: NSManagedObject {
    @NSManaged var postId: String
    @NSManaged var authorId: String
    @NSManaged var authorName: String
    @NSManaged var imageURL: String
    @NSManaged var caption: String
    @NSManaged var likeCount: Int32
    @NSManaged var commentCount: Int32
    @NSManaged var createdAt: Date
    @NSManaged var isLikedByCurrentUser: Bool
    @NSManaged var fetchedAt: Date  // for cache invalidation
}

// Image cache metadata
@objc(CachedImage)
class CachedImage: NSManagedObject {
    @NSManaged var url: String
    @NSManaged var localPath: String
    @NSManaged var cachedAt: Date
    @NSManaged var fileSize: Int64
}
```

**Remote (API response model):**

```swift
struct PostResponse: Decodable {
    let postId: String
    let author: AuthorResponse
    let media: MediaResponse
    let engagement: EngagementResponse
    let createdAt: Date
    
    struct AuthorResponse: Decodable {
        let userId: String
        let displayName: String
        let avatarURL: URL
    }
    
    struct MediaResponse: Decodable {
        let imageURL: URL
        let width: Int
        let height: Int
        let blurHash: String  // Low-res placeholder
    }
    
    struct EngagementResponse: Decodable {
        let likeCount: Int
        let commentCount: Int
        let isLikedByCurrentUser: Bool
    }
}
```

---

### API Design

**Feed Pagination (Cursor-based, not offset):**

```
GET /v1/feed?cursor=<cursor_token>&limit=20

Response:
{
  "posts": [...],
  "nextCursor": "eyJpZCI6IjEyMzQ1NiIsInRzIjoiMjAyNC0...",
  "hasMore": true
}
```

**Why cursor over offset?**
- Offset is unstable: if new posts inserted, pages shift
- Cursor is stable: consistent pagination even with live insertions
- Better for infinite scroll pattern

**Optimistic Like:**
```
POST /v1/posts/{postId}/likes
Body: { "userId": "current_user_id" }

// iOS sends immediately, updates local state optimistically
// Rollback UI if request fails
```

---

### Feed Loading Strategy

```swift
class FeedViewModel: ObservableObject {
    @Published var posts: [PostViewModel] = []
    @Published var isLoadingInitial = false
    @Published var isLoadingMore = false
    
    private var nextCursor: String?
    private let repository: FeedRepository
    
    func loadInitialFeed() async {
        isLoadingInitial = true
        defer { isLoadingInitial = false }
        
        // 1. Show cached posts immediately (offline-first)
        let cached = await repository.fetchCachedPosts(limit: 20)
        posts = cached.map(PostViewModel.init)
        
        // 2. Fetch fresh from network in background
        do {
            let fresh = try await repository.fetchFeedFromNetwork(cursor: nil)
            posts = fresh.posts.map(PostViewModel.init)
            nextCursor = fresh.nextCursor
            
            // 3. Update cache
            await repository.cachePosts(fresh.posts)
        } catch {
            // Network failed — cached posts remain visible
            // Show subtle "offline" indicator
        }
    }
    
    func loadMoreIfNeeded(currentPost: PostViewModel) async {
        guard currentPost.id == posts.suffix(5).first?.id,
              !isLoadingMore,
              let cursor = nextCursor else { return }
        
        isLoadingMore = true
        defer { isLoadingMore = false }
        
        let more = try? await repository.fetchFeedFromNetwork(cursor: cursor)
        if let more {
            posts.append(contentsOf: more.posts.map(PostViewModel.init))
            nextCursor = more.nextCursor
        }
    }
}
```

---

### Image Loading & Caching

```swift
// Three-tier caching: Memory → Disk → Network
class ImageCache {
    private let memoryCache = NSCache<NSString, UIImage>()
    private let diskCache = DiskImageCache()
    
    func load(url: URL) async throws -> UIImage {
        let key = url.absoluteString as NSString
        
        // 1. Memory cache — instant
        if let cached = memoryCache.object(forKey: key) {
            return cached
        }
        
        // 2. Disk cache — fast
        if let diskCached = await diskCache.image(for: url) {
            memoryCache.setObject(diskCached, forKey: key)
            return diskCached
        }
        
        // 3. Network — slowest
        let (data, _) = try await URLSession.shared.data(from: url)
        guard let image = UIImage(data: data) else {
            throw ImageError.invalidData
        }
        
        // Store in both caches
        memoryCache.setObject(image, forKey: key)
        await diskCache.store(image, for: url)
        
        return image
    }
}
```

**BlurHash for progressive loading:**
```swift
// Show blurry placeholder while full image loads
struct PostImageView: View {
    let post: PostViewModel
    @State private var image: UIImage?
    
    var body: some View {
        ZStack {
            // Instant blurry placeholder from BlurHash
            BlurHashImage(blurHash: post.blurHash, size: .init(width: 32, height: 32))
                .opacity(image == nil ? 1 : 0)
            
            // Full image when loaded
            if let image {
                Image(uiImage: image)
                    .resizable()
                    .scaledToFill()
                    .transition(.opacity)
            }
        }
        .task {
            image = try? await ImageCache.shared.load(url: post.imageURL)
        }
    }
}
```

---

### Performance Optimizations

1. **Prefetching**: Pre-load images for off-screen cells
```swift
extension FeedViewController: UICollectionViewDataSourcePrefetching {
    func collectionView(_ collectionView: UICollectionView, 
                        prefetchItemsAt indexPaths: [IndexPath]) {
        let urls = indexPaths.compactMap { posts[$0.row].imageURL }
        ImagePrefetcher.shared.startPrefetching(urls: urls)
    }
}
```

2. **Cell height caching**: Avoid repeated layout calculations
3. **Diffable data source**: Animate only changed cells
4. **Image resizing**: Download image at display size, not full resolution
5. **Background decoding**: Decode images off main thread

---

## System Design 2: Offline-First Chat App

### Architecture Decision: Offline-First

```
User sends message
        ↓
Save to local DB immediately (status: "sending")
        ↓
Update UI optimistically (message appears instantly)
        ↓
Send to server in background
        ↓
Server ACK received → update status to "sent"
Server delivery confirmed → update to "delivered"
Recipient reads → update to "read"
```

**If send fails:**
- Keep message in local DB with status "failed"
- Show retry button
- Background retry queue attempts periodically

### Message Queue Architecture

```swift
actor MessageQueue {
    private var pendingMessages: [PendingMessage] = []
    private var isSending = false
    
    func enqueue(_ message: PendingMessage) async {
        pendingMessages.append(message)
        await flush()
    }
    
    private func flush() async {
        guard !isSending, !pendingMessages.isEmpty else { return }
        isSending = true
        defer { isSending = false }
        
        while let message = pendingMessages.first {
            do {
                try await networkClient.sendMessage(message)
                pendingMessages.removeFirst()
                await updateLocalStatus(message.id, status: .sent)
            } catch {
                // Exponential backoff before retry
                await Task.sleep(nanoseconds: 2_000_000_000)
                // Will retry on next flush call
                break
            }
        }
    }
}
```

### WebSocket Management

```swift
class WebSocketManager {
    private var webSocketTask: URLSessionWebSocketTask?
    private let session: URLSession
    private var reconnectAttempts = 0
    private let maxReconnectAttempts = 10
    
    func connect(token: String) {
        var request = URLRequest(url: wsURL)
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        webSocketTask = session.webSocketTask(with: request)
        webSocketTask?.resume()
        receiveMessages()
        startPingTimer()
    }
    
    private func receiveMessages() {
        webSocketTask?.receive { [weak self] result in
            switch result {
            case .success(let message):
                self?.handle(message)
                self?.receiveMessages() // Continue listening
            case .failure:
                self?.scheduleReconnect()
            }
        }
    }
    
    private func scheduleReconnect() {
        guard reconnectAttempts < maxReconnectAttempts else { return }
        let delay = pow(2.0, Double(reconnectAttempts)) // Exponential backoff
        reconnectAttempts += 1
        DispatchQueue.main.asyncAfter(deadline: .now() + delay) { [weak self] in
            self?.connect(token: ...)
        }
    }
    
    private func startPingTimer() {
        Timer.scheduledTimer(withTimeInterval: 30, repeats: true) { [weak self] _ in
            self?.webSocketTask?.sendPing { _ in }
        }
    }
}
```

---

## System Design 3: iOS SDK for Analytics

### Design Goals for an SDK

- **Zero impact on host app performance** (no main thread blocking)
- **Minimal binary size increase** (< 500KB)
- **Simple public API** (one-line event tracking)
- **Reliable delivery** (retry on failure, persistence across app restarts)
- **Batching** (don't send every event individually)

### Public API Design

```swift
// Simple, ergonomic public API
public final class Analytics {
    public static let shared = Analytics()
    
    private init() {}
    
    public func configure(apiKey: String, options: Options = .default) {
        AnalyticsEngine.shared.configure(apiKey: apiKey, options: options)
    }
    
    public func track(event: String, properties: [String: Any] = [:]) {
        AnalyticsEngine.shared.track(
            Event(name: event, properties: properties, timestamp: Date())
        )
    }
    
    public func identify(userId: String, traits: [String: Any] = [:]) {
        AnalyticsEngine.shared.identify(userId: userId, traits: traits)
    }
    
    public func screen(_ name: String, properties: [String: Any] = [:]) {
        track(event: "Screen Viewed", properties: ["screen": name].merging(properties) { $1 })
    }
    
    public struct Options {
        public var batchSize: Int = 20
        public var flushInterval: TimeInterval = 30
        public var maxQueueSize: Int = 1000
        public var endpoint: URL = URL(string: "https://api.analytics.com/v1/batch")!
        
        public static let `default` = Options()
    }
}
```

### Internal Engine Design

```swift
actor AnalyticsEngine {
    static let shared = AnalyticsEngine()
    
    private var eventQueue: [Event] = []
    private var flushTask: Task<Void, Never>?
    private var configuration: Analytics.Options = .default
    private let persistence: EventPersistence
    private let networkClient: AnalyticsNetworkClient
    
    func track(_ event: Event) {
        // Limit queue size to prevent memory issues
        guard eventQueue.count < configuration.maxQueueSize else { return }
        
        eventQueue.append(event)
        persistence.append(event) // Persist to survive app restart
        
        if eventQueue.count >= configuration.batchSize {
            Task { await flush() }
        }
    }
    
    func flush() async {
        guard !eventQueue.isEmpty else { return }
        
        let batch = Array(eventQueue.prefix(configuration.batchSize))
        
        do {
            try await networkClient.sendBatch(batch)
            eventQueue.removeFirst(min(batch.count, eventQueue.count))
            persistence.remove(events: batch)
        } catch {
            // Keep in queue for retry — persistence ensures survival
        }
    }
    
    private func startFlushTimer() {
        flushTask?.cancel()
        flushTask = Task {
            while !Task.isCancelled {
                try? await Task.sleep(nanoseconds: UInt64(configuration.flushInterval * 1_000_000_000))
                await flush()
            }
        }
    }
}
```

---

## System Design 4: App Modular Architecture

### Monolith → Modular Migration

**Starting state:** Single app target with everything in it

**Problem symptoms:**
- Build time > 10 minutes
- Any change triggers full recompile
- Engineers step on each other's code
- Impossible to share code with extensions

**Target state:** Feature modules with clear ownership

### Migration Strategy: Strangler Fig

```
Phase 1: Extract shared utilities (lowest risk)
  Month 1-2: Networking, Analytics, DesignSystem, Extensions

Phase 2: Extract core business logic
  Month 3-4: Auth module, UserProfile module

Phase 3: Extract feature modules (one per sprint)
  Month 5+: CheckoutFeature, SearchFeature, HomeFeature, etc.
```

### Module Interface Design

```swift
// Public interface of a feature module
// Other modules only see this, not implementation details

public protocol CheckoutFeatureInterface {
    func startCheckout(cartId: String) -> UIViewController
    func continueCheckout(orderId: String) -> UIViewController
}

// Internal implementation — hidden from other modules
final class CheckoutCoordinator: CheckoutFeatureInterface {
    private let dependencies: CheckoutDependencies
    
    public func startCheckout(cartId: String) -> UIViewController {
        let vc = CheckoutStartViewController(cartId: cartId, 
                                             dependencies: dependencies)
        return UINavigationController(rootViewController: vc)
    }
}
```

### Build Time Impact of Modularization

With a single monolith target:
- Any file change → recompile everything → 10+ min build

With modules (type-checked incrementally):
- Change in `FeatureCheckout` → recompile only `FeatureCheckout` + `App` → 1-2 min
- Change in `DesignSystem` → recompile `DesignSystem` + dependents → 3-5 min
- Change in `Networking` → full rebuild (everyone depends on it) — keep this module stable

---

## System Design Interview: How to Stand Out

### Signals Interviewers Look For

| Good Signal | How to Show It |
|---|---|
| User empathy | "Users on slow networks will see..." |
| iOS platform depth | Reference real APIs (NSCache, URLSession, NWPathMonitor) |
| Trade-off awareness | "Cursor pagination beats offset because..." |
| Scale thinking | "At 10M users, this cache eviction policy..." |
| Testability | "This architecture makes it easy to mock the repository..." |
| Monitoring | "I'd track these metrics to detect regressions..." |

### Common Mistakes to Avoid

1. **Jumping to code too fast**: Spend 5 min on requirements first
2. **Ignoring offline**: Almost every mobile design needs offline consideration
3. **Over-engineering**: Match complexity to stated requirements
4. **Only happy path**: Address error states, retry, edge cases
5. **Ignoring performance**: Memory, battery, network are always relevant on mobile
6. **Not drawing**: Visual aids massively help in system design — always whiteboard

### Template Opening Statement

> "Before I dive into the design, let me clarify a few things to make sure I'm solving the right problem. [Ask 2-3 clarifying questions]. Based on your answers, here's how I'm thinking about this..."

---

## iOS Architecture for EM: Trade-off Cheat Sheet

| Architecture | Best For | Avoid When | Test Difficulty | Code Volume |
|---|---|---|---|---|
| MVC | Tiny screens, prototypes | Large teams, complex logic | Hard | Low |
| MVP | Mid-size apps, UIKit | SwiftUI-first | Medium | Medium |
| MVVM | Most apps, SwiftUI | Tiny apps | Easy | Medium |
| VIPER | Large teams, strict roles | Solo/small teams | Easiest | Very High |
| TCA | Complex state machines | Simple CRUD apps | Easiest | High |
| Clean | Enterprise, multiple platforms | Small apps | Medium-Hard | Very High |

### The EM's Rule of Architecture Choice

> "The best architecture is the one your team can understand, maintain, and onboard new engineers into. An architecture that looks beautiful in docs but confuses your team in code is not a good architecture."
