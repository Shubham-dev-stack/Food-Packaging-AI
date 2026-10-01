# Engineering & Scientific Rules for Implementation

**Document Type:** Project Guardrails & Coding Standards  
**Problem Statement ID:** SIH26236  
**Primary Source:** [docs/Problem_Statement.md](file:///d:/Food-Packaging-AI/docs/Problem_Statement.md)  
**Playbook Reference:** [docs/SaaS_Playbook_Reference.md](file:///d:/Food-Packaging-AI/docs/SaaS_Playbook_Reference.md)  
**Memory & State:** [docs/Memory.md](file:///d:/Food-Packaging-AI/docs/Memory.md)  

---

## 1. Scientific & Domain Integrity Guardrails

1. **Never Invent Scientific Data:** Under no circumstances may an engineer or AI assistant fabricate barrier numbers (OTR, WVTR), respiration rates ($R$), critical water activities ($a_w$), or gas compositions.
2. **Mandatory Citation for Numerical Inputs:** Every baseline threshold added to the knowledge base must possess a valid `reference_id` linking to an authoritative source in `EvidenceSource` (e.g. USDA, ASTM, Robertson 2012).
3. **No Unvalidated Metric Claims:** Do not claim commercial shelf-life extension percentages, exact food waste reduction numbers, or model accuracy metrics. Mark unvalidated figures as **TBD**.
4. **Preserve Source Hierarchy:**
   - Level 1: `docs/Problem_Statement.md` (Primary product truth).
   - Level 2: `docs/Research_and_Evidence.md` (Scientific foundation).
   - Level 3: `docs/SaaS_Playbook_Reference.md` (Engineering methodology).
   - Level 4: Project Assumptions (must be explicitly tagged `[PROTOTYPE ASSUMPTION]`).
5. **Enforce Contextual Food Safety Advisories:** Never allow low-acid foods ($pH \ge 4.6$) in reduced-oxygen or anaerobic packaging formats to be recommended without attaching the contextual Reduced-Oxygen Packaging (ROP) safety advisory, and avoid claiming certified commercial food safety without licensed process validation.

---

## 2. Architectural & Code Discipline

1. **Modular Monolith Architecture:** Keep all code within a clean modular structure. Do not introduce microservices, distributed queues, or remote service meshes.
2. **Server as Source of Truth:** All physical validation, barrier matching, candidate filtering, and ranking must execute in `backend/app/domain/` or `backend/app/services/`. Frontend code is strictly for presentation and form interaction.
3. **Decoupled Business Logic:** Business and physics logic must not live inside UI components or API route handlers. Route handlers stay thin; domain logic resides in dedicated services.
4. **Dependency Discipline:** Do not install external libraries without justification. Avoid adding duplicate libraries (e.g. multiple HTTP clients or state libraries).
5. **No Premature Optimization:** Avoid complex caching layers (Redis) or distributed message buses for datasets that fit comfortably in indexed relational memory.

---

## 3. Security & Secrets Management

1. **Zero Committed Secrets:** Never commit passwords, tokens, API keys, or credentials to version control.
2. **Environment Variable Configuration:** All runtime configurations must load from `.env`, accompanied by a fully documented `.env.example`.
3. **Parameterized Queries Only:** All database interactions must use SQLAlchemy ORM or parameterized SQL to eliminate SQL injection vulnerabilities.
4. **Sanitized Input Boundaries:** Every API route must validate requests using Pydantic schemas, enforcing strict types and physical bounds before processing.
5. **Error Message Redaction:** Never leak internal stack traces, system paths, or raw database errors to the client.

---

## 4. Testing & Verification Discipline

1. **Never Edit a Test to Pass:** If a test fails, the bug is in the application logic. Fixing code by weakening test assertions is strictly forbidden.
2. **No Mocking Business Logic:** Unit tests for food physics, barrier calculation, and candidate ranking must execute real mathematical calculations against benchmark fixtures, not mock return values.
3. **The Universal "Don't Fool Me" Verification Standard:**
   Before declaring any implementation task complete:
   - Run the full test suite and inspect real terminal output.
   - List every file modified and explain why.
   - List anything stubbed, mocked, or hardcoded.
   - State any assumptions requiring human confirmation.
4. **Edge Case Test Coverage:** Test suites must explicitly cover physically impossible inputs, out-of-range temperatures, respiring vs non-respiring crops, and high-fat oxidation thresholds.

---

## 5. Development Workflow & Decision Logging

1. **Small, Focused Diffs:** Implement one phase and one feature at a time on dedicated git branches. Avoid sprawling multi-feature commits.
2. **Mandatory Decision Recording:** Any major architectural adjustment, schema modification, or scientific assumption must be immediately logged in [docs/Memory.md](file:///d:/Food-Packaging-AI/docs/Memory.md) with context, rationale, and consequences.
3. **Verification Before PR/Merge:** Every task must pass linting, typechecking, and unit tests before merging into `main`.
