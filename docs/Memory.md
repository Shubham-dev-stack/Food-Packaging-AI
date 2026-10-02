# Project Memory & Architectural Decision Log

**Project Name:** AI-Based Intelligent Food Packaging Material Recommendation System for Food Commodities  
**Problem Statement ID:** SIH26236  
**Document Type:** Persistent Project State & Decision History  
**Last Updated:** Phase 7 Complete (Fresh Produce & MAP Optimization Verified)  

---

## 1. Current Project Status
- **Current Phase:** **Phase 8 Complete — Trade-Off & Multi-Criteria Optimization Verified**. Ready for **Phase 9: End-to-End Testing & Security Hardening**.
- **Engine Logic Status:** Pure deterministic domain layer implemented in `backend/app/domain/` with zero HTTP or UI dependencies. All multi-criteria ranking calculations use transparent linear composite utility functions with explicit barrier, circularity, and cost weighting presets.
- **Application Code Status:**
  - Backend: 69 automated tests passing (`pytest` with 100% pass rate). Zero lint errors (`ruff check`) and formatting verified (`ruff format --check`).
  - Frontend: Production build, strict TypeScript compilation, and 25 unit tests passing (`vitest run`, `tsc -b && vite build`). Clean React 19 + TypeScript architecture using canonical `/api` prefix.
- **Repository Integrity:** Clean, reproducible environment. Database and test files isolated.

---

## 2. Approved Documents Register

| Document | Path | Status | Verification & Role |
| :--- | :--- | :--- | :--- |
| **Problem Statement** | [docs/Problem_Statement.md](file:///d:/Food-Packaging-AI/docs/Problem_Statement.md) | **Approved** | Verbatim SIH26236 problem statement; sole source of product requirements. |
| **Playbook Reference** | [docs/SaaS_Playbook_Reference.md](file:///d:/Food-Packaging-AI/docs/SaaS_Playbook_Reference.md) | **Approved** | 15-Layer Playbook adaptation for SIH engineering discipline. |
| **Scientific Evidence**| [docs/Research_and_Evidence.md](file:///d:/Food-Packaging-AI/docs/Research_and_Evidence.md) | **Approved (Audited)** | Scientific evidence foundation, ASTM testing standards, and safety boundaries. |
| **CLAUDE Context** | [CLAUDE.md](file:///d:/Food-Packaging-AI/CLAUDE.md) | **Approved** | Persistent context, source hierarchy, and verification rules for agents. |
| **PRD** | [docs/PRD.md](file:///d:/Food-Packaging-AI/docs/PRD.md) | **Approved** | Complete functional and non-functional requirements (FR-001 – FR-014). |
| **System Design** | [docs/System_Design.md](file:///d:/Food-Packaging-AI/docs/System_Design.md) | **Approved** | Logical system flows, actor interactions, and state models. |
| **Data Model** | [docs/Data_Model.md](file:///d:/Food-Packaging-AI/docs/Data_Model.md) | **Approved** | Normalized relational entities, units, constraints, and citation keys. |
| **AI Recommendation** | [docs/AI_Recommendation_Engine.md](file:///d:/Food-Packaging-AI/docs/AI_Recommendation_Engine.md) | **Approved** | Domain physics algorithms, produce respiration logic, and multi-criteria ranking. |
| **Architecture** | [docs/Architecture.md](file:///d:/Food-Packaging-AI/docs/Architecture.md) | **Approved** | Modular Monolith (FastAPI + React/TypeScript + SQLite/Postgres). |
| **UX/UI Design** | [docs/Design.md](file:///d:/Food-Packaging-AI/docs/Design.md) | **Approved** | Decision-support workstation layout, component specs, and accessibility. |
| **Engineering Rules**| [docs/Rules.md](file:///d:/Food-Packaging-AI/docs/Rules.md) | **Approved** | Guardrails against hallucinated data, secrets leaks, and test tampering. |
| **Phases Roadmap** | [docs/Phases.md](file:///d:/Food-Packaging-AI/docs/Phases.md) | **Approved** | 12 sequential implementation phases from Phase 0 to Phase 11. |
| **Testing & Security** | [docs/Testing_Security.md](file:///d:/Food-Packaging-AI/docs/Testing_Security.md) | **Approved** | Test pyramid, boundary test matrix, and security threat mitigations. |
| **SIH Evaluation** | [docs/Evaluation.md](file:///d:/Food-Packaging-AI/docs/Evaluation.md) | **Approved** | SIH jury criteria, 3-min/5-min demo scripts, and benchmark scenarios. |
| **Memory Log** | [docs/Memory.md](file:///d:/Food-Packaging-AI/docs/Memory.md) | **Approved** | Living project state register. |
| **Project README** | [README.md](file:///d:/Food-Packaging-AI/README.md) | **Approved** | High-level overview and documentation sitemap. |

---

## 3. Major Architectural & Product Decisions

- **ADR-001: Adoption of Modular Monolith over Distributed Microservices**
  - *Context:* The SIH prototype requires low operational complexity, high developer velocity, and easy local demonstration.
  - *Decision:* Build as a single repository containing decoupled `backend/` (FastAPI) and `frontend/` (React/Vite).
  - *Consequences:* Eliminates distributed networking failure modes; enables single-command local execution for judges.
- **ADR-002: Selection of Domain-Guided Constraint Satisfaction over Black-Box Neural Networks**
  - *Context:* Deep neural networks cannot guarantee adherence to food safety physics or explain recommendations in ASTM units without massive training data (which does not exist for packaging).
  - *Decision:* Employ deterministic mass-transfer formulas, Arrhenius kinetics, and multi-criteria utility ranking.
  - *Consequences:* Recommendations are 100% explainable, mathematically defensible, and safe from catastrophic hallucinations.
- **ADR-003: Inclusion of Recyclable Mono-Materials in Core Material Catalog**
  - *Context:* Plastic Waste Management Rules (India) mandate circularity, but multi-layer foil laminates are unrecyclable.
  - *Decision:* Present recyclable mono-material structures (e.g. BoPE/PE) as explicit alternatives alongside conventional laminates.
  - *Consequences:* Directly satisfies SIH sustainability mandates while highlighting technical barrier trade-offs.
- **ADR-004: Framing Barrier Requirements as Supported Target Ranges & Contextual Food Safety Advisories**
  - *Context:* Open research gaps exist for non-standard geometry mass-transfer and complex multi-hurdle microbial kinetics.
  - *Decision:* Present OTR and WVTR recommendations as evidence-backed target requirement ranges rather than claiming unvalidated exact laboratory cutoffs; present food safety for low-acid reduced-oxygen packs as a contextual safety advisory rather than a simplistic classifier.
  - *Consequences:* Eliminates false claims of laboratory certification while delivering actionable, legally and scientifically sound decision support.
- **ADR-005: Strict SQLite Relational Foreign-Key & CheckConstraint Enforcement**
  - *Context:* SQLite defaults to disabled foreign keys unless explicitly activated per connection.
  - *Decision:* Registered an automatic SQLAlchemy connection listener executing `PRAGMA foreign_keys=ON` on every SQLite connection, paired with database-level `CheckConstraint` bounds on all physical quantities.
  - *Consequences:* Prevents invalid physical parameters or orphan records at the persistence boundary.
- **ADR-006: Pure Decoupled Domain Intelligence Layer**
  - *Context:* Business and physics recommendation logic should be completely decoupled from ORM entities, HTTP routes, serialization formats, and UI frameworks to ensure testability, safety, and reusability.
  - *Decision:* Implemented domain logic exclusively within `backend/app/domain/` using pure Python types and standard library dataclasses (`RecommendationInput`, `TargetSpecifications`, `CandidateEvaluation`, `RecommendationResultDomain`).
  - *Consequences:* The engine executes deterministically in in-memory test environments with zero HTTP or UI overhead.

---

## 4. Phase 1 Data Foundation Summary

- **Database Engine:** SQLite 3 (for local development and evaluation), configurable via `DATABASE_URL` in `.env`.
- **ORM Framework:** SQLAlchemy 2.1 (using modern `DeclarativeBase`, `Mapped`, `mapped_column`, `relationship`, `CheckConstraint`).
- **Implemented Entities (`backend/app/models/`):**
  1. `EvidenceSource`: Bibliographic citations, author/year, source type, and DOI/standards keys.
  2. `Commodity`: Core food items with category, respiration flag, and default storage mode.
  3. `CommodityProperty`: Physicochemical characteristics ($a_w$, moisture %, fat %, pH, temperature/RH bounds, spoilage pathways) linked to `EvidenceSource`.
  4. `ProduceRespirationData`: Produce respiration rates at reference temperatures, $Q_{10}$ factors, critical $\text{O}_2$ extinction, and $\text{CO}_2$ limits.
  5. `MAPConfiguration`: Evidence-backed gas composition targets ($\text{O}_2, \text{CO}_2, \text{N}_2$), target temperatures, and suitability advisories.
  6. `PackagingMaterial`: Base polymers and laminates with family, density, sealability, and recyclability category.
  7. `PackagingBarrierProperty`: Quantitative barrier metrics (OTR under ASTM D3985, WVTR under ASTM F1249, gauge in $\mu\text{m}$, mechanical strength).
  8. `SustainabilityMetric`: Carbon footprint ($\text{kg CO}_2\text{-eq}/\text{kg}$), circularity tier, and Indian EPR category.
  9. `CostIndex`: Normalized economic multiplier relative to baseline LDPE film ($= 1.0$) and conversion complexity.
  10. `RecommendationRequest`: Request audit log storing evaluation inputs.
  11. `RecommendationResult`: Output audit log storing material recommendations and explainability summaries.
- **Seed & Fixture Ingestion (`data/knowledge_base/seed.py`):**
  - Fixtures stored in `data/processed/*.json`.
  - Ingests 8 bibliographic evidence records, 8 packaging materials, and 5 representative benchmark commodities.
  - Full idempotency: checks existence before inserting; repeated seeding causes zero duplicates.
- **Repository Access Abstractions (`backend/app/repositories/`):**
  - `EvidenceRepository`: Query by ID, list all.
  - `CommodityRepository`: Query by ID, common name, list with joined relationships.
  - `MaterialRepository`: Query by ID, trade code, filter by polymer family with joined barrier/sustainability/cost.

---

## 5. Phase 2 Domain Physics & Recommendation Engine Summary

- **Engine Package (`backend/app/domain/`):**
  1. `types.py`: Domain data definitions, immutable dataclasses, standard enums (`RecommendationStatus`, `CandidateEligibility`, `StorageType`, `TransitStress`), `TransitGaugeConfig` for configurable mechanical thickness baselines, and `RankingWeightsConfig` enforcing sum=1.0 validation.
  2. `units.py`: Strict physical unit conversions ($\mu\text{m} \leftrightarrow \text{mil}$, $^\circ\text{C} \leftrightarrow \text{K}$), Tetens saturation vapor pressure equation $p_{\text{sat}}(T)$ with separate water and ice coefficients, and vapor pressure gradient calculation $\Delta p_w$.
  3. `barrier.py`:
     - Added `calculate_mass_balance_moisture_flux` deriving required moisture flux step-by-step from product geometry and shelf life in $[g / (m^2 \cdot \text{day})]$.
     - Formally distinguished mass-balance moisture flux, linearized permeance scaling `[PROTOTYPE ASSUMPTION]`, and evidence-backed empirical target ranges (Robertson 2012 / Labuza 1998).
     - Labeled OTR cutoffs as `[PROTOTYPE HEURISTIC: Robertson 2012 / Marsh & Bugusu 2007]` with ASTM D3985-17 standard test conditions (23°C, 0% RH).
     - Made transit gauge calculation configurable via `TransitGaugeConfig` with explicit `[PROTOTYPE ASSUMPTION]` labels and ASTM F1306/D4169 test caveats.
  4. `respiration.py`:
     - Fresh produce respiration kinetics scaled via $Q_{10}$ exponential model linked directly to Fonseca 2002.
     - Coupled equilibrium oxygen transmission rate ($\text{OTR}_{\text{eq}}$) calculation based on package surface area and produce mass.
     - Micro-perforation evaluation updated to reflect film permselectivity $\beta = \text{CO}_2/\text{O}_2 \approx 3\text{--}6$ relative to commodity $\text{CO}_2$ tolerance and transmission capacity.
  5. `safety.py`:
     - Reframed ROP evaluation as an educational, contextual advisory: `[CONTEXTUAL FOOD SAFETY ADVISORY - REDUCED-OXYGEN PACKAGING]`.
     - Explicitly separated contextual hazard flags (*Clostridium botulinum* germination in low-acid $pH \ge 4.6$ and high moisture $a_w \ge 0.92$) from regulatory certification, declaring that the software does NOT certify commercial food safety compliance (21 CFR 114 / FSSAI).
  6. `filtering.py`:
     - Replaced hard produce OTR cutoffs with coupled hypoxia risk check ($bp.\text{otr} < 0.20 \times \text{OTR}_{\text{eq}}$ for continuous dense films).
     - Converted dense film disqualifications for respiring produce to `CONDITIONALLY_ELIGIBLE` with perforation/venting requirements.
     - Removed arbitrary `shelf_life > 60` threshold for light protection; light barrier conditionality now triggered directly by documented commodity photosensitivity.
     - Converted sub-zero neat PLA rejection into a qualitative conditionality (`CONDITIONALLY_ELIGIBLE`), noting low glass transition temperature $T_g \approx 55\text{--}60^\circ\text{C}$ and requiring ASTM D1709 impact validation.
  7. `ranking.py`:
     - Implemented configurable `RankingWeightsConfig` defaulting to the 50/30/20 baseline from `docs/AI_Recommendation_Engine.md` Section 3.5 (Barrier Safety Margin $w_{\text{barrier}} = 0.50$, Sustainability $w_{\text{sust}} = 0.30$, Economic Index $w_{\text{cost}} = 0.20$).
     - Provided `SUSTAINABILITY_PRIORITY_WEIGHTS` preset (0.40/0.45/0.15).
     - Implemented candidate sorting precedence ensuring fully `ELIGIBLE` candidates always rank ahead of `CONDITIONALLY_ELIGIBLE` candidates before utility score sorting.
  8. `explanation.py`:
     - Deterministic explainability synthesis generating human-readable dominant spoilage drivers, critical storage factors, primary/alternative selection rationales, candidate disqualification audits with explicit rejection reasons, and prototype modeling assumptions.
     - Citation consistency enforced: Robertson edition corrected to 2012 (`REF_ROBERTSON_2012`), ASTM standards updated to ASTM D3985-17 and ASTM F1249-20.
  9. `engine.py`: `RecommendationEngine.evaluate()` coordinator managing the end-to-end evaluation pipeline deterministically with zero database or network side effects.

- **Scientific Guardrail Patch Summary:**
  - Audit verified dimensional correctness and separated mass balance flux from material permeance.
  - Replaced universal hard cutoffs with prototype assumptions/heuristics labeled `[PROTOTYPE ASSUMPTION]` or `[PROTOTYPE HEURISTIC]`.
  - Replaced arbitrary light barrier threshold with documented commodity photo-sensitivity.
  - Coupled produce respiration to package area, mass, and film permselectivity.
  - Made ranking weights configurable with validated baseline weights (50/30/20).
  - Ensured all generated recommendation citations resolve to existing seeded `EvidenceSource` records.
  - Test suite expanded to 41 automated tests in backend (`pytest` with 100% pass rate: 8 data models, 14 physics unit tests, 2 health checks, 10 engine integration scenarios, 7 seeding idempotency tests). Zero lint errors (`ruff check`) and formatting verified (`ruff format --check`).

---

## 6. Intentionally Deferred Decisions & Future Scope
- **Deferred Decision 1 (Dynamic Shelf-Life Kinetics):** Coupled differential equation simulations for variable non-isothermal cold chains are deferred; MVP prototype utilizes empirical benchmark shelf lives.
- **Deferred Decision 2 (Automated Micro-Perforation Laser Sizing):** Exact numerical perforation hole diameter, count, and pitch modeling per package geometry deferred to future empirical postharvest validation.
- **Deferred Decision 3 (Live Polymer Resin Pricing Feeds):** Real-time commodity market pricing integration deferred; MVP utilizes normalized relative economic multipliers (LDPE = 1.0).

---

## 7. Active Research Gaps & Open Scientific Questions
1. Analytical and numerical sizing of mass-transfer equations for irregular non-pouch packaging geometries (e.g. thermoformed trays with lidding films, rigid bottles).
2. Cultivar-specific $Q_{10}$ factors and respiration rates under severe ambient temperature abuse ($>25^\circ\text{C}$).
3. Threshold pinhole development in thin aluminum foil ($<12\ \mu\text{m}$) during long-haul rough-terrain transit.
4. Non-linear temperature-dependent water vapor permeation in hydrophilic bio-based polymers (e.g., starch blends, chitosan).

---

---

## 8. Phase 3 REST API & Integration Summary

- **Architecture:** Decoupled layered architecture where the HTTP/API layer acts purely as an adapter around the pure domain engine.
  - `HTTP Request` $\rightarrow$ `FastAPI Router` $\rightarrow$ `Pydantic v2 Request Validation` $\rightarrow$ `RecommendationService` $\rightarrow$ `Repositories (Joined SQLAlchemy ORM)` $\rightarrow$ `RecommendationEngine.evaluate(...)` (Pure domain) $\rightarrow$ `RecommendationRepository (Audit Log Persistence)` $\rightarrow$ `Pydantic Response Serialization`.
- **Domain Layer Boundary Preserved:** `backend/app/domain/` remained 100% untouched. Zero imports of FastAPI, Pydantic, SQLAlchemy, or HTTP exceptions in domain logic.
- **Implemented Endpoints (`/api` prefix):**
  1. `GET /api/health` — System and database health status (preserved from Phase 0).
  2. `GET /api/commodities` — Query catalog of commodities (optional `category` filter).
  3. `GET /api/commodities/{commodity_id}` — Detailed postharvest parameters, baseline properties, respiration data, and MAP targets.
  4. `GET /api/materials` — Query candidate packaging materials (optional `family` filter) with ASTM test specs, eco-metrics, and cost index.
  5. `GET /api/materials/{material_id}` — Complete physical barrier specs, test conditions, recyclability, and cost multiplier.
  6. `GET /api/evidence` — Query bibliographic citations, ASTM testing standards, and literature evidence.
  7. `GET /api/evidence/{reference_id}` — Detailed citation metadata, DOI/standard number, and verification notes.
  8. `POST /api/recommendations` — Evaluate optimal packaging materials, barrier targets, and explainable decision trace for given commodity context.
  9. `GET /api/recommendations/{request_id}` — Retrieve persisted recommendation session by audit ID.
  10. `GET /` — API root service status and link to interactive OpenAPI documentation (`/docs`).
- **Standardized Error Handling (`backend/app/api/errors.py`):**
  - Uniform JSON structure: `{"error": "...", "message": "...", "details": [...]}`.
  - Pydantic validation errors return structured 422 with field-level issues.
  - Missing entities return 404 with clean resource descriptions.
  - Unhandled server exceptions logged internally with generated UUID `error_id`, returning sanitized 500 without leaking stack traces or environment variables.
- **Audit Persistence (`backend/app/repositories/recommendation_repository.py`):**
  - Every evaluation logs full input conditions to `recommendation_requests` and resulting recommendations to `recommendation_results`.
- **Automated Verification:** 61 automated tests passing across 10 test modules (`pytest` 100% pass rate). Ruff linting and formatting 100% compliant. Frontend strict TypeScript check and production build verified with 0 errors.

---

## 9. Next Implementation Phase (Historical)
- **Immediate Next Step:** **Phase 4 — Frontend Core & Input Workspace**.
- **Scope of Phase 4:** Build the React + TypeScript responsive input workstation (split-screen layout, commodity search/selector, physical parameter sliders with real-time client-side bounds checking, storage mode toggles, and API client integration). Results dashboard rendering deferred to Phase 5.

---

## 10. Phase 4 Frontend Core & Input Workspace Summary

- **Architecture:** Professional responsive split-screen input workstation built with React 19, TypeScript, Vite, and Tailwind CSS v4.
  - Zero heavy external state management libraries (Redux/Zustand); uses clean React state/hooks and modular components.
  - Full adherence to canonical API route prefix: strictly `/api` via Vite development proxy (`/api` $\rightarrow$ `http://127.0.0.1:8000`).
- **Core Components Created & Integrated (`frontend/src/`):**
  1. `types/api.ts`: Canonical TypeScript type definitions strictly matching backend Pydantic models (`RecommendationCreateRequest`, `RecommendationResponse`, `CandidateEvaluationResponse`, `CommodityDetailResponse`, `CommodityBriefResponse`, etc.).
  2. `services/api.ts`: Strongly-typed API client wrapper handling `GET /api/commodities`, `GET /api/commodities/{id}`, `POST /api/recommendations`, `GET /api/recommendations/{id}`, and `GET /api/health`, converting backend error responses to typed `ApiError` instances.
  3. `components/common/FormField.tsx`: Reusable accessible form field wrapper supporting label, sublabel, required badge, user override indicator, reset action, and inline validation errors.
  4. `components/common/Alert.tsx`: Reusable alert banner with semantic styling (`info`, `warning`, `error`, `success`).
  5. `components/inputs/CommodityPicker.tsx`: Commodity selection dropdown with loading, empty catalog, and error/retry states.
  6. `components/inputs/BaselinePreviewCard.tsx`: Real-time inspection panel displaying the selected commodity's baseline physicochemical parameters ($a_w$, typical moisture %, fat %, pH), respiration kinetics ($Q_{10}$, reference rate), and literature citation provenance.
  7. `components/inputs/EnvironmentalInputs.tsx`: Distribution & storage condition controls including storage regime segmented selector (`ambient`, `chilled`, `frozen`), target shelf life days (1 to 730), temperature slider (-25°C to 50°C), RH slider (10% to 100%), and transit stress profile selector (`local_standard`, `long_haul_refrigerated`, `rough_terrain_unpaved`).
  8. `components/inputs/PropertyOverrides.tsx`: Collapsible accordion for optional user overrides (moisture %, $a_w$, fat %, pH, respiration rate) with individual "Reset to Baseline" controls, packaging prototype geometry inputs (net weight kg, permeation area m²), and the bio-based/circular substrate preference toggle.
  9. `pages/Workspace.tsx`: Top-level input workstation coordinating state, client-side validation, backend request submission, submission spinner, error reporting, and Phase 4/Phase 5 handoff feedback panel.
  10. `App.tsx`: Mounted `Workspace` component as root application view.
- **Client-Side Validation & Guardrails:**
  - Enforces shelf life bounds (1–730 days), temperature bounds (-25°C to 50°C), RH bounds (10%–100%), geometry bounds ($>0$).
  - Enforces storage regime physical coherence: frozen $\le 0.0^\circ\text{C}$, chilled $-2.0^\circ\text{C}$ to $15.0^\circ\text{C}$, ambient $\ge 5.0^\circ\text{C}$.
  - Respiration override disabled for non-respiring crops.
- **Scope Discipline Maintained:**
  - Zero modification to backend domain engine in `backend/app/domain/`.
  - Final results dashboard, candidate comparison radar/bar charts, detailed packaging specs grid, MAP gas dynamics visualizations, and QR code generation are strictly deferred to Phase 5.
- **Verification Status:**
  - `tsc -b && vite build` succeeds with 0 errors.
  - Backend 61 pytest tests passing with 100% rate.
  - Backend lint and format 100% compliant (`ruff check`, `ruff format --check`).

---

## 11. Phase 5 Recommendation Dashboard & Results Display Summary

- **Architecture:** Complete user-facing recommendation results experience presenting the backend's deterministic decision output without altering or replicating any scientific algorithms in the frontend.
  - Zero duplicate recommendation logic in the client.
  - Clean state flow: `IDLE` $\rightarrow$ `SUBMITTING` $\rightarrow$ `SUCCESS` (`result` view) / `ERROR`.
  - Seamless navigation between the 2 workflow steps: `[1. Input Parameters]` $\leftrightarrow$ `[2. Recommendation Result]`, preserving submitted inputs and allowing instant adjustments or new evaluations.
- **Created & Integrated Components (`frontend/src/`):**
  1. `components/recommendation/StatusBadge.tsx`: Visual badge rendering the 4 backend decision states with explicit semantic badges:
     - `SUPPORTED`: Sufficient evidence exists for prototype decision.
     - `CONDITIONAL`: Depends on documented storage/handling conditions.
     - `INSUFFICIENT_EVIDENCE`: Available information is not sufficient for confident recommendation.
     - `RESEARCH_REQUIRED`: Scientific/data evidence is missing; no answer fabricated.
  2. `components/recommendation/PrimaryRecommendationCard.tsx`: Highlights the primary recommended packaging structure, material family, trade code, nominal gauge (with mil conversion), OTR, WVTR, circularity/mono-material status, relative cost multiplier, MCDA score, and condition notes with non-guarantee prototype language.
  3. `components/recommendation/AlternativeRecommendationCard.tsx`: Presents the alternative material structure for different engineering or circularity trade-offs (e.g. recyclable mono-material or bio-based polymer) without framing it as an error or inferior fallback.
  4. `components/recommendation/TechnicalSpecificationGrid.tsx`: Dedicated technical specifications section displaying ASTM F1249 WVTR target, ASTM D3985 OTR target, ASTM D4169/F1306 recommended gauge, sealability, light-barrier requirement, microperforation requirement, and their respective analytical/mechanical rationales.
  5. `components/recommendation/CandidateComparisonTable.tsx`: Full candidate comparison matrix displaying material name, polymer family, structure, eligibility, barrier safety score, circularity score, relative cost index, MCDA composite utility, gauge, OTR, and WVTR.
  6. `components/recommendation/DisqualifiedCandidatesList.tsx`: Collapsible accordion displaying all disqualified candidates with their exact backend rejection reasons and barrier snapshots.
  7. `components/recommendation/SafetyAdvisoryBanner.tsx`: Prominent, non-alarmist warning banner rendering contextual food safety advisories (e.g. *Clostridium botulinum* risks in reduced-oxygen packs) with explicit disclaimers regarding regulatory certification.
  8. `components/recommendation/UncertaintyNotesCard.tsx`: Displays analytical uncertainty notes, documented engineering assumptions, and scientific limitations directly from the backend explanation trace.
  9. `pages/RecommendationResultView.tsx`: Top-level result dashboard page assembling all specification and comparison components with review/modify action buttons and submitted context summary.
- **Warning Audit (Step 0):**
  - Audited 4 warnings from pytest suite:
    - 3 warnings caused by Starlette deprecation of `HTTP_422_UNPROCESSABLE_ENTITY` in favor of `HTTP_422_UNPROCESSABLE_CONTENT`. Safely updated in `backend/app/api/errors.py`.
    - 1 warning from upstream `starlette.testclient` recommending `httpx2`. Identified as an informational deprecation notice within Starlette's test harness; intentionally deferred as it does not affect correctness, runtime execution, or production dependencies.
- **Verification Status:**
  - `npm run build` (`tsc -b && vite build`): Succeeded in 603ms with 0 errors across 33 transformed modules.
  - Backend pytest suite: 61 passed with 100% pass rate.
  - Backend lint & format: 100% compliant (`ruff check`, `ruff format --check`).

---

## 12. Phase 6 Explainability & Evidence Traceability Summary

- **Architecture:** Complete user-facing explainability and scientific evidence traceability experience presenting structured rationale, decision constraints, disqualification reasoning, and bibliographic literature provenance directly from the backend domain engine.
  - Zero duplicate recommendation logic in the client.
  - Fully decoupled and transparent hierarchy:
    1. Primary Recommendation Card
    2. "Why this recommendation?" (dominant spoilage vector & selection rationale)
    3. Governing Decision Factors & Packaging Constraints
    4. Technical Engineering Specification Grid
    5. Alternative Recommendation Card
    6. Candidate Materials Comparison Matrix
    7. Disqualified Candidates Log (why other candidates were ruled out)
    8. Scientific Evidence Traceability Panel (resolving cited source IDs to title, authors, year, standard number, and scope notes)
    9. Documented Engineering Assumptions Panel
    10. Uncertainty Profile & Decision Status Confidence
    11. Scientific Limitations & Boundaries Panel
- **Evidence Retrieval & Traceability Strategy:**
  - Surfaced citations strictly map to real seeded `EvidenceSource` records (`REF_ROBERTSON_2012`, `REF_ASTM_F1249`, `REF_ASTM_D3985`, `REF_KADER_2002`, `REF_FONSECA_2002`, `REF_USDA_HB66_2016`, etc.).
  - Frontend utilizes memoized session cache (`evidenceCache`) to resolve individual citations via `GET /api/evidence/{reference_id}` on-demand, preventing redundant network queries.
  - Built an accessible modal dialog displaying detailed citation metadata, publication year, author list, standard number, and verification notes.
  - Graceful degradation: Unresolvable or missing evidence IDs display an explicit *"Unresolved Reference / Metadata unavailable"* notice without breaking page rendering or concealing the recommendation.
- **Verification & Test Status:**
  - Frontend Vitest suite: 10/10 automated tests passing covering rationale rendering, decision factors, disqualification expansion, evidence resolution, missing evidence fallback, assumptions, limitations, safety advisory, and uncertainty profile.
  - Strict TypeScript check (`tsc -b --noEmit`) and Vite production build pass with 0 errors across 38 transformed modules.
  - Backend regression: 61/61 pytest tests passing (100% pass rate).
  - Ruff lint & format: 100% compliant (`ruff check`, `ruff format --check`).

---

## 13. Phase 7 Fresh Produce & Modified Atmosphere Packaging (MAP) Optimization Summary

- **Architecture:** Dedicated fresh produce post-harvest respiration and MAP experience in the recommendation results flow, presenting post-harvest biological kinetics, $Q_{10}$ temperature scaling adjustments, coupled equilibrium gas exchange interactions, MAP headspace gas target compositions, and packaging ventilation/micro-perforation guidance.
  - Zero duplicate recommendation logic in the client; all values and recommendations directly reflect the backend's deterministic domain physics (`backend/app/domain/respiration.py`).
  - Conditioned on `commodityDetail.is_respiring`: Non-respiring foods (e.g. potato chips, roasted peanuts, frozen foods) completely omit the fresh produce dashboard.
  - Transparent physiological boundaries: Clarifies why fresh produce cannot simply be treated as an inert shelf-stable food requiring high-barrier hermetic sealing.
- **Created & Integrated Components (`frontend/src/components/recommendation/fresh-produce/`):**
  1. `RespirationKineticsCard.tsx`:
     - Visualizes reference respiration rate at baseline temperature ($mg\ \text{CO}_2 / (kg \cdot hr)$).
     - Visualizes $Q_{10}$ temperature scaling factor and dynamically calculated rate at current operating storage temperature using $R(T) = R(T_{\text{ref}}) \times Q_{10}^{(T - T_{\text{ref}})/10}$.
     - Renders physiological safety limits: Critical $\text{O}_2$ extinction threshold (fermentation onset point) and maximum tolerable $\text{CO}_2$ concentration.
     - Detects and highlights temperature abuse alerts: Freezing/chilling injury risk for temperatures $<0^\circ\text{C}$ and accelerated respiratory depletion/anaerobic breakdown warning for temperatures $>25^\circ\text{C}$.
  2. `MAPSuitabilityCard.tsx`:
     - Visualizes MAP suitability status badge (`MAP Recommended`, `Ventilated Only`, or `Research Required`).
     - Target headspace gas composition bar and percentage metrics ($\text{O}_2$, $\text{CO}_2$, $\text{N}_2$ balance).
     - Renders practical handling notes (post-harvest pre-cooling to target temp, packaging gas flush guidelines).
     - Links literature citations (e.g., Kader 2002, USDA HB-66) through to the Phase 6 evidence resolution modal.
  3. `VentilationGuidanceCard.tsx`:
     - Equilibrium oxygen transmission demand: Contrasts packaging film continuous breathability against active respiring biomass demand.
     - Transpiration & condensation risk: WVTR management to prevent free water droplet accumulation and subsequent fungal/bacterial decay.
     - Micro-perforation vs. continuous film engineering rationale: Explains why standard high-barrier plastic films suffocate living produce and when laser/mechanical micro-perforations or ventilated macro-holes are physically mandated.
  4. `FreshProduceDashboard.tsx`:
     - Orchestrates the three cards under a dedicated "Fresh Produce Respiration & MAP Optimization" section header.
     - Guarded by `commodityDetail?.is_respiring`; returns `null` for non-respiring crops.
- **Integration Points:**
  - `pages/RecommendationResultView.tsx`: Embeds `FreshProduceDashboard` directly beneath the `PrimaryRecommendationCard` and above the "Why this recommendation?" explainability section, ensuring post-harvest physiology takes visual precedence for living produce.
  - `pages/Workspace.tsx`: Passes `commodityDetail` down to `RecommendationResultView`.
- **Verification & Test Status:**
  - Frontend Vitest suite: 8 dedicated tests in `frontend/src/tests/FreshProduceMAP.test.tsx` (18 total frontend tests passing across the test suite):
    1. Renders fresh produce dashboard for respiring commodities (`is_respiring: true`).
    2. Completely suppresses fresh produce dashboard for non-respiring commodities (`is_respiring: false` / null).
    3. Calculates and displays temperature-scaled respiration rate via $Q_{10}$ equation.
    4. Displays target gas composition windows ($\text{O}_2$, $\text{CO}_2$, $\text{N}_2$) for MAP-recommended produce.
    5. Displays ventilated-only advisory when MAP is unsuitable.
    6. Displays research-required advisory when MAP data is unvalidated or unavailable.
    7. Displays micro-perforation breathability guidance when required.
    8. Flags extreme temperature warnings (chilling/freezing $<0^\circ\text{C}$ and heat abuse $>25^\circ\text{C}$).
  - Strict TypeScript check (`tsc -b --noEmit`) passes with 0 errors.
  - Vite production build (`vite build`) passes with 0 errors across 42 transformed modules in ~885ms.
  - Backend pytest regression: 61/61 tests passing (100% pass rate).
  - Ruff lint & format: 100% compliant (`ruff check`, `ruff format --check`).

---

## 14. Phase 8 Trade-Off & Multi-Criteria Optimization Summary

- **Architecture:** Implemented transparent multi-criteria decision analysis (MCDA) across backend domain and frontend UI:
  - Preset Configurations:
    - `balanced`: 50% Barrier ($w_b = 0.50$), 30% Sustainability ($w_s = 0.30$), 20% Cost ($w_c = 0.20$).
    - `sustainability`: 40% Barrier ($w_b = 0.40$), 45% Sustainability ($w_s = 0.45$), 15% Cost ($w_c = 0.15$).
    - `cost`: 40% Barrier ($w_b = 0.40$), 15% Sustainability ($w_s = 0.15$), 45% Cost ($w_c = 0.45$).
  - Strict Hard Physical Constraints vs Soft Preference Boundaries:
    - Hard physical packaging constraints (WVTR target compliance, OTR target compliance, micro-perforation suitability, thermal/storage limits) gate candidate qualification first in `filter_candidates()`.
    - Soft preferences (`optimization_preference`) ONLY rank qualified candidates. Disqualified candidates cannot be rescued by weighting adjustments.
  - Transparent Composite Utility Breakdown:
    - $U = w_b \cdot S_b + w_s \cdot S_s + w_c \cdot S_c$
    - Reports exact factor contributions: `barrier_contribution`, `sustainability_contribution`, `cost_contribution`, final rank `#1, #2, ...`, and applied weights object.
  - Produce Respiration Rate Authority Audit:
    - In `RespirationKineticsCard.tsx`, accepts authoritative Q10 adjusted rate from domain engine (`target_specifications.adjusted_respiration_rate_co2`) rather than acting as a second scientific calculation source.
- **Frontend Implementation (`frontend/src/components/recommendation/trade-off/`):**
  - `TradeOffAnalysisCard.tsx`:
    - 3-way preset selector tabs (`Balanced`, `Sustainability Priority`, `Cost Priority`) with active preference badge.
    - Visual weight distribution stacked bar with percentage indicators.
    - Qualified Candidates Score Breakdown table displaying raw score, weighted contribution breakdown ($w \cdot S$), composite utility, and rank.
    - Hard vs Soft constraint distinction callout informing users why disqualified candidates cannot be promoted.
    - Plain-language trade-off summary explaining why the primary candidate scored highest and what trade-offs were made.
  - `RecommendationResultView.tsx` & `Workspace.tsx`:
    - Interactive `onPreferenceChange` callback enabling live re-evaluation with stateful persistence.
- **Verification & Test Status:**
  - Backend: 8 dedicated tests in `backend/tests/test_trade_off_optimization.py` verifying default weights, sustainability priority, cost priority, hard constraint immunity, score breakdown summation, ranking determinism, produce constraints, and schema validation.
  - 69/69 pytest tests passing (100% pass rate). Ruff check & format clean.
  - Frontend: 7 dedicated tests in `frontend/src/tests/TradeOffOptimization.test.tsx` (25 total frontend tests passing across 3 test files).
  - Strict TypeScript check (`tsc -b --noEmit`) passes with 0 errors. Vite production build passes with 0 errors (43 modules).

---

## 15. Next Implementation Phase
- **Immediate Next Step:** **Phase 9 — Security & Reliability Hardening / End-to-End Testing**.
- **Scope of Phase 9:** Dependency vulnerability scan, strict CORS and security headers, input sanitization, global error boundaries, and end-to-end integration workflows.


