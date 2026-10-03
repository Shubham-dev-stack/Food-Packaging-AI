# Implementation Phases: AI Food Packaging Recommendation System

**Document Type:** Phased Engineering Roadmap  
**Problem Statement ID:** SIH26236  
**Primary Source:** [docs/Problem_Statement.md](file:///d:/Food-Packaging-AI/docs/Problem_Statement.md)  
**System Architecture:** [docs/Architecture.md](file:///d:/Food-Packaging-AI/docs/Architecture.md)  
**Rules & Discipline:** [docs/Rules.md](file:///d:/Food-Packaging-AI/docs/Rules.md)  
**Memory & State:** [docs/Memory.md](file:///d:/Food-Packaging-AI/docs/Memory.md)  

---

## 1. Roadmap Overview & Sequencing

The implementation follows a strict **bottom-up, domain-first sequence**. The domain physics and data foundation are built and verified before API routes or UI screens are implemented.

```mermaid
flowchart LR
    P0[Phase 0: Foundation] --> P1[Phase 1: Data Models]
    P1 --> P2[Phase 2: Physics Engine]
    P2 --> P3[Phase 3: Backend API]
    P3 --> P4[Phase 4: Frontend Core]
    P4 --> P5[Phase 5: Results UI]
    P5 --> P6[Phase 6: Explainability]
    P6 --> P7[Phase 7: Produce & MAP]
    P7 --> P8[Phase 8: E2E Testing]
    P8 --> P9[Phase 9: Hardening]
    P9 --> P10[Phase 10: Deployment]
    P10 --> P11[Phase 11: Demo Polish]
    P11 --> P12[Phase 12: Project Freeze]
```

---

## 2. Phase-by-Phase Specifications

### Phase 0: Project Foundation & Tooling
- **Objective:** Establish repo scaffolding, runtime environments, linters, formatters, and git hygiene.
- **Prerequisites:** Approved documentation foundation.
- **Deliverables:**
  - Python virtual environment setup with `requirements.txt` (FastAPI, Pydantic, SQLAlchemy, Pytest).
  - Node.js frontend workspace setup (`package.json`, Vite, React, TypeScript, Tailwind CSS).
  - Pre-commit configuration, `.gitignore`, and `.env.example`.
- **Expected Files:** `backend/requirements.txt`, `frontend/package.json`, `.gitignore`, `.env.example`.
- **Verification:** Run `pytest` and `npm run build` demonstrating zero errors in empty harness.
- **Definition of Done:** Both backend and frontend development servers boot with working health checks.
- **Excluded Work:** No database tables or application logic.

---

### Phase 1: Data Foundation & Curated Knowledge Base
- **Objective:** Implement relational data models and ingest verified benchmark datasets with citations.
- **Prerequisites:** Phase 0 complete; [docs/Data_Model.md](file:///d:/Food-Packaging-AI/docs/Data_Model.md).
- **Deliverables:**
  - SQLAlchemy models for `EvidenceSource`, `Commodity`, `CommodityProperty`, `ProduceRespirationData`, `PackagingMaterial`, `PackagingBarrierProperty`, `MAPConfiguration`, `SustainabilityMetric`, and `CostIndex`.
  - JSON seed fixtures in `data/processed/` containing 25+ benchmark commodities and 15+ packaging materials.
  - Database initialization script creating local SQLite instance with complete foreign-key integrity.
- **Expected Files:** `backend/app/models/*.py`, `backend/app/repositories/*.py`, `data/processed/*.json`, `backend/app/core/db.py`.
- **Verification:** Automated seed test verifying all fixtures load without schema or foreign-key violations.
- **Definition of Done:** Database seeds successfully and passes query integration tests.
- **Excluded Work:** Recommendation or filtering logic.

---

### Phase 2: Domain Physics & Recommendation Engine
- **Objective:** Build pure, deterministic food preservation and barrier calculation algorithms.
- **Prerequisites:** Phase 1 complete; [docs/AI_Recommendation_Engine.md](file:///d:/Food-Packaging-AI/docs/AI_Recommendation_Engine.md).
- **Deliverables:**
  - Mass transfer module calculating vapor pressure gradients ($\Delta p_w$) and maximum allowable WVTR.
  - Oxygen sensitivity module calculating OTR cutoffs and light barrier requirements.
  - Produce respiration module with $Q_{10}$ temperature scaling and micro-perforation checks.
  - Constraint filtering and multi-attribute utility ranking service ($S_{\text{barrier}}, S_{\text{sustainability}}, S_{\text{cost}}$).
  - Pathogen and botulism safety guardrail rules.
- **Expected Files:** `backend/app/domain/physics.py`, `backend/app/domain/respiration.py`, `backend/app/services/recommendation.py`.
- **Verification:** 100% test pass rate on unit tests against benchmark food items (chips, broccoli, powders).
- **Definition of Done:** Domain services return mathematically verified recommendations for all test cases.
- **Excluded Work:** HTTP endpoints or Web UI.

---

### Phase 3: Backend REST API Gateway
- **Objective:** Expose the recommendation engine via a secure, validated FastAPI interface.
- **Prerequisites:** Phase 2 complete; [docs/Architecture.md](file:///d:/Food-Packaging-AI/docs/Architecture.md).
- **Deliverables:**
  - Pydantic request/response schemas matching `docs/Data_Model.md`.
  - Endpoints: `GET /api/commodities`, `GET /api/commodities/{id}`, `POST /api/recommendations`, `GET /api/health`.
  - Input validation middleware and global exception handler redacting raw tracebacks.
- **Expected Files:** `backend/app/api/v1/*.py`, `backend/app/schemas/*.py`, `backend/app/main.py`.
- **Verification:** API integration tests using `pytest` and FastAPI `TestClient`, checking 200 OK and 400 Bad Request on invalid inputs.
- **Definition of Done:** All endpoints functional and documented via interactive Swagger UI (`/docs`).
- **Excluded Work:** Frontend integration.

---

### Phase 4: Frontend Core & Input Workspace
- **Objective:** Build responsive user interface for commodity selection and parameter configuration.
- **Prerequisites:** Phase 3 complete; [docs/Design.md](file:///d:/Food-Packaging-AI/docs/Design.md).
- **Deliverables:**
  - Split-screen layout (40% Input Workspace, 60% Dashboard).
  - Commodity search/filter dropdown with auto-populated baseline preview.
  - Sliders for moisture %, fat %, pH, temperature, and relative humidity with numerical feedback.
  - Client-side validation hooks matching backend rules.
- **Expected Files:** `frontend/src/components/inputs/*.tsx`, `frontend/src/pages/Workspace.tsx`.
- **Verification:** Form validates inputs, displays baseline previews, and emits structured payload.
- **Definition of Done:** User can select a commodity, tweak parameters, and trigger evaluation.
- **Excluded Work:** Results rendering.

---

### Phase 5: Recommendation Experience & Technical Specifications Grid
- **Objective:** Render primary recommendation, alternatives, and technical specifications grid.
- **Prerequisites:** Phase 4 complete.
- **Deliverables:**
  - Primary Material Banner with trade code, structure, and suitability status.
  - Technical Specifications Grid: Cards for OTR, WVTR, Thickness, Sealability, Permeability, and Strength.
  - Alternative / Recyclable Material comparison card.
  - Interactive tooltips explaining ASTM standards (ASTM D3985, ASTM F1249).
- **Expected Files:** `frontend/src/components/results/*.tsx`, `frontend/src/components/specs/*.tsx`.
- **Verification:** UI accurately displays specifications and ASTM units returned from the backend.
- **Definition of Done:** Results dashboard updates seamlessly upon submission without page reload.
- **Excluded Work:** Produce MAP-specific cards.

---

### Phase 6: Explainability & Evidence Traceability
- **Objective:** Build transparent Explanation Cards, disqualification logs, and citations modal.
- **Prerequisites:** Phase 5 complete.
- **Deliverables:**
  - Explanation Card detailing the primary degradation driver and environmental impact.
  - Expandable Disqualification Log displaying why alternative polymers failed.
  - Evidence Library modal displaying bibliographic reference metadata for underlying claims.
  - Critical safety alert banner for low-acid anaerobic packaging.
- **Expected Files:** `frontend/src/components/explainability/*.tsx`, `frontend/src/components/evidence/*.tsx`.
- **Verification:** Every test recommendation displays a coherent explanation card linking to real citations.
- **Definition of Done:** Non-specialist users can read why the system selected the material.

---

### Phase 7: Fresh Produce & MAP Experience
- **Objective:** Implement specialized respiration and modified atmosphere views for produce.
- **Prerequisites:** Phase 6 complete.
- **Deliverables:**
  - Dynamic switching to produce respiration mode when respiring crop is selected.
  - Headspace gas target meters ($\% \text{O}_2, \% \text{CO}_2, \% \text{N}_2$).
  - Micro-perforation specification card (hole diameter, breathability guidance).
  - Clear `[RESEARCH REQUIRED]` state badge when cultivar gas tolerances are unverified.
- **Expected Files:** `frontend/src/components/produce/*.tsx`.
- **Verification:** Respiring crops display micro-perforated film guidance and safe gas limits.
- **Definition of Done:** Potato, Broccoli, and Apple test scenarios exhibit appropriate produce behaviors.

---

### Phase 8: End-to-End Testing & Verification
- **Objective:** Validate system across full integration workflows and boundary edge cases.
- **Prerequisites:** Phase 7 complete; [docs/Testing_Security.md](file:///d:/Food-Packaging-AI/docs/Testing_Security.md).
- **Deliverables:**
  - Comprehensive unit test suite covering 100% of domain physics formulas.
  - Automated integration tests verifying API request/response contracts.
  - Playwright end-to-end tests validating the primary user journeys.
- **Expected Files:** `backend/tests/test_e2e.py`, `frontend/tests/e2e/*.spec.ts`.
- **Verification:** Full automated test suite passes with zero warnings or skipped tests.
- **Definition of Done:** "Don't Fool Me" verification audit executed and documented.

---

### Phase 9: Security & Reliability Hardening
- **Objective:** Audit dependencies, sanitize inputs, enforce strict CORS, and verify error boundaries.
- **Prerequisites:** Phase 8 complete.
- **Deliverables:**
  - Dependency vulnerability scan (`pip-audit`, `npm audit`).
  - Strict CORS policy and security headers.
  - Global error boundaries in React preventing client-side crashes.
  - Health check endpoint verification (`/api/health`).
- **Expected Files:** `backend/app/core/security.py`, `frontend/src/components/ErrorBoundary.tsx`.
- **Verification:** Fuzzing with malformed payloads results in clean 400 errors without server crashes.
- **Definition of Done:** Clean security scan and hardened application boundary.

---

### Phase 10: Production Readiness, Security Hardening & SIH Demo Reliability ✅
- **Objective:** Harden configuration, security, database readiness, frontend timeouts, and automate demo verification.
- **Prerequisites:** Phase 9 complete.
- **Deliverables:**
  - Lifespan context manager (`@asynccontextmanager lifespan`) in `backend/app/main.py` auto-initializing database schema.
  - Health & readiness probe (`GET /api/health`) executing lightweight `SELECT 1` checking DB liveness and environment.
  - Clean configuration via `backend/app/core/config.py`, `LOG_LEVEL`, and non-wildcard `CORS_ORIGINS`.
  - Frontend API hardening with `DEFAULT_REQUEST_TIMEOUT_MS = 10000` (10s) and UI retry mechanism.
  - End-to-end smoke test suite (`backend/tests/test_smoke.py`) covering all 4 core SIH demonstration scenarios.
  - Comprehensive evaluator quickstart and local execution documentation in `README.md`.
- **Expected Files:** `backend/app/main.py`, `backend/app/api/v1/health.py`, `backend/tests/test_smoke.py`, `frontend/src/services/api.ts`, `frontend/src/pages/Workspace.tsx`.
- **Verification:** 85/85 backend tests passing, 31/31 frontend tests passing, zero ruff lint errors, production Vite build verified.
- **Definition of Done:** Production-ready configuration, zero hardcoded secrets, deterministic smoke tests passing, evaluated cleanly.

---

### Phase 11: Final Evaluation Harness, SIH Demo Polish & Evidence/Claims Audit ✅
- **Objective:** Finalize golden evaluation matrix, audit scientific evidence/claims, and guarantee rock-solid demo reliability.
- **Prerequisites:** Phase 10 complete; [docs/Evaluation.md](file:///d:/Food-Packaging-AI/docs/Evaluation.md).
- **Deliverables:**
  - Golden evaluation cases fixture (`data/evaluation/prototype_evaluation_cases.json`) covering Scenarios A through H.
  - Automated evaluation matrix test suite (`backend/tests/test_evaluation_matrix.py`) testing all 8 scenarios end-to-end.
  - Critical smoke test audit (`backend/tests/test_smoke.py`) tracing every asserted value to domain formulas, ASTM standards, or prototype assumptions.
  - Comprehensive Claims & Evidence Audit categorizing claims into `[EXTERNAL EVIDENCE]`, `[INFERENCE]`, `[PROTOTYPE ASSUMPTION]`, `[RESEARCH REQUIRED]`, and `[CONTEXT DEPENDENT]`.
  - Alternative recommendation selection audit in `backend/app/domain/ranking.py`.
  - Updated 3-minute and 5-minute SIH live demonstration scripts in `docs/Evaluation.md`.
- **Expected Files:** `data/evaluation/prototype_evaluation_cases.json`, `backend/tests/test_evaluation_matrix.py`, `backend/tests/test_smoke.py`, `docs/Evaluation.md`, `docs/Testing_Security.md`, `docs/Memory.md`.
- **Verification:** 93/93 backend tests passing, 31/31 frontend tests passing, 6/6 manual demo flows verified, 0 ruff lint errors, production Vite build verified.
- **Definition of Done:** The SIH presentation flow is rock-solid, explainable, evidence-backed, and fully verified.

---

### Phase 12: Final SIH Submission Package, Judge-Ready Demo & Project Freeze ✅
- **Objective:** Finalize judge evaluation package, provide 1-click evaluation presets, audit project state inventory, and enforce official project feature freeze.
- **Prerequisites:** Phase 11 complete; [docs/Evaluation.md](file:///d:/Food-Packaging-AI/docs/Evaluation.md).
- **Deliverables:**
  - 1-Click Judge Demonstration Presets component (`frontend/src/components/inputs/DemoPresets.tsx`) embedded directly into Workspace.
  - 11-step sequential judge evaluation journey documented in `docs/Evaluation.md`.
  - 4-category project inventory auditing all capabilities into Implemented, Prototype Assumption, Research Required, and Future Scope.
  - Comprehensive 18-point SIH submission checklist verified and embedded in `docs/Evaluation.md`.
  - Official project feature freeze enacted; no further product modifications or unverified ML additions permitted.
- **Expected Files:** `frontend/src/components/inputs/DemoPresets.tsx`, `frontend/src/pages/Workspace.tsx`, `docs/Evaluation.md`, `docs/Phases.md`, `docs/Memory.md`, `README.md`.
- **Verification:** 93 backend tests passing (100%), 31 frontend vitest tests passing (100%), zero lint/type errors, production Vite build cleanly generated.
- **Definition of Done:** Complete, polished, freeze-locked SIH submission package ready for technical jury evaluation.

