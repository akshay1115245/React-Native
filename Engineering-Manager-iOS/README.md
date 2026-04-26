# Engineering Manager - iOS: Complete Interview Preparation & Career Roadmap

> A comprehensive, structured guide covering everything you need to know — from fundamentals to advanced leadership — to land an Engineering Manager (iOS) role at top-tier tech companies.

---

## Table of Contents

1. [Role Overview & Expectations](#1-role-overview--expectations)
2. [Core iOS Technical Knowledge](#2-core-ios-technical-knowledge)
3. [iOS Architecture & Design Patterns](#3-ios-architecture--design-patterns)
4. [iOS Performance & Optimization](#4-ios-performance--optimization)
5. [Mobile DevOps & CI/CD](#5-mobile-devops--cicd)
6. [Engineering Management Fundamentals](#6-engineering-management-fundamentals)
7. [People Management & Leadership](#7-people-management--leadership)
8. [Project & Program Management](#8-project--program-management)
9. [Cross-Functional Collaboration](#9-cross-functional-collaboration)
10. [System Design for Mobile](#10-system-design-for-mobile)
11. [Technical Strategy & Roadmap Planning](#11-technical-strategy--roadmap-planning)
12. [Data-Driven Engineering](#12-data-driven-engineering)
13. [Interview Question Bank](#13-interview-question-bank)
14. [30-60-90 Day Plan](#14-30-60-90-day-plan)
15. [Learning Resources & Skill-Building Plan](#15-learning-resources--skill-building-plan)
16. [Books, Courses & Communities](#16-books-courses--communities)

---

## 1. Role Overview & Expectations

### What Is an Engineering Manager - iOS?

An Engineering Manager (EM) for iOS is a hybrid leader who:
- Manages a team of iOS engineers (typically 4–12 direct reports)
- Is accountable for the technical quality, delivery, and growth of the iOS platform/product
- Acts as a bridge between product, design, data, and engineering
- Sets technical direction while staying close to the code (in most companies)
- Hires, retains, and grows engineers

### Difference: EM vs. Tech Lead vs. Staff Engineer

| Dimension | Tech Lead | Staff Engineer | Engineering Manager |
|---|---|---|---|
| Primary focus | Technical execution | Technical strategy | People + delivery |
| Reports | None (usually) | None | 4–12 engineers |
| Coding | 50–80% | 30–70% | 0–30% |
| Career ownership | Self | Self + influence | Others' careers |
| Accountability | Code quality | System architecture | Team outcomes |

### Typical Responsibilities

- **People**: 1:1s, performance reviews, promotions, hiring, firing, coaching
- **Delivery**: Sprint planning, roadmap execution, removing blockers
- **Technical**: Architecture reviews, technical decisions, code quality standards
- **Strategy**: Long-term iOS platform vision, tech debt management
- **Culture**: Team health, psychological safety, engineering culture
- **Stakeholder management**: Sync with PM, Design, Data, QA, Leadership

### What Top Companies Look For

| Company | Key EM Traits |
|---|---|
| Apple | Deep platform expertise, quality obsession, confidentiality discipline |
| Google | Structured thinking, data-driven decisions, career development focus |
| Meta | Speed, impact at scale, cross-functional leadership |
| Airbnb | Craft, reliability, user empathy |
| Spotify | Autonomy culture, squad model, technical depth |
| Startups | Versatility, velocity, hands-on coding |

---

## 2. Core iOS Technical Knowledge

### 2.1 Swift Language Mastery

#### Fundamentals
- Value types (`struct`, `enum`) vs. reference types (`class`)
- Optionals, optional chaining, `guard`, `if let`, `nil` coalescing
- Closures: capturing, trailing closure syntax, escaping vs. non-escaping
- Generics: type constraints, associated types, generic functions
- Protocols: protocol-oriented programming, default implementations, `where` clauses
- Error handling: `throw`, `try`, `catch`, `Result<T, E>`

#### Advanced Swift
- Property wrappers (`@State`, `@Published`, custom wrappers)
- Result builders (DSL construction in SwiftUI)
- `async`/`await` and structured concurrency (`Task`, `TaskGroup`, `Actor`)
- `Sendable` protocol and data-race safety
- `@MainActor`, global actors
- Macros (Swift 5.9+): `@Observable`, attached macros

#### Memory Management
- ARC (Automatic Reference Counting) — how it works
- Strong, weak, unowned references
- Retain cycles — detection and prevention
- Memory leaks: Instruments → Leaks / Allocations
- `[weak self]` and `[unowned self]` in closures

**Skills to Gain:**
- Build a library in pure Swift using generics and protocols
- Write a custom property wrapper
- Port a completion-handler-based API to `async/await`
- Identify and fix a retain cycle using Instruments

---

### 2.2 Objective-C (Awareness Level)

- Still prevalent in legacy codebases
- Interoperability with Swift: bridging headers, `@objc`, `@objcMembers`
- Categories, protocols, dynamic dispatch
- Memory management: MRC vs. ARC differences
- Key-Value Observing (KVO), Key-Value Coding (KVC)

**Skills to Gain:**
- Read and understand Objective-C code
- Add Swift extensions to Obj-C classes
- Know when to use `@objc` attribute

---

### 2.3 UIKit Deep Dive

#### View Hierarchy & Lifecycle
- `UIViewController` lifecycle: `viewDidLoad`, `viewWillAppear`, `viewDidAppear`, `viewWillDisappear`, `viewDidDisappear`
- `UIView` lifecycle: `init`, `layoutSubviews`, `drawRect`, `updateConstraints`
- Responder chain: how touch events propagate

#### Auto Layout
- NSLayoutConstraint, VFL, anchors
- Intrinsic content size, content hugging, compression resistance
- `UIStackView` composition
- Safe area layout guides
- Dynamic Type support

#### Table & Collection Views
- `UITableView` / `UICollectionView` data source and delegate patterns
- `UICollectionViewCompositionalLayout`
- `UICollectionViewDiffableDataSource` & `NSDiffableDataSourceSnapshot`
- Cell reuse and prefetching

#### Navigation & Routing
- `UINavigationController`, `UITabBarController`, `UISplitViewController`
- Modal presentation styles
- Deep linking and Universal Links
- Custom transitions and `UIViewControllerTransitioningDelegate`

**Skills to Gain:**
- Build a complex collection view with multiple sections and cell types
- Implement custom animated transitions
- Build a routing coordinator pattern

---

### 2.4 SwiftUI

#### Core Concepts
- Declarative UI paradigm
- `View` protocol, `body` property
- State management: `@State`, `@Binding`, `@ObservableObject`, `@EnvironmentObject`, `@Environment`
- `@Observable` macro (iOS 17+, Swift 5.9+)
- View identity and lifetime

#### Layout System
- `VStack`, `HStack`, `ZStack`, `LazyVStack`, `LazyHStack`
- `Grid`, `LazyGrid`
- `GeometryReader`
- `ViewThatFits` (adaptive layouts)

#### Advanced SwiftUI
- Custom `Layout` protocol
- `PreferenceKey` for child-to-parent communication
- `matchedGeometryEffect` for hero animations
- `Canvas` for custom drawing
- `TimelineView` for scheduled updates
- SwiftUI + UIKit interop: `UIViewRepresentable`, `UIViewControllerRepresentable`

**Skills to Gain:**
- Build a feature end-to-end in SwiftUI
- Migrate a UIKit screen to SwiftUI incrementally
- Implement a custom animation with `matchedGeometryEffect`

---

### 2.5 Concurrency & Threading

#### Grand Central Dispatch (GCD)
- Dispatch queues: serial vs. concurrent
- `DispatchQueue.main`, `DispatchQueue.global(qos:)`
- QoS classes: `.userInteractive`, `.userInitiated`, `.default`, `.utility`, `.background`
- Dispatch groups, semaphores, barriers
- Thread explosion problem

#### Operation Queue
- `Operation`, `OperationQueue`
- Dependencies between operations
- Cancellation

#### Swift Concurrency (Modern)
- `async`/`await` — sequential async code
- `Task`, `Task.detached`
- `TaskGroup` — structured parallelism
- `Actor` — data isolation
- `@MainActor` — UI updates
- `AsyncStream`, `AsyncThrowingStream`
- `Sendable` and concurrency safety
- Continuation wrapping: `withCheckedContinuation`, `withCheckedThrowingContinuation`

**Skills to Gain:**
- Rewrite a GCD-based network layer to Swift Concurrency
- Implement an actor to safely manage shared state
- Detect data races using Thread Sanitizer

---

### 2.6 Networking

#### URLSession
- `URLSession`, `URLSessionConfiguration` (default, ephemeral, background)
- `URLSessionTask` types: data, upload, download, stream, websocket
- `URLRequest`, HTTP methods, headers
- Background downloads/uploads
- Certificate pinning

#### Modern Networking
- `URLSession` with `async/await`
- Combine with networking
- Codable: `Encodable`, `Decodable`, custom coding keys, nested decoding
- REST API integration
- GraphQL basics (for companies using it)
- WebSockets

#### Network Layer Design
- Repository pattern
- Protocol-based mocking for tests
- Retry logic, exponential backoff
- Network reachability: `NWPathMonitor`

**Skills to Gain:**
- Build a generic, testable network layer
- Implement retry with exponential backoff
- Handle offline caching

---

### 2.7 Data Persistence

| Technology | Use Case |
|---|---|
| UserDefaults | Small key-value preferences |
| Keychain | Secure credentials, tokens |
| Core Data | Complex object graphs, local database |
| SwiftData | Modern Core Data (iOS 17+) |
| SQLite / GRDB | High-performance queries |
| FileManager | Binary files, documents |
| CloudKit | iCloud sync |

#### Core Data Deep Dive
- `NSManagedObjectContext`, `NSPersistentContainer`
- Fetch requests, predicates, sort descriptors
- Relationships and cascades
- Migration: lightweight vs. heavy migration
- Background contexts for off-main-thread operations
- `NSFetchedResultsController` for UI sync

**Skills to Gain:**
- Model a multi-entity Core Data schema with relationships
- Implement background fetch and merge to main context
- Perform a Core Data migration

---

### 2.8 Security

- Keychain Services API
- Biometric authentication: `LocalAuthentication` framework, Face ID / Touch ID
- Transport Layer Security: ATS (App Transport Security)
- Certificate pinning
- Jailbreak detection techniques
- Data encryption: `CryptoKit` (AES-GCM, HMAC, SHA hashing)
- OAuth 2.0 / PKCE flow for auth
- Secure coding practices: input validation, avoiding SQL injection

**Skills to Gain:**
- Implement biometric login with Keychain fallback
- Implement certificate pinning
- Use CryptoKit for encrypting local data

---

### 2.9 Testing

#### Unit Testing
- XCTest framework
- Arrange-Act-Assert pattern
- Mocking with protocols
- `@testable import`
- Test doubles: stub, mock, fake, spy

#### UI Testing
- `XCUIApplication`, `XCUIElement`
- Accessibility identifiers
- Page Object Model for UI tests
- Test performance

#### Snapshot Testing
- `swift-snapshot-testing` library
- Visual regression detection

#### TDD & BDD
- Test-Driven Development cycle (Red-Green-Refactor)
- Quick + Nimble for BDD-style tests
- Code coverage targets (aim for 70%+ on business logic)

**Skills to Gain:**
- Achieve 80%+ coverage on a service layer with unit tests
- Set up UI tests for critical user flows
- Set up snapshot tests for key UI components

---

## 3. iOS Architecture & Design Patterns

### 3.1 MVC (Model-View-Controller)

- Apple's default; leads to Massive View Controller if not disciplined
- Controller mediates Model ↔ View
- When appropriate: simple screens, prototypes

### 3.2 MVP (Model-View-Presenter)

- Presenter holds UI logic, View is passive
- Easier to unit test than MVC
- Boilerplate-heavy

### 3.3 MVVM (Model-View-ViewModel)

- ViewModel exposes state; View observes
- Pairs naturally with Combine / SwiftUI
- Works well with reactive programming
- Key: ViewModel should not import UIKit

### 3.4 VIPER

- View, Interactor, Presenter, Entity, Router
- Strict separation of concerns
- Common in large teams with many engineers
- Verbose but highly testable

### 3.5 The Composable Architecture (TCA)

- State, Action, Reducer, Store, Effect
- Unidirectional data flow
- Point-Free library
- Strong testing story
- Good for complex state machines

### 3.6 Clean Architecture

- Entities → Use Cases → Interface Adapters → Frameworks
- Dependency rule: inner layers know nothing about outer
- Combine with any of the above patterns

### 3.7 Coordinator Pattern

- Decouple navigation from ViewControllers
- `Coordinator` protocol with `start()` method
- Child coordinators for sub-flows
- Works with both UIKit and SwiftUI

### 3.8 Dependency Injection

- Constructor injection (preferred)
- Property injection
- DI containers: Swinject, Needle, Factory
- Avoiding service locator anti-pattern

### 3.9 Design Patterns (GoF Patterns in iOS Context)

| Pattern | iOS Usage |
|---|---|
| Singleton | `URLSession.shared`, `NotificationCenter.default` — use sparingly |
| Observer | `NotificationCenter`, Combine, KVO |
| Delegate | `UITableViewDelegate`, custom callbacks |
| Factory | View/VC creation in coordinators |
| Builder | Complex object creation (URL builders) |
| Strategy | Interchangeable algorithms (sorting, networking) |
| Decorator | Extending behavior without subclassing |
| Command | Undo/redo operations |

**Skills to Gain:**
- Refactor an MVC app to MVVM+Coordinator
- Build a feature using Clean Architecture
- Explain trade-offs of each architecture to your team

---

## 4. iOS Performance & Optimization

### 4.1 Rendering Performance

- Core Animation pipeline: app → render server → GPU
- `CALayer` vs `UIView`
- Offscreen rendering: when it happens, how to avoid
- `shouldRasterize` trade-offs
- Overdraw detection with Color Blended Layers
- Main thread rule: always update UI on main thread
- `drawRect` performance implications
- Avoiding layout recalculation on scroll

### 4.2 Memory Optimization

- Instruments: Allocations, Leaks, VM Tracker
- Memory warnings: `didReceiveMemoryWarning`
- Image memory: `UIImage` vs `CGImage` compression
- Lazy loading of heavy resources
- `NSCache` for memory-sensitive caching
- Avoid large objects on stack

### 4.3 Launch Time Optimization

- Pre-main time: dylib loading, Objective-C runtime, initializers
- Post-main time: `application(_:didFinishLaunchingWithOptions:)`
- Techniques: fewer dylibs, lazy initialization, background pre-warming
- MetricKit for launch time monitoring
- `DYLD_PRINT_STATISTICS` environment variable

### 4.4 Energy & Battery

- Reduce background activity
- Use `URLSession` background configurations
- Batch network requests
- Avoid polling; use push notifications
- Location: use appropriate accuracy level
- Background fetch: `BGTaskScheduler`

### 4.5 Network Performance

- HTTP/2 multiplexing
- Response caching: `URLCache`
- Image caching: `NSCache`, third-party (Kingfisher, SDWebImage)
- Pagination and lazy loading
- Compression (gzip)
- Protobuf vs JSON

### 4.6 Profiling Tools

| Tool | Purpose |
|---|---|
| Instruments - Time Profiler | CPU hotspots |
| Instruments - Allocations | Memory allocations |
| Instruments - Leaks | Memory leaks |
| Instruments - Core Animation | Rendering performance |
| Instruments - Network | HTTP traffic analysis |
| MetricKit | Real-device production metrics |
| Xcode Organizer | Crash reports, energy reports |
| os_signpost | Custom performance points |

**Skills to Gain:**
- Profile an app with Time Profiler and fix a CPU hotspot
- Reduce app launch time by 20%
- Detect and fix a memory leak using Instruments

---

## 5. Mobile DevOps & CI/CD

### 5.1 Build Systems

- Xcode build system fundamentals
- `xcodebuild` CLI
- Build configurations: Debug, Release, custom
- Build settings, xcconfig files
- Schemes and targets
- SPM (Swift Package Manager) vs. CocoaPods vs. Carthage

### 5.2 Continuous Integration

| Tool | Notes |
|---|---|
| Xcode Cloud | Apple-native, tight Xcode integration |
| Bitrise | Mobile-first CI, rich iOS integrations |
| Fastlane | Automation tool for building, testing, deploying |
| GitHub Actions | General purpose, extensive marketplace |
| CircleCI | Flexible, good macOS support |
| Jenkins | Self-hosted, maximum control |

### 5.3 Fastlane Essentials

- `fastlane scan` — run tests
- `fastlane gym` — build IPA
- `fastlane deliver` — upload to App Store Connect
- `fastlane match` — code signing management
- `fastlane pilot` — TestFlight management
- Lanes and custom actions

### 5.4 Code Signing

- Certificates: Development, Distribution
- Provisioning profiles: development, ad hoc, App Store, enterprise
- `match` for team-wide code signing
- Automatic vs. manual signing
- Apple Developer Program management

### 5.5 App Distribution

- TestFlight: internal vs. external testing
- App Store review process and guidelines
- Enterprise distribution
- Ad hoc distribution
- App Store Connect API

### 5.6 Release Engineering

- Semantic versioning (`MARKETING_VERSION`, `CURRENT_PROJECT_VERSION`)
- Feature flags: LaunchDarkly, Firebase Remote Config, custom
- Phased releases on App Store
- Rollback strategies (cannot pull from App Store; use feature flags)
- Crash monitoring: Firebase Crashlytics, Sentry, Bugsnag

**Skills to Gain:**
- Set up a complete Fastlane pipeline for build → test → deploy
- Configure Xcode Cloud or Bitrise for a project
- Implement feature flag infrastructure

---

## 6. Engineering Management Fundamentals

### 6.1 The Manager's Job

- **Output**: Your team's output is your output (Andy Grove)
- **Leverage**: Focus on high-leverage activities (1:1s, hiring, architecture reviews, process improvements)
- **Context**: Give context, not control; set clear goals, let engineers decide how
- **Trust**: Build trust through consistency and follow-through

### 6.2 Management vs. Leadership

| Management | Leadership |
|---|---|
| Plans and budgets | Sets direction and vision |
| Organizes and staffs | Aligns people to direction |
| Controls and problem-solves | Motivates and inspires |
| Produces predictability | Produces change |

Great EMs do both.

### 6.3 The Dual Ladder

- IC (Individual Contributor): SWE → Senior → Staff → Principal → Fellow
- Management: EM → Senior EM → Director → VP → SVP → CTO
- Understanding both paths helps with career conversations

### 6.4 Manager Anti-Patterns to Avoid

- **Seagull manager**: appears only to criticize, then leaves
- **Micromanager**: over-controls, kills autonomy
- **Absentee manager**: too hands-off, team drifts
- **Hero manager**: does everything themselves instead of enabling team
- **Friend over manager**: avoids hard conversations

---

## 7. People Management & Leadership

### 7.1 1:1 Meetings

**Purpose:**
- Relationship building
- Information gathering (team health)
- Coaching and growth
- Unblocking

**Best Practices:**
- Weekly for direct reports, biweekly minimum
- Engineer sets the agenda primarily
- Note-taking and follow-through essential
- Mix: short-term (tactical), long-term (growth), personal check-in

**Sample 1:1 Agenda:**
1. How are you doing? (personal first)
2. What's on your mind? / What's blocking you?
3. Project updates (briefly)
4. Career and growth (rotate topics)
5. Feedback exchange (two-way)

### 7.2 Performance Management

#### Setting Expectations
- Clear job levels and expectations (leveling rubrics)
- OKRs or goals set collaboratively
- Regular check-ins, not just annual reviews

#### Performance Reviews
- Gather peer feedback (360°)
- Self-evaluation
- Manager assessment
- Calibration with peer managers
- Written review + delivery conversation

#### Performance Improvement Plans (PIPs)
- Only after significant coaching
- Specific, measurable goals
- Regular check-ins
- Document everything
- Often results in separation; treat with dignity

#### Promotions
- Evidence-based: gather impact data proactively
- Promote for next level, not current excellence
- Know your company's promotion process and timelines
- Advocate loudly in calibrations

### 7.3 Hiring

#### Building a Strong Hiring Funnel
- Write compelling, inclusive job descriptions
- Source proactively (LinkedIn, GitHub, conferences, internal referrals)
- Partner with recruiting team
- Diverse interview panels

#### Interview Design
- Define what you're assessing before designing questions
- Structured interviews with consistent rubrics
- iOS technical screen: coding, architecture, debugging
- Behavioral interviews: STAR format
- Bar raiser concept (Amazon)

#### Candidate Experience
- Fast feedback loops
- Communicate clearly throughout
- Respect candidate's time

#### Onboarding
- First 30/60/90 day plan
- Buddy system
- Gradual ownership: shadow → co-pilot → solo → lead
- Early wins matter for confidence

### 7.4 Feedback & Coaching

#### SBI Model (Situation-Behavior-Impact)
- **Situation**: "In yesterday's design review..."
- **Behavior**: "...you interrupted Sarah three times..."
- **Impact**: "...which made her hesitant to share ideas."

#### GROW Coaching Model
- **Goal**: What do you want to achieve?
- **Reality**: What's happening now?
- **Options**: What could you do?
- **Will**: What will you do?

#### Radical Candor (Kim Scott)
- **Care Personally**: genuinely care about people
- **Challenge Directly**: be honest and direct
- Avoid: Ruinous Empathy, Obnoxious Aggression, Manipulative Insincerity

### 7.5 Team Motivation & Engagement

#### Intrinsic Motivators (Daniel Pink - Drive)
- **Autonomy**: control over their work
- **Mastery**: getting better at something
- **Purpose**: believing work matters

#### Psychological Safety (Amy Edmondson)
- Team members feel safe to take risks and speak up
- Build by: modeling vulnerability, punishing blame, rewarding learning from failure

#### Recognition & Appreciation
- Public recognition for impact
- Private recognition for personal growth
- Timely (not months later)
- Specific (not generic "good job")

### 7.6 Difficult Conversations

**Framework:**
1. Prepare: facts, impact, desired outcome
2. Open: state your intent clearly
3. Listen: understand their perspective
4. Explore: find root causes
5. Plan: agree on next steps
6. Follow up: check in consistently

**Topics requiring difficult conversations:**
- Underperformance
- Behavioral issues (communication, attitude)
- Missed promotion
- Layoff/termination
- Team conflict

---

## 8. Project & Program Management

### 8.1 Agile for Engineering Managers

#### Scrum Roles
- Product Owner: what to build
- Scrum Master: how the team works
- Development Team: building
- EM responsibility: often acts as facilitator and escalation path

#### Key Ceremonies
- Sprint planning: commit to sprint scope
- Daily standup: blockers and coordination
- Sprint review: demo to stakeholders
- Retrospective: team improvement

#### Kanban Alternative
- Continuous flow instead of sprints
- WIP (Work In Progress) limits
- Good for operational/support teams

### 8.2 Estimation & Planning

- Story points vs. time-based estimation
- T-shirt sizing for roadmap planning
- Three-point estimation: optimistic, likely, pessimistic
- Accounting for: bugs, tech debt, on-call, meetings, PTO
- Historical velocity as estimation baseline

### 8.3 Risk Management

- Identify risks early (technical, resource, dependency)
- Risk matrix: likelihood × impact
- Mitigation vs. contingency planning
- Communicate risks proactively to stakeholders

### 8.4 Technical Debt Management

- Define and categorize technical debt
- Make debt visible: track in backlog
- Negotiate dedicated debt sprints (20% of capacity as rule of thumb)
- Distinguish between reckless and prudent debt (Ward Cunningham)

### 8.5 Incident Management

- Severity levels (P0–P4)
- On-call rotations and schedules
- Runbooks: documented response procedures
- Post-mortems: blameless, focus on systems
- Five Whys root cause analysis
- Metrics: MTTR (Mean Time To Restore), MTTD (Mean Time To Detect)

### 8.6 Delivery Metrics

| Metric | What It Measures |
|---|---|
| Lead Time | Idea → Production |
| Cycle Time | Code complete → Production |
| Deployment Frequency | How often you ship |
| Change Failure Rate | % of deployments causing failures |
| MTTR | Time to recover from failure |

These are the DORA metrics — industry standard for measuring engineering team performance.

---

## 9. Cross-Functional Collaboration

### 9.1 Working with Product Management

- Understand the product roadmap and business context
- Push back constructively on scope creep
- Offer technical alternatives when asked to cut features
- Bring engineering constraints to roadmap discussions early
- "Build the right thing" — PMs own this, but EMs must inform it

### 9.2 Working with Design

- Involve engineers in design reviews early
- Raise feasibility and performance concerns before implementation
- Maintain a design system for consistency
- iOS HIG (Human Interface Guidelines) — know it well
- Accessibility standards: WCAG, `UIAccessibility`

### 9.3 Working with QA / Test Engineering

- Define quality standards and acceptance criteria
- Shift-left testing: testing earlier in the cycle
- Shared ownership of quality
- Flaky test management

### 9.4 Working with Data / Analytics

- Instrument iOS apps for tracking: Amplitude, Mixpanel, Firebase Analytics
- Define events and properties with data team
- Experiment infrastructure: A/B testing (Firebase A/B, Optimizely)
- Review A/B test results and make data-driven decisions

### 9.5 Working with Platform / Backend

- API versioning and iOS backward compatibility
- Contract testing: Pact
- Backend-for-frontend (BFF) pattern
- Breaking change communication and migration plans

### 9.6 Executive Communication

- Update format: what's happening, impact, what we need
- Speak in business outcomes, not technical details (unless asked)
- Dashboard-driven visibility: OKRs, KPIs, sprint metrics
- Never surprise executives — proactively escalate issues

---

## 10. System Design for Mobile

### 10.1 Mobile System Design Framework

Use this framework to structure any mobile system design question:

1. **Requirements clarification** (functional + non-functional)
2. **High-level architecture** (client-server interaction)
3. **Data model** (local and remote)
4. **API design** (REST endpoints, GraphQL queries)
5. **Client-side architecture** (module breakdown)
6. **Offline support** strategy
7. **Performance** (pagination, caching, lazy loading)
8. **Reliability** (error handling, retry, circuit breaker)
9. **Security** (auth, data at rest, in transit)
10. **Analytics & monitoring**

### 10.2 Common Mobile Design Problems

#### Design an Offline-First App
- Local database (Core Data / SQLite) as source of truth
- Sync engine: conflict resolution strategies (last-write-wins, CRDTs, operational transforms)
- Queue outgoing mutations for when network returns
- Optimistic UI updates

#### Design a Real-Time Chat App (iOS)
- WebSocket connection management
- Message ordering and deduplication
- Push notifications: APNs (Apple Push Notification service)
- Local persistence with unread counts
- Typing indicators, read receipts

#### Design an Image Feed (Instagram-like)
- Pagination: offset vs. cursor-based
- Image caching: `NSCache` + disk cache
- Prefetching with `UICollectionViewDataSourcePrefetching`
- Upload pipeline: compress → upload → CDN
- Optimistic rendering

#### Design an Offline-Capable Maps App
- Tile-based map rendering
- Tile caching strategies
- Vector vs. raster tiles
- Routing algorithm with local data

### 10.3 Client Architecture Design

- Modular architecture: feature modules, core modules, shared modules
- Dependency graph: avoid circular dependencies
- Binary frameworks vs. source packages
- Interface modules for decoupling
- Dynamic vs. static frameworks: trade-offs

### 10.4 Scaling iOS Teams

- Micro-frontend equivalent: feature flags, modular architecture
- Parallel builds: Xcode parallelization settings
- Remote build cache (Bazel, Gradle Enterprise for iOS)
- Build time optimization strategies

---

## 11. Technical Strategy & Roadmap Planning

### 11.1 Setting Technical Vision

- Where is the iOS platform today? (current state)
- Where should it be in 1-2 years? (future state)
- What's the gap and the path? (strategy)
- Communicate vision: ADRs (Architecture Decision Records), RFCs

### 11.2 Architecture Decision Records (ADRs)

**Template:**
```
# ADR-001: Adopt SwiftUI for new features

## Status: Accepted

## Context
Our UIKit codebase is aging. New engineers prefer SwiftUI.
SwiftUI is now stable (iOS 15+).

## Decision
All new screens will be built in SwiftUI.
UIKit remains for legacy screens until refactored.

## Consequences
- Faster UI development
- Need SwiftUI training for senior engineers
- Interop layer needed for shared navigation
```

### 11.3 Technology Adoption

**Technology Radar Framework:**
- Adopt: use in production now
- Trial: use on projects with low risk
- Assess: worth exploring in prototypes
- Hold: do not start new work with

### 11.4 Managing Legacy Code

- Strangler Fig pattern: replace incrementally
- Wrap before refactor: isolate legacy behind interfaces
- Boy Scout Rule: leave code better than you found it
- Measure: track % new vs. legacy code over time

### 11.5 Build vs. Buy Decisions

| Factor | Build | Buy / Open Source |
|---|---|---|
| Core differentiator? | Build | — |
| Available quality solution? | — | Buy |
| Total cost of ownership | Higher | Lower (usually) |
| Customization needs | High | Low |
| Time to market | Slower | Faster |

### 11.6 Platform Engineering for iOS

- Shared design system (fonts, colors, components)
- Common networking and auth modules
- Analytics SDK abstraction
- Error handling and logging standards
- Feature flag infrastructure

---

## 12. Data-Driven Engineering

### 12.1 Key iOS Metrics

#### User-Facing Metrics
- Crash-free sessions rate (target: >99.5%)
- App launch time (cold/warm/hot launch)
- ANR / Hang rate (watchdog terminations, main thread hangs)
- Screen load time (P50, P90, P99)
- Network error rate

#### Business Metrics
- DAU/MAU (Daily/Monthly Active Users)
- Retention (D1, D7, D30)
- Session length and depth
- Conversion rates (funnel analysis)
- Feature adoption rate

#### Team Metrics
- Cycle time and lead time
- Deployment frequency
- Bug escape rate
- Test coverage
- Build time

### 12.2 Instrumentation

- Event tracking: user actions, screen views, errors
- Custom MetricKit metrics
- Logging: `os_log`, Unified Logging System
- Distributed tracing: correlate iOS events with backend traces

### 12.3 A/B Testing

- Hypothesis: "We believe X will improve Y by Z"
- Experiment setup: control vs. treatment group
- Statistical significance: p-value < 0.05, power ≥ 0.8
- Guard rails: monitor for negative side effects
- Ship or kill: data-driven decisions

### 12.4 Dashboards & Visibility

- Build dashboards for: releases, crashes, performance, product metrics
- Share with team and stakeholders
- Alert on regressions (automated)
- Weekly team metrics review

---

## 13. Interview Question Bank

### 13.1 Technical iOS Questions

**Architecture:**
- "How would you choose between MVVM and VIPER for a new iOS project?"
- "Explain the coordinator pattern. How does it solve the massive view controller problem?"
- "How do you handle dependency injection at scale in an iOS app?"
- "Describe how you would migrate a UIKit app to SwiftUI incrementally."

**Concurrency:**
- "Explain the difference between GCD and Swift concurrency. When would you choose one over the other?"
- "What are actors in Swift concurrency and what problem do they solve?"
- "How do you prevent main thread blocking in a UIKit app?"
- "What is a retain cycle and how does [weak self] solve it in a closure?"

**Performance:**
- "How would you investigate and fix an app that users say 'feels slow'?"
- "Explain the Core Animation rendering pipeline."
- "How do you optimize table view scrolling performance?"
- "What causes app launch time to increase and how do you fix it?"

**Networking:**
- "Design a networking layer for a production iOS app."
- "How would you implement offline support in an iOS app?"
- "Explain certificate pinning and when you'd use it."

### 13.2 Engineering Management Behavioral Questions

**Leadership & People:**
- "Tell me about a time you turned around an underperforming engineer."
- "How do you handle a situation where your best engineer wants to leave?"
- "Describe how you've built a high-performing team from scratch."
- "Tell me about a time you had to make an unpopular decision with your team."
- "How do you balance technical work with management responsibilities?"

**Delivery & Execution:**
- "Tell me about a project that was severely behind schedule. How did you handle it?"
- "How do you manage technical debt while maintaining velocity?"
- "Describe a time you had to negotiate scope with a product manager."
- "How do you ensure quality without slowing down your team?"

**Conflict & Communication:**
- "Tell me about a conflict between two senior engineers on your team. How did you resolve it?"
- "How do you handle disagreement with your own manager?"
- "Describe a time you had to deliver difficult feedback to an engineer."
- "How do you communicate a project delay to stakeholders?"

**Strategy & Vision:**
- "How do you balance short-term delivery with long-term technical health?"
- "Tell me about a major technical decision you drove for your iOS platform."
- "How do you stay current with iOS platform changes while managing a team?"
- "Describe how you built the technical roadmap for your iOS team."

**Hiring:**
- "How do you assess iOS engineering talent in an interview?"
- "Tell me about a great hire you made and what made them great."
- "How do you build a diverse and inclusive engineering team?"
- "What makes a great onboarding experience for a new iOS engineer?"

### 13.3 System Design Interview Questions

- "Design the iOS client architecture for a social media feed app."
- "Design an offline-first to-do app for iOS."
- "How would you design the push notification system for a chat app?"
- "Design the iOS architecture for a real-time collaborative document editor."
- "How would you design the iOS SDK for a third-party analytics provider?"

### 13.4 STAR Answer Templates

**STAR Format:** Situation → Task → Action → Result

**Example: Managing underperformance**

> **Situation**: One of my senior iOS engineers was consistently missing deadlines and producing code with high bug counts. Team morale was starting to dip.
>
> **Task**: I needed to address the performance issue while preserving team trust and being fair to the engineer.
>
> **Action**: I had a candid 1:1 conversation, gathered specific examples with data, collaborated on a PIP with clear 30-day goals, provided weekly check-ins with coaching, and looped in HR. I also helped the engineer understand the why — they were struggling with a personal situation I wasn't aware of.
>
> **Result**: The engineer improved significantly over 45 days, completed the PIP successfully, and has since led two major features. Team morale improved as they saw the issue being addressed directly.

---

## 14. 30-60-90 Day Plan

### First 30 Days: Listen & Learn

**Goal: Build trust and understand the current state**

**Week 1–2 (Orientation):**
- Meet with every direct report (1:1, discovery conversation)
- Meet with key stakeholders: PM, Design, QA leads, senior engineers
- Review existing iOS codebase, architecture docs, ADRs
- Understand CI/CD pipeline end-to-end
- Review crash reports, performance dashboards, App Store reviews

**Week 3–4 (Diagnosis):**
- Shadow team in standups, sprint planning, design reviews
- Review last 3 sprint retrospectives
- Understand current technical debt inventory
- Identify top 3 team pain points
- Review open bugs and P0/P1 incident history

**Deliverable by Day 30:** Written "State of the iOS Team" doc with observations and early hypotheses

---

### Days 31–60: Build Relationships & Early Wins

**Goal: Establish credibility and begin shaping**

- Establish regular 1:1 cadence and fill in team member growth plans
- Drive one quick win (e.g., fix broken CI pipeline, automate a manual process)
- Begin structured code reviews to understand code quality
- Participate actively in architecture discussions
- Set up metrics dashboards for team visibility
- Identify one area for process improvement and pilot it

**Deliverable by Day 60:** Updated team goals aligned with product roadmap; first engineering OKRs draft

---

### Days 61–90: Set Direction & Deliver

**Goal: Lead from the front with a clear vision**

- Define iOS technical roadmap for next 2 quarters
- Introduce one architectural improvement initiative
- Run team health survey and share results with team
- Launch structured interview process improvements
- Deliver first complete sprint cycle as EM
- Present iOS platform strategy to engineering leadership

**Deliverable by Day 90:** Presented iOS Technical Strategy deck; team OKRs finalized; clear roadmap communicated

---

## 15. Learning Resources & Skill-Building Plan

### Phase 1: iOS Technical Mastery (Months 1–3)

| Topic | Action |
|---|---|
| Swift advanced features | Build a real app using async/await, actors, Combine |
| SwiftUI | Complete a project from scratch in SwiftUI |
| Core Data / SwiftData | Build a local-first app with full CRUD and migration |
| Testing | Achieve 80%+ coverage on a new module |
| Performance | Profile a real app with Instruments; fix 2 issues |
| Architecture | Refactor an MVC app to MVVM+Coordinator |
| CI/CD | Set up a complete Fastlane pipeline from scratch |

### Phase 2: Management Fundamentals (Months 2–4)

| Topic | Action |
|---|---|
| 1:1 structure | Run structured 1:1s and document learnings |
| Giving feedback | Practice SBI model in low-stakes situations |
| Conflict resolution | Role-play difficult conversations |
| Hiring | Conduct 10+ technical interviews with structured rubrics |
| Performance reviews | Write sample performance reviews for hypothetical engineers |
| Goal setting | Write OKRs for a hypothetical iOS team |

### Phase 3: Strategy & Leadership (Months 3–6)

| Topic | Action |
|---|---|
| Technical vision | Write a 12-month iOS platform strategy doc |
| Architecture decisions | Write 5 ADRs for real or hypothetical decisions |
| System design | Practice 10 mobile system design problems |
| Executive communication | Present a mock iOS status update to senior stakeholders |
| Data-driven decisions | Analyze A/B test results and write a decision memo |
| Cross-functional | Simulate PM/EM collaboration on a feature |

### Phase 4: Interview Preparation (Months 4–6)

| Activity | Frequency |
|---|---|
| STAR answer preparation | Write 20 STAR stories covering all key behavioral themes |
| Technical coding practice | 2–3 LeetCode/Swift Coding problems per week |
| System design practice | 2 mobile system designs per week with peer review |
| Mock interviews | 5+ mock EM interviews with engineers or coaches |
| Role-specific research | Research target company's iOS architecture and culture |
| Applied networking | Connect with EMs at target companies on LinkedIn |

---

## 16. Books, Courses & Communities

### Essential Books for iOS Engineering Managers

#### Management & Leadership
| Book | Author | Key Value |
|---|---|---|
| The Manager's Path | Camille Fournier | Best intro to engineering management, EM-specific |
| High Output Management | Andy Grove | Management fundamentals from Intel CEO |
| An Elegant Puzzle | Will Larson | Engineering management at scale |
| Radical Candor | Kim Scott | Feedback and leadership framework |
| Accelerate | Nicole Forsgren | Data-driven engineering, DORA metrics |
| The Five Dysfunctions of a Team | Patrick Lencioni | Team dynamics and trust |
| Drive | Daniel Pink | Motivation and autonomy |
| Crucial Conversations | Patterson et al. | Handling difficult conversations |
| First, Break All the Rules | Marcus Buckingham | Great manager behaviors from Gallup research |
| No Rules Rules | Reed Hastings | Netflix culture and high performance |

#### iOS & Technical
| Book | Author | Key Value |
|---|---|---|
| Swift in Depth | Tjeerd in 't Veen | Advanced Swift patterns |
| iOS Unit Testing by Example | Jon Reid | Test-driven iOS development |
| Advanced iOS App Architecture | Rene Cacheaux | Architecture patterns in depth |
| Swift Design Patterns | Paul Hudson | Design patterns in Swift |
| Designing Data-Intensive Applications | Martin Kleppmann | Backend systems knowledge for EMs |
| A Philosophy of Software Design | John Ousterhout | Code complexity and design |
| Clean Architecture | Robert C. Martin | Architecture principles |

### Online Courses

| Platform | Course | Purpose |
|---|---|---|
| Apple Developer | WWDC sessions | Latest iOS APIs and best practices |
| Point-Free | pointfree.co | Functional Swift, TCA, Composable Architecture |
| Ray Wenderlich / Kodeco | iOS courses | Comprehensive iOS topics |
| Stanford CS193p | SwiftUI App Development | Free, university-level SwiftUI |
| Pluralsight | iOS architecture courses | Architecture deep dives |
| Coursera | Engineering Management specializations | Management frameworks |
| LinkedIn Learning | People management courses | Soft skills development |

### Platforms & Practice

| Platform | Use |
|---|---|
| GitHub | Build portfolio projects, contribute to open source |
| LeetCode (Swift) | Coding interview practice |
| Excalidraw / Miro | System design whiteboarding practice |
| Newsletter: iOS Dev Weekly | Stay current with iOS ecosystem |
| Newsletter: Lenny's Newsletter | Product and engineering leadership |
| Newsletter: The Pragmatic Engineer | Engineering management insights (Gergely Orosz) |

### Communities

| Community | Value |
|---|---|
| iOS Dev Happy Hour (Slack) | iOS developer community |
| Swift Forums (forums.swift.org) | Swift language evolution discussions |
| Indie Dev Monday | Indie iOS developers |
| iOSLeadEssentials.com | iOS architecture and career community |
| Engineering Managers Slack (Rands) | Rands Leadership Slack — large EM community |
| LinkedIn groups | Engineering Management, iOS Development groups |
| Local iOS Meetups / NSConference | In-person networking |
| WWDC (Apple Developer Conference) | Annual Apple platform updates |

### Podcasts

| Podcast | Focus |
|---|---|
| Swift by Sundell | iOS development best practices |
| iOS Dev Discussions | iOS career and technical topics |
| Stacktrace | iOS and Apple ecosystem |
| Developing Leadership | Engineering leadership podcast |
| The Engineering Manager | EM-focused podcast |
| Soft Skills Engineering | Non-technical career advice for engineers |
| Lenny's Podcast | Product and growth (EM-relevant) |

---

## Quick Reference: Interview Readiness Checklist

### Technical iOS (Self-Assessment)

- [ ] Can explain ARC, retain cycles, and weak/unowned confidently
- [ ] Have implemented async/await and actors in a real project
- [ ] Can design a production-grade networking layer from scratch
- [ ] Know MVVM, VIPER, TCA trade-offs and can explain them clearly
- [ ] Have diagnosed and fixed a memory leak using Instruments
- [ ] Have optimized app launch time
- [ ] Understand Core Data migrations
- [ ] Can set up a CI/CD pipeline with Fastlane
- [ ] Have built features in both UIKit and SwiftUI
- [ ] Understand certificate pinning and Keychain usage

### Management (Self-Assessment)

- [ ] Have managed at least 4 direct reports (preferred)
- [ ] Have conducted 10+ technical interviews
- [ ] Have delivered performance reviews and difficult feedback
- [ ] Have driven a project from planning to production
- [ ] Have managed technical debt negotiation with product
- [ ] Have experienced or led incident response (on-call)
- [ ] Have hired and onboarded engineers
- [ ] Can run a blameless post-mortem
- [ ] Have set OKRs or team goals
- [ ] Have influenced without authority across teams

### Behavioral STAR Stories Prepared

- [ ] Technical decision I drove and its impact
- [ ] Conflict I resolved between engineers
- [ ] Underperforming engineer I helped improve
- [ ] Project that was at risk and how I saved it
- [ ] Unpopular decision I made and how I handled pushback
- [ ] Great hire I made
- [ ] Technical debt strategy I implemented
- [ ] Cross-functional win I delivered
- [ ] Promotion I advocated for (or denied, with reasoning)
- [ ] Culture change I drove on the team

---

## Key Frameworks Summary Card

| Framework | Use |
|---|---|
| STAR | Behavioral interview answers |
| SBI | Giving specific feedback |
| GROW | Coaching conversations |
| DORA Metrics | Measuring team performance |
| RACI | Defining ownership and accountability |
| RFC / ADR | Technical decision documentation |
| OKR | Goal setting and alignment |
| Radical Candor | Feedback culture |
| Technology Radar | Technology adoption decisions |
| Strangler Fig | Legacy code migration |

---

*This document is a living reference. Revisit and update it as you grow in your Engineering Manager journey.*
