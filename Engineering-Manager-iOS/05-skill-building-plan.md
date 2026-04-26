# Skill-Building Action Plan: Engineering Manager - iOS

> A structured, time-phased plan to build every skill needed to land and excel in an EM - iOS role.

---

## Self-Assessment: Where Are You Today?

Rate yourself honestly on each area (1-5):

### iOS Technical Skills

| Skill | 1 (Beginner) | 3 (Intermediate) | 5 (Expert) | Your Score |
|---|---|---|---|---|
| Swift language (advanced) | Can't explain ARC | Comfortable with generics, protocols | Deep knowledge of concurrency, macros | ___ |
| UIKit | Can't build a list | Builds features independently | Expert in collection views, animation, perf | ___ |
| SwiftUI | Never used it | Built simple screens | Built complex apps, knows internals | ___ |
| iOS Architecture | Knows MVC | Implements MVVM | Chose arch for multiple real projects | ___ |
| Concurrency | Uses DispatchQueue.main | Understands GCD | Deep knowledge of Swift Concurrency, actors | ___ |
| Testing | No tests | Some unit tests | TDD, 80%+ coverage, UI tests, mocks | ___ |
| Performance | Not profiled apps | Used Instruments once | Optimized launch, scroll, memory in prod | ___ |
| Networking | Makes URLSession calls | Designed a network layer | Production-grade layer with retry, caching | ___ |
| CI/CD | Never set up | Used existing pipelines | Set up Fastlane + Xcode Cloud from scratch | ___ |
| Security | Basic HTTPS | Keychain usage | Certificate pinning, CryptoKit, OAuth/PKCE | ___ |

### Management Skills

| Skill | 1 (No Experience) | 3 (Some Experience) | 5 (Expert) | Your Score |
|---|---|---|---|---|
| 1:1s | Never done | Running 1:1s | Coaching, relationship-building, career convos | ___ |
| Performance management | Never done | Given feedback | Full PIP cycle, reviews, promotions | ___ |
| Hiring | Never interviewed | Participated in interviews | Owned loop, designed process, made offers | ___ |
| Goal setting (OKRs) | Never done | Written OKRs | Aligned team to company strategy via OKRs | ___ |
| Conflict resolution | Avoid conflict | Address directly | Skilled facilitator, resolved team conflicts | ___ |
| Technical strategy | Never done | Contributed to strategy | Authored and presented platform strategy | ___ |
| Stakeholder management | Individual contributor | Some PM/Design interaction | Owned relationships across multiple functions | ___ |
| Incident management | Not on call | Participated in incidents | Led P0 response, post-mortems, process design | ___ |
| Delivery management | No tracking | Tracks sprint | Manages roadmap, risk, scope negotiation | ___ |
| Hiring | Never hired | 1-2 hires | Built team, pipeline, interview process | ___ |

---

## Scoring Guide

| Total Score (sum of all 20) | Status |
|---|---|
| 80-100 | Ready for senior EM interviews |
| 60-79 | Ready for EM interviews, gaps to address |
| 40-59 | Needs 6-12 months of deliberate practice |
| Below 40 | Needs 12-18+ months; consider Tech Lead first |

---

## 6-Month Skill-Building Plan

### Month 1: iOS Technical Foundation

**Goal**: Shore up any technical gaps. You must be credible with engineers.

**Week 1-2: Swift & Concurrency**
- [ ] Read the Swift book chapters on generics, protocols, concurrency
- [ ] Complete the WWDC sessions: "Meet async/await in Swift", "Protect mutable state with Swift actors"
- [ ] Build a small project using async/await + actors (e.g., a weather app)
- [ ] Watch "Eliminate data races using Swift Concurrency" (WWDC)

**Week 3-4: Architecture**
- [ ] Read "Advanced iOS App Architecture" by Rene Cacheaux (Ray Wenderlich)
- [ ] Refactor a personal project from MVC to MVVM+Coordinator
- [ ] Study TCA: read Point-Free episodes on The Composable Architecture
- [ ] Write an ADR for your architecture decision

**Deliverable**: A GitHub project demonstrating MVVM+Coordinator with async/await networking, Core Data, and 70%+ test coverage.

---

### Month 2: iOS Platform & DevOps

**Goal**: Be able to set up and manage iOS platform infrastructure.

**Week 1-2: Testing**
- [ ] Achieve 80% unit test coverage on your Month 1 project
- [ ] Add UI tests for the critical user flow
- [ ] Add snapshot tests (swift-snapshot-testing) for key screens
- [ ] Set up test coverage reporting

**Week 3-4: CI/CD & DevOps**
- [ ] Set up Fastlane for your project (scan, gym, deliver)
- [ ] Set up GitHub Actions to run tests on every PR
- [ ] Configure code signing with `fastlane match` (if Apple Developer account available)
- [ ] Integrate Crashlytics for crash monitoring

**Deliverable**: GitHub project with full CI/CD pipeline running on every commit.

---

### Month 3: Performance & Advanced iOS

**Goal**: Develop the profiling and optimization skills engineers expect from a strong EM.

**Week 1-2: Instruments & Performance**
- [ ] Profile your Month 1 app with Time Profiler — find and fix one hotspot
- [ ] Profile with Allocations — find a memory inefficiency
- [ ] Implement image caching with 3-tier strategy (memory, disk, network)
- [ ] Measure and optimize app launch time

**Week 3-4: Security & Accessibility**
- [ ] Implement Keychain storage for a credential
- [ ] Implement biometric authentication (TouchID/FaceID) with fallback
- [ ] Add accessibility labels and VoiceOver support to your app
- [ ] Run the accessibility inspector on your app — fix 3 issues

**Deliverable**: A blog post or internal document describing what you found and fixed in each profiling session.

---

### Month 4: Management Fundamentals

**Goal**: Build the people management toolkit.

**Week 1-2: 1:1s and Feedback**
- [ ] Practice 1:1 templates with a peer (role-play)
- [ ] Practice giving SBI feedback (3 scenarios) — record yourself, review
- [ ] Read "Radical Candor" (Kim Scott) — summarize the key model
- [ ] Read "The Manager's Path" (Camille Fournier) — take notes on EM chapter

**Week 3-4: Hiring and Performance**
- [ ] Design a complete iOS engineer interview loop (4 sessions, rubrics for each)
- [ ] Write 5 sample performance reviews for hypothetical engineers at different levels
- [ ] Write a sample PIP for a hypothetical underperforming engineer
- [ ] Write sample OKRs for a hypothetical iOS team for Q1

**Deliverable**: A "Management Toolkit" document with your 1:1 template, feedback frameworks, hiring rubric, and OKR examples.

---

### Month 5: Strategy & Leadership

**Goal**: Think and communicate at the EM level.

**Week 1-2: Technical Strategy**
- [ ] Write a 12-month iOS platform strategy for a hypothetical company (3-5 pages)
- [ ] Create a Technology Radar for iOS tools/libraries
- [ ] Write 5 ADRs for real or hypothetical iOS decisions
- [ ] Read "An Elegant Puzzle" (Will Larson) — focus on systems and processes chapters

**Week 3-4: Data & Metrics**
- [ ] Define a metrics framework for an iOS team (technical + product + team metrics)
- [ ] Design an A/B testing protocol for a mobile feature
- [ ] Create a mock executive dashboard for iOS team health
- [ ] Read "Accelerate" (Nicole Forsgren) — understand DORA metrics deeply

**Deliverable**: iOS Platform Strategy document + metrics framework ready to present to a hypothetical leadership team.

---

### Month 6: Interview Preparation

**Goal**: Translate all your preparation into interview readiness.

**Week 1-2: STAR Stories**
- [ ] Write 20 STAR stories across all 5 behavioral themes
- [ ] Record yourself telling 5 of them — review for clarity, conciseness (aim for 3-4 min each)
- [ ] Get feedback from a peer manager or coach

**Week 3: System Design**
- [ ] Practice 8 mobile system design problems (use the templates in this guide)
- [ ] Present 3 designs to someone and get feedback
- [ ] Time yourself: requirements (5 min), high-level (10 min), deep dive (20 min), trade-offs (5 min)

**Week 4: Mock Interviews**
- [ ] Complete 3 mock technical iOS interviews (use LeetCode iOS problems or real iOS challenges)
- [ ] Complete 5 mock behavioral interviews (use the question bank)
- [ ] Complete 2 full mock EM interview loops (behavioral + system design + technical)

**Deliverable**: Interview-ready with prepared answers for every question in the question bank.

---

## Daily Habits for iOS EM Candidates

### 30 Minutes/Day

| Day | Focus |
|---|---|
| Monday | Read iOS Dev Weekly newsletter — stay current |
| Tuesday | Coding: Swift problem or iOS feature |
| Wednesday | STAR story practice (write or record one) |
| Thursday | Management reading (books, blogs, podcasts) |
| Friday | System design problem (15 min) + reflection |
| Weekend | Project work or deeper reading |

### Weekly

- Review WWDC sessions (1 session/week minimum)
- Follow 5 iOS engineering managers on LinkedIn/Twitter — read their posts
- Post one insight to LinkedIn or Twitter — practice communicating ideas publicly
- Connect with one person in iOS or EM community

### Monthly

- Attend one virtual iOS meetup or conference
- Read one management book chapter
- Write one technical or leadership article (even if unpublished)
- Review and update your STAR story bank

---

## Building Your Portfolio

### GitHub Portfolio Projects

**Project 1: Architecture Showcase**
- MVVM+Coordinator app with real API
- 80%+ test coverage
- CI/CD pipeline
- README documenting architecture decisions

**Project 2: Offline-First App**
- Core Data or SwiftData
- Sync mechanism
- Conflict resolution strategy documented
- Performance metrics in README

**Project 3: iOS SDK**
- Clean public API
- Zero-dependency
- Documentation
- Example app

**Project 4: Open Source Contribution**
- Contribute to a real iOS open-source project
- Even documentation or bug fixes count
- Shows collaboration, code quality in public

### Writing Portfolio

Publish on Medium, LinkedIn, or your own blog:

1. "How we migrated our iOS app to MVVM+Coordinator"
2. "Lessons from optimizing iOS app launch time by 40%"
3. "How I structure 1:1s as an iOS Engineering Manager"
4. "Building a modular iOS architecture for scale"
5. "What I wish I knew before becoming an Engineering Manager"

---

## Resources: Priority Reading Order

### If You Have 1 Month

1. "The Manager's Path" — Camille Fournier (management)
2. "Radical Candor" — Kim Scott (feedback)
3. WWDC: Swift Concurrency sessions (technical)
4. Stanford CS193p: SwiftUI (if SwiftUI gaps)

### If You Have 3 Months

Add:
5. "High Output Management" — Andy Grove
6. "An Elegant Puzzle" — Will Larson
7. "Advanced iOS App Architecture" — Ray Wenderlich
8. Point-Free: TCA episodes
9. "Accelerate" — Nicole Forsgren

### If You Have 6 Months

Add everything above plus:
10. "iOS Unit Testing by Example" — Jon Reid
11. "Designing Data-Intensive Applications" — Martin Kleppmann (backend awareness)
12. "Clean Architecture" — Robert C. Martin
13. "The Five Dysfunctions of a Team" — Patrick Lencioni
14. "Drive" — Daniel Pink
15. "Crucial Conversations" — Patterson et al.

---

## Tracking Your Progress

### Weekly Check-In Template

```markdown
## Week [N] Progress Check

### iOS Technical
- What I practiced: 
- Key insight gained: 
- Gap still remaining: 

### Management Skills
- What I practiced: 
- Key insight gained: 
- Gap still remaining: 

### Interview Prep
- STAR stories written this week: 
- System designs practiced: 
- Mock interviews done: 

### Next Week Priority
1. 
2. 
3. 
```

### Monthly Milestone Review

Score yourself again on the self-assessment table at the start of each month. You should see improvement in your targeted areas. If not:
- Was the practice deliberate? (targeted toward weakness, with feedback)
- Was it enough? (30+ min/day)
- Do you need a different resource or approach?

---

## Signs You're Ready to Apply

**Technical:**
- [ ] You can explain any iOS topic in the README at a solid level
- [ ] You've built 2-3 iOS projects demonstrating architectural thinking
- [ ] You can profile an app and identify performance issues confidently
- [ ] You can design a system design answer end-to-end in 40 minutes

**Management:**
- [ ] You have 20+ STAR stories prepared and practiced
- [ ] You can answer every question in the interview question bank
- [ ] You've completed 5+ mock behavioral interviews
- [ ] You have clear, quantified examples of team impact

**Mindset:**
- [ ] You can articulate "why management" authentically and convincingly
- [ ] You understand the company's iOS products deeply
- [ ] You have genuine enthusiasm for helping others grow
- [ ] You can discuss your management philosophy coherently
