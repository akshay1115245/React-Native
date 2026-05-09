# Engineering Manager Playbook: People, Process & Leadership

> Practical frameworks, templates, and tactics for day-to-day engineering management.

---

## The EM Operating System

Think of your role as running a system with three layers:

```
┌─────────────────────────────────────┐
│          STRATEGY LAYER             │ ← Vision, Roadmap, OKRs
├─────────────────────────────────────┤
│         PEOPLE LAYER                │ ← 1:1s, Growth, Hiring, Culture
├─────────────────────────────────────┤
│         EXECUTION LAYER             │ ← Delivery, Quality, Process
└─────────────────────────────────────┘
```

A great EM keeps all three layers healthy simultaneously. When one breaks down, the whole system degrades.

---

## 1:1 Mastery

### The 1:1 Is Not a Status Update

Status is asynchronous (Slack, Jira, email). The 1:1 is for:
- **Trust building**: the relationship is the foundation of everything
- **Coaching**: help them grow, unblock, think through problems
- **Feedback**: both directions
- **Early signals**: catch burnout, conflict, and confusion early
- **Career**: understand their aspirations and help them get there

### 1:1 Agenda Template

```markdown
## 1:1 - [Name] - [Date]

### Their Agenda (engineer fills before meeting)
- 

### Manager Agenda
- 

### Standing Items (rotate weekly)
Week 1: Career goals and growth
Week 2: Team/project health check
Week 3: Feedback exchange
Week 4: Longer-term aspirations

### Action Items (carry forward)
- [ ] 
- [ ] 

### Notes
```

### Discovery Questions for New Direct Reports

Use these in the first 2-4 weeks:
- "What's the best thing about working here that you'd never want to change?"
- "What's the one thing that drives you most crazy about how the team works?"
- "When have you felt most proud of your work in this team?"
- "What does your ideal working relationship with a manager look like?"
- "What are you hoping to get better at in the next year?"
- "Is there anything about the team dynamics I should know about?"
- "What would make you consider leaving this team?"
- "If you were the EM, what would you do differently?"

### Warning Signs in 1:1s

| Signal | Possible Meaning |
|---|---|
| Engineer cancels repeatedly | Disengagement, or too busy (overloaded) |
| Only short, surface answers | Low trust, defensive |
| Complaining without proposing | Frustration building |
| "Everything is fine" always | Not psychologically safe enough to share |
| Energy drop from previous meetings | Something happened — ask |
| Talking about other jobs/companies | Retention risk — explore motivators |

---

## Career Development Framework

### Career Conversation Structure (3 Conversations)

Based on Russ Laraway's "Career Conversations" model:

**Conversation 1: Life Story**
- "Tell me about your life from childhood to now — the significant choices and experiences."
- Goal: understand their values, what drives them, how they make decisions
- Not about work — about the person

**Conversation 2: Dreams**
- "What's your ultimate dream — even if it seems impossible?"
- Explore multiple options: "What else? What else?"
- Goal: understand where they genuinely want to go
- Not yet about what they should do — about inspiration

**Conversation 3: 18-Month Plan**
- Connect life story + dreams to immediate priorities
- What skills do they need to develop?
- What roles/projects will accelerate growth?
- What does success look like in 18 months?

### Growth Plan Template

```markdown
## Growth Plan: [Engineer Name]
## Period: Q3 2024 – Q4 2024

### Current Level: iOS Engineer II
### Target: iOS Engineer III (promotion-ready by end of period)

### Promotion Criteria (company rubric)
- Technical: leads feature design, mentors junior engineers, drives architecture decisions
- Execution: delivers complex projects with minimal guidance
- Impact: work influences beyond immediate team

### Gap Analysis
| Area | Current State | Target State |
|---|---|---|
| System Design | Designs components | Designs features/systems |
| Mentorship | None yet | Actively mentoring 1 junior |
| Initiative | Waits for direction | Identifies and drives improvements |
| Scope | Feature-level | Cross-team collaboration |

### Development Actions (This Quarter)
1. **Lead the offline sync feature** — own design, execution, and stakeholder communication
2. **Mentor [Junior Engineer]** — weekly pair sessions, code reviews
3. **Present at team tech talk** — pick iOS architecture topic

### Milestones
- Month 1: Feature design doc reviewed and approved
- Month 2: Implementation complete, junior mentorship in progress
- Month 3: Feature shipped, tech talk done, promotion doc drafted

### EM Support
- Introduce to senior engineers in platform team for collaboration
- Include in architecture review sessions
- Provide stretch opportunities in Q4 planning
```

### Promotion Advocacy Script

Use this framework when advocating in calibration sessions:

> "[Name] is ready for [Level N+1]. Here's the evidence:
>
> **Technical impact**: Led the redesign of our offline sync module — reduced data conflicts by 40%, shipped to 100% of users. This was a system-level decision affecting 4 other teams.
>
> **Leadership**: Has been the de facto tech lead for the payments feature for 2 quarters. Brings engineers up-front in design, runs code reviews that catch architectural issues.
>
> **Scope**: Drove adoption of our new testing standards across the mobile team — not just their own work.
>
> This isn't about how long they've been here — they are clearly operating at the next level and have been for 6 months. I'm proposing a promotion."

---

## Hiring: End-to-End Process

### iOS Engineer Interview Loop

**Round 1: Recruiter Screen** (recruiter owns)
- Motivation, logistics, compensation alignment

**Round 2: Technical Phone Screen** (senior engineer)
- 45 min Swift coding: medium-complexity problem
- Focus: code quality, communication, Swift idioms
- Not LeetCode puzzles — real-world iOS problem

**Round 3: Technical Loop** (3-4 sessions)
- Session A: iOS Architecture (design a feature from scratch)
- Session B: Coding / debugging session
- Session C: System Design (mobile system design)
- Session D (optional): Cross-functional / product collaboration

**Round 4: Management Interview** (EM owns)
- Culture fit, values alignment
- Team collaboration, conflict resolution
- Career motivations
- Past project deep-dive

**Round 5: Offer & Close** (recruiter + EM)

### iOS Architecture Interview: Rubric

Question: "Design the iOS app architecture for a news feed with offline support."

| Dimension | Weak | Strong | Exceptional |
|---|---|---|---|
| Requirements | Jumps in | Asks some questions | Clarifies functional + non-functional + constraints |
| Architecture | Names a pattern | Explains pattern + why | Discusses trade-offs of 2-3 options with justification |
| Offline | "Use CoreData" | Explains sync strategy | Discusses conflict resolution, queue, idempotency |
| Performance | Not mentioned | Mentions pagination | Discusses image caching, prefetching, lazy loading |
| Testing | Not mentioned | Mentions unit tests | Explains how architecture enables testing |
| Communication | Unclear | Clear | Draws diagrams proactively, confirms understanding |

### Hiring Debrief Protocol

**After each interview, each interviewer independently submits:**
- Hire / Lean Hire / Lean No Hire / No Hire recommendation
- Evidence: specific quotes, observations, code quality notes
- Key signals for and against

**Debrief meeting (within 24 hours):**
1. Each interviewer shares recommendation without hearing others first (to reduce anchoring)
2. Discuss discrepancies
3. Identify must-have vs. nice-to-have signal gaps
4. Align on decision
5. EM makes final call and communicates to recruiter

### Offer Negotiation Tips for EMs

- Know your compensation band before the debrief
- Understand the candidate's competing offers if possible
- Differentiate your offer: project impact, team quality, growth opportunities
- Don't create false urgency — builds resentment
- Be willing to walk away if compensation expectations don't align

---

## Delivering Difficult Feedback

### SBI Framework in Practice

**Situation-Behavior-Impact:**

| Bad Feedback | Good Feedback (SBI) |
|---|---|
| "You're too aggressive in meetings" | "In yesterday's architecture review (S), you interrupted Maria three times before she finished her point (B). She stopped contributing after that, and we may have missed her perspective (I)." |
| "Your code quality is bad" | "In last week's PR (S), there were no unit tests for the payment flow (B). This led to a P1 bug in production that took 4 hours to debug (I)." |
| "You need to communicate better" | "During the sprint (S), you didn't update the Jira tickets or Slack the team about your blocker for 3 days (B). The backend team built an API assuming wrong params and had to rework it (I)." |

### Radical Candor Quadrant

```
                    Challenge Directly
                           ↑
           Obnoxious     │    Radical
           Aggression    │    Candor
                         │
Care  ←─────────────────┼─────────────────→ Care
Personally               │              Personally
(low)                    │              (high)
                         │
         Manipulative    │    Ruinous
         Insincerity     │    Empathy
                         ↓
                    Don't Challenge Directly
```

**Ruinous Empathy** (most common EM failure): You care but don't say the hard truth. Engineer suffers long-term.

**Obnoxious Aggression**: You challenge but don't care. Technically right, relationally damaging.

**Manipulative Insincerity**: You don't care and don't say it. Toxic.

**Radical Candor**: You genuinely care AND tell the truth. The goal.

### Feedback Delivery Script Templates

**Positive reinforcement:**
> "I want to call out something specific. In the sprint planning yesterday, you pushed back on adding three more stories by pointing to the team's actual velocity data. That was exactly right, and it helped us protect the team's capacity. I want you to keep doing that."

**Constructive (first time):**
> "I want to share something I noticed. [SBI]. I'm telling you this because I want you to succeed here, and I think this is holding you back. What's your take on what happened?"

**Escalation (pattern persisting):**
> "We've talked about [behavior] before, on [dates]. I'm concerned because I'm still seeing it. I want to talk about a plan together — not as punishment, but because I need to see change, and I want to support you in making it. If things don't improve by [timeframe], we'll need to involve HR in a more formal process."

---

## Managing Underperformance

### Performance Issue Lifecycle

```
Early Signal → Informal Coaching → Documented Coaching → PIP → Exit or Recovery
    |               |                    |                |         |
  Weeks          Weeks-Months         1-3 months      30-90 days  Outcome
```

**Rule**: Never surprise an engineer with a PIP. They should have had multiple conversations before it.

### PIP Structure

```markdown
## Performance Improvement Plan
## Engineer: [Name] | Manager: [Your Name] | Date: [Date]

### Background
[2-3 sentences describing what led to this PIP, referencing prior coaching conversations]

### Areas of Concern
1. **Code Quality**: In the last 3 sprints, [Name] has introduced 7 P2 bugs that escaped to production. The team average is 1-2. [Link to specific examples]
2. **Delivery**: [Name] has missed the agreed-upon sprint commitments in 4 of the last 5 sprints without proactively raising blockers. [Link to sprint data]
3. **Communication**: [Name] has not updated task status in Jira for 3+ days on 6 occasions in the past month, causing planning issues for dependent teams.

### Success Criteria (30-Day Goals)
1. Zero P2+ bugs escaping to production originating from [Name]'s code
2. Communicate blockers within 1 business day of identification
3. Keep Jira task status current with daily updates
4. Achieve code review approval without major revision requests

### Support Plan
- Weekly 1:1 check-ins focused on PIP progress (30 min extra)
- Pair programming sessions with [Senior Engineer] twice per week
- Manager will review every PR before submission during PIP period

### Checkpoints
- Week 2 check-in: [Date]
- Week 4 final review: [Date]

### Consequences
If the success criteria are not met by [Date], [Company] will proceed with a formal separation process.
```

---

## Incident Management Playbook

### Severity Definitions

| Level | Impact | Response Time | Examples |
|---|---|---|---|
| P0 | All users affected, revenue/data loss | Immediate | App crashes on launch, payment failure |
| P1 | Significant % affected, major feature down | < 15 min | Login broken, feed not loading |
| P2 | Partial impact, degraded performance | < 1 hour | Slow load times, image failures |
| P3 | Minor, workaround available | < 4 hours | UI bug, minor feature broken |
| P4 | Negligible impact | Sprint backlog | Cosmetic issues |

### Incident Response Checklist (iOS-Specific)

**Immediate (0–15 min):**
- [ ] Acknowledge the incident in incident channel
- [ ] Check Crashlytics / Sentry for crash rate trend
- [ ] Check App Store Connect for user reviews spiking
- [ ] Check server error rates (is it backend or iOS?)
- [ ] Identify affected iOS version range and device types
- [ ] Assign Incident Commander (IC)

**Mitigation (15–60 min):**
- [ ] If crash in new release: initiate App Store version halt (if phased release)
- [ ] If backend-triggered: coordinate with backend team
- [ ] Enable/disable feature flag if applicable
- [ ] Push emergency fix if code issue — expedited review process?
- [ ] Communicate status to stakeholders every 15-30 min

**Resolution:**
- [ ] Confirm metrics returning to normal
- [ ] Send resolution notice to stakeholders
- [ ] Schedule post-mortem within 5 business days

### Blameless Post-Mortem Template

```markdown
## Incident Post-Mortem
### Incident: [Name/ID]
### Date: [Date] | Severity: P[N]
### Duration: [Start] – [End] | Total Impact: [X] hours / [Y]% of users

---

### Timeline
| Time | Event |
|---|---|
| 14:03 | First alert triggered — crash rate exceeded 2% |
| 14:07 | On-call engineer acknowledged |
| 14:22 | Root cause identified: nil force-unwrap in payment parser |
| 14:40 | Fix deployed via feature flag |
| 15:10 | Crash rate returned to baseline |

---

### Impact
- Users affected: ~120,000 (12% of DAU)
- Failed payment attempts: ~8,400
- Estimated revenue impact: $42,000
- App Store rating drop: 4.6 → 4.1 (recovered in 2 weeks)

---

### Root Cause
A force-unwrap `!` on an optional `currencyCode` field in the payment response parser. The backend team deployed a change that omitted this field for non-US users. The iOS app crashed on any payment attempt for non-US users after the backend deploy.

---

### Why Did This Happen? (Five Whys)
1. Why did the app crash? → Force-unwrap on nil value
2. Why was there a force-unwrap? → Developer assumed field always present per contract
3. Why was assumption wrong? → Backend team made a breaking API change without notice
4. Why wasn't this caught in testing? → API contract testing was not in place
5. Why no API contract testing? → Never prioritized in the roadmap

---

### What Went Well
- On-call response was fast (4 min acknowledgement)
- Feature flag rollback was executed cleanly
- Cross-team communication was effective

---

### Action Items
| Action | Owner | Due Date |
|---|---|---|
| Replace all force-unwrap in network models with safe handling | iOS Team | 1 week |
| Implement Pact contract testing for payment API | iOS + Backend | 3 weeks |
| Add crash rate alert threshold for payment flow | Platform | 1 week |
| Establish breaking change communication protocol with backend | EM | 2 weeks |
| Add non-US payment coverage to UI test suite | QA | 2 weeks |
```

---

## Team Health & Culture

### Team Health Survey Questions (Run Quarterly)

Rate 1-5 (Strongly Disagree → Strongly Agree):

**Psychological Safety**
1. I feel safe to speak up about problems and concerns on this team.
2. I can take risks on this team without feeling afraid of failure.
3. Members of this team never reject others for being different.

**Clarity**
4. I understand what's expected of me in my role.
5. I know what our team's goals are for this quarter.
6. I understand how my work connects to the company's mission.

**Autonomy**
7. I have enough autonomy to make decisions about my work.
8. My manager trusts me to do my job without micromanaging.

**Growth**
9. I have opportunities to learn and grow at this company.
10. My manager actively supports my career development.

**Collaboration**
11. People on this team cooperate to get things done.
12. We have effective processes for working together.

**Recognition**
13. My contributions are recognized and valued.
14. I know what it takes to grow and advance on this team.

**Overall**
15. I would recommend this team to a friend as a great place to work.

### Interpreting Results

- **4.0–5.0**: Healthy — focus on maintenance and growth
- **3.0–3.9**: Attention needed — investigate specific low areas
- **Below 3.0**: Critical — immediate action required, leadership escalation

### Building Psychological Safety (Practical Actions)

1. **Model vulnerability**: "I made a mistake in that decision. Here's what I learned."
2. **Publicly praise learning, not just results**: "Sarah tried something that didn't work, but we all learned X from it."
3. **Punish silence, not failure**: Ask quiet people for their view; reward dissent.
4. **Separate investigation from blame in incidents**: Post-mortems are about systems, not people.
5. **React to bad news graciously**: If you react with anger to problems being surfaced, people will stop surfacing them.

---

## Working With Your Manager

### Managing Up: What Your Manager Needs From You

1. **No surprises**: Surface problems early. "I think the Q3 launch is at risk because X" is always better than a missed launch.
2. **Framed asks**: Don't bring problems without framing your proposed solution.
3. **Visibility**: Keep them informed at the right level of detail (not too deep, not too abstract).
4. **Your priorities**: They can't calibrate your headcount or resources if they don't know what matters to you.
5. **Team wins**: Make your team's work visible to leadership.

### Skip-Level Relationship

Your skip-level (your manager's manager) should:
- Know who your strong performers are
- Know your team's key initiatives
- Trust that your team is healthy and executing

How to build the relationship:
- Ask your manager if occasional skip-levels are appropriate
- Send brief monthly written updates up the chain
- Invite skip-level to relevant demos

### Disagreeing With Your Manager

**When to push back:**
- You have data or context they don't
- The decision affects your team's safety, morale, or ethics
- You have domain expertise that changes the analysis

**How to push back well:**
1. Understand their reasoning first (don't assume)
2. Present your disagreement privately, not publicly
3. Use data, not opinion
4. Accept the final decision if overruled — disagree and commit
5. Know when to escalate (rare): ethics violations, legal concerns

---

## Communication Templates

### Project Status Update (Weekly)

```markdown
## iOS Team Status Update — Week of [Date]

### 🟢 On Track
- [Feature A]: On track for [Date] release. 80% complete.
- [Feature B]: Design finalized, implementation started.

### 🟡 At Risk
- [Feature C]: Backend API delay may impact our timeline. Mitigation: we're parallelizing UI work with mock data. Expect 1-week impact if not resolved by Friday.

### 🔴 Off Track
- [Feature D]: Descoped from Q3 to Q4. Root cause: underestimated complexity of offline sync. Stakeholders aligned.

### Key Wins This Week
- Crash-free rate improved from 99.1% → 99.6% after the memory leak fix
- Hired [Name] — starting [Date]

### Needs Attention / Decisions Required
- Need PM alignment on [Feature E] priority before sprint planning Monday

### Key Metrics
| Metric | Current | Target | Trend |
|---|---|---|---|
| Crash-free rate | 99.6% | >99.5% | ↑ |
| App launch time (P50) | 1.2s | <1.5s | → |
| Build time | 4.2 min | <5 min | → |
| Sprint velocity | 42 pts | 40 pts | ↑ |
```

### Escalation Message Template

```markdown
**ESCALATION: [Brief Description]**

**Current Impact**: [What is happening, how many users affected, business impact]

**Root Cause**: [Known/unknown — what you know so far]

**Actions Taken**: [What has been done]

**What I Need**: [Specific ask — decision, resource, approval, visibility]

**Timeline**: [When decision is needed]

**Owner**: [Who is responsible for next action]
```
