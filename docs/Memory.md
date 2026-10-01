# Project Memory & Architectural Decision Log

**Project Name:** AI-Based Intelligent Food Packaging Material Recommendation System for Food Commodities  
**Problem Statement ID:** SIH26236  
**Document Type:** Persistent Project State & Decision History  
**Last Updated:** Phase 1 Complete (Data Foundation & Curated Knowledge Base Verified)  

---

## 1. Current Project Status
- **Current Phase:** **Phase 1 Complete — Data Foundation & Curated Knowledge Base Verified**. Ready for **Phase 2: Domain Physics & Recommendation Engine**.
- **Data Foundation Status:** Relational ORM models, foreign-key enforcement, database check constraints, repository access layer, and JSON fixture ingestion fully implemented and verified via automated test suite.
- **Application Code Status:** 17 automated tests passing in backend (`pytest` with 100% pass rate). Zero warnings in linting (`ruff check`) and code formatting (`ruff format --check`). Frontend build and strict TypeScript check verified with 0 errors.
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

## 5. Intentionally Deferred Decisions & Future Scope
- **Deferred Decision 1 (Dynamic Shelf-Life Kinetics):** Coupled differential equation simulations for variable non-isothermal cold chains are deferred to Phase 2 research; MVP prototype utilizes empirical benchmark shelf lives.
- **Deferred Decision 2 (Automated Micro-Perforation Laser Sizing):** Exact numerical perforation diameter and pitch modeling per package geometry deferred to future empirical postharvest validation.
- **Deferred Decision 3 (Live Polymer Resin Pricing Feeds):** Real-time commodity market pricing integration deferred; MVP utilizes normalized relative economic multipliers (LDPE = 1.0).

---

## 6. Active Research Gaps & Open Scientific Questions
1. Sizing mass-transfer equations for irregular non-pouch packaging geometries (e.g. thermoformed trays with lidding films).
2. Cultivar-specific $Q_{10}$ factors under severe ambient temperature abuse ($>25^\circ\text{C}$).
3. Threshold pinhole development in thin aluminum foil ($<12\ \mu\text{m}$) during long-haul rough-terrain transit.

---

## 7. Next Implementation Phase
- **Immediate Next Step:** **Phase 2 — Domain Physics & Recommendation Engine**.
- **Scope of Phase 2:** Pure mathematical and physical domain algorithms in `backend/app/domain/` (vapor pressure differential $\Delta p_w$, maximum allowable WVTR/OTR target ranges, produce respiration $Q_{10}$ scaling, constraint filtering, and multi-criteria utility ranking). No frontend features or API endpoints.
