# SaaS Playbook Reference & Engineering Discipline

> **Source**: Adapted from `reference/vibe-coding-real-saas-playbook.pdf` (*Vibe Coding a Real SaaS: The 15-Layer Playbook*) for the **SIH 2026 Problem Statement SIH26236** (*AI-Based Intelligent Food Packaging Material Recommendation System for Food Commodities*).

---

## 1. Core Engineering Philosophy & Golden Rules

Agentic coding fails when agents optimize for *"it runs on my machine"* or jump straight into generating speculative code without context, memory, or architectural boundaries. This playbook establishes engineering discipline so that AI assistants act as disciplined builders while the human developer acts as the system architect.

### The 10 Golden Rules
1. **You are the architect; the agent is the builder.** Decide first, then delegate.
2. **Plan before code, every time.** Fixing a design or plan is cheap; rewriting broken code is expensive.
3. **Write it down.** `CLAUDE.md` and `/docs/` are the system memory. Without them, every new session starts from zero and makes conflicting choices.
4. **Small tasks, small diffs.** One feature per branch, one concern per commit.
5. **The agent must prove it works.** Run tests, typechecks, linters, and display actual output before claiming completion.
6. **Never edit a test to make it pass.** If a test exposes a bug, fix the application logic—never dilute test assertions.
7. **Review with a fresh pair of eyes.** Use fresh sessions or dedicated reviewer agents for objective code and security scrutiny.
8. **Server is the source of truth.** All validation, domain rules, permissions, and calculations must execute securely on the backend.
9. **Scoped data queries.** Ensure database queries are explicit, properly filtered, and validated.
10. **Read the diff.** Never merge changes that cannot be explained or justified.

---

## 2. The Core Agent Workflow Loop

Every layer and feature in this project must follow the 5-step operational loop:

```
[ Plan First ] ➔ [ Review Plan ] ➔ [ Implement in Small Steps ] ➔ [ Verify Work ] ➔ [ Record Decision ]
```

1. **Plan First**: Draft explicit requirements, data contracts, and edge cases in `/docs/` before writing code.
2. **Review the Plan**: Evaluate trade-offs, identify missing constraints, and reject unnecessary over-engineering.
3. **Implement in Small Steps**: Work on dedicated branches with minimal, focused changes.
4. **Verify Work**: Run test suites, verify domain constraints, check boundary cases, and show real execution outputs.
5. **Record Decision**: Update `CLAUDE.md` and appropriate `/docs/` files with any design decisions, rationale, or known constraints.

### The "Don't Fool Me" Verification Standard
Before any implementation task is marked complete:
- Run all test suites, typechecks, and linters, and inspect the real output.
- Enumerate every file modified and explain why.
- Explicitly list anything skipped, stubbed, mocked, or hard-coded.
- Clearly state any assumptions that require human confirmation.
- Never declare a task complete if tests are failing, skipped, or mock-only.

---

## 3. The 15 Layers: SIH Project Classification

The playbook emphasizes that an early prototype must avoid premature over-engineering (e.g., microservices, distributed queues, or complex multi-tenant billing on day one). Below is the classification of all 15 layers specifically tailored for the **SIH 2026 Food Packaging Recommendation System**:

| # | Layer | Build Phase | SIH 2026 Classification | Justification & Prototype Guidance |
|---|-------|-------------|-------------------------|------------------------------------|
| 1 | **System Design** | Plan | **REQUIRED FOR MVP** | Essential to define food commodities, user inputs, packaging outputs, target personas (farmers, startups, industries), and out-of-scope items before coding. |
| 2 | **System Architecture** | Plan | **REQUIRED FOR MVP** | Modular monolith design separating domain recommendation logic, mathematical/barrier models, data persistence, and UI. Low operational burden. |
| 3 | **Databases & Storage** | Foundation | **REQUIRED FOR MVP** | Structured schema for food commodity characteristics, packaging materials, and barrier properties. Migrations must be version-controlled. Complex multi-tenant isolation is *Useful Later*. |
| 4 | **Auth & Permissions** | Foundation | **NOT CURRENTLY NECESSARY** / **USEFUL LATER** | The SIH problem statement describes an expert decision-support tool. An open public/research demo is standard for hackathon evaluation. Auth can be added if personalized accounts/saving recommendations are needed. |
| 5 | **APIs & Backend Logic** | Foundation | **REQUIRED FOR MVP** | Core recommendation engine endpoints, input validation (e.g. Pydantic schemas for moisture, pH, OTR, WVTR), clean error responses, and deterministic calculation services. (Payment/webhooks: *Not Currently Necessary*). |
| 6 | **Frontend** | Product | **REQUIRED FOR MVP** | Responsive, accessible interface for inputting food parameters (sliders, selectors, storage conditions) and displaying detailed material recommendations, barrier specs, and explanations. |
| 7 | **CI/CD & Version Control** | Ship | **REQUIRED FOR MVP** | Clean Git hygiene, feature branches, descriptive commit messages, and basic GitHub Actions running automated test suites on push. |
| 8 | **Testing** | Ship | **REQUIRED FOR MVP** | Comprehensive unit tests for recommendation logic, barrier calculations, respiration/MAP formulas, and boundary validations. No mocked business logic. |
| 9 | **Hosting & Cloud** | Ship | **REQUIRED FOR MVP** (Simple) | Simple single-platform deployment (e.g. Render, Railway, Vercel) for live evaluation. Avoid complex cloud orchestration like Kubernetes or multi-region setups. |
| 10 | **Security** | Harden | **REQUIRED FOR MVP** (Basic) | Strict server-side input sanitization, dependency vulnerability auditing, and prevention of injection attacks. Enterprise penetration testing is *Useful Later*. |
| 11 | **Rate Limiting** | Harden | **ONLY IF THE ARCHITECTURE REQUIRES IT** | Only necessary if external paid LLM APIs are invoked for explanations or to prevent denial-of-service on public demonstration endpoints. |
| 12 | **Caching & CDN** | Harden | **NOT CURRENTLY NECESSARY** | Commodity and material dataset size is compact and easily handled in-memory or via standard indexed DB queries. Caching layers add premature operational complexity. |
| 13 | **Error Tracking & Logs** | Operate | **REQUIRED FOR MVP** (Standard) | Structured logging for backend calculation errors and recommendation mismatches. External Sentry integration is *Useful Later*. |
| 14 | **Monitoring & Alerts** | Operate | **USEFUL LATER** | A standard health-check endpoint (`/api/health`) is required for deployment verification. Complex alerting and 24/7 runbooks are *Not Currently Necessary* for prototype phase. |
| 15 | **Scaling** | Grow | **NOT CURRENTLY NECESSARY** | Optimization for millions of concurrent users is out of scope for the SIH prototype. Focus entirely on recommendation accuracy, domain validity, and code cleanliness. |

---

## 4. Key Agent Blind Spots to Guard Against

1. **Jumping straight to code:** Agents default to writing code before defining requirements or validating food science constraints.
2. **Inventing scientific facts & thresholds:** Agents hallucinate polymer barrier numbers, respiration rates, or shelf-life values when datasets are missing.
3. **Over-engineering infrastructure:** Agents introduce microservices, distributed caching, or complex auth systems when a simple modular service suffices.
4. **Testing mocks instead of reality:** Writing tests that pass because the mock passes, rather than validating real calculations against scientific benchmark data.
5. **Silently moving project scope:** Agents add bells and whistles (e.g., social login, payment gateways) that distract from the primary SIH problem statement.
