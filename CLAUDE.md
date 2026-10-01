# Project: SIH 2026 - SIH26236
**AI-Based Intelligent Food Packaging Material Recommendation System for Food Commodities**

---

# Problem Statement
Packaging plays a critical role in preserving the quality, safety, and shelf life of food commodities during storage, transport, and distribution. Improper selection causes moisture degradation, lipid oxidation, microbial spoilage, and massive food loss. Small food businesses, farmers, startups, and local manufacturers often lack specialized packaging engineering expertise. Fresh produce continues post-harvest respiration, requiring strict control over oxygen and carbon dioxide permeation.

This project delivers an intelligent decision-support software application that evaluates commodity characteristics and storage/transport conditions to recommend optimized packaging materials and technical specifications (OTR, WVTR, thickness, sealability, gas permeability, mechanical strength, and MAP suitability).

---

# Source of Truth & Hierarchy
1. **Primary Product Requirements**: [docs/Problem_Statement.md](file:///d:/Food-Packaging-AI/docs/Problem_Statement.md) (verbatim SIH26236 statement).
2. **Scientific & Technical Evidence**: [docs/Research_and_Evidence.md](file:///d:/Food-Packaging-AI/docs/Research_and_Evidence.md) (peer-reviewed literature, official food packaging handbooks, ASTM/ISO standards).
3. **Engineering & Architecture Methodology**: [docs/SaaS_Playbook_Reference.md](file:///d:/Food-Packaging-AI/docs/SaaS_Playbook_Reference.md) (derived from the 15-Layer Playbook).
4. **Project Assumptions**: Only allowed when explicitly tagged as `[PROTOTYPE ASSUMPTION]`.

> **Note on Agent Roles:** Claude may be used as an external planning and review assistant if requested, but the local repository documentation is the primary source of truth. **Antigravity** will perform all codebase implementation tasks following approved documentation phases.

---

# Product Goal
Deliver an intelligent, scientifically defensible, explainable web/mobile decision-support prototype that assists farmers, food startups, and manufacturers in selecting suitable, cost-effective, and sustainable food packaging materials without requiring deep polymer physics training.

---

# Current Status
- **Current Phase**: Documentation Complete (All 16 Foundation Documents Approved).
- **Application Code**: None. (Implementation commences in Phase 0 upon user prompt).
- **Core Architecture Stance**: Modular Monolith (FastAPI + React/TypeScript + SQLite/Postgres) optimized for low operational complexity, high transparency, and verifiable domain calculations.

---

# Document Map
- [docs/Problem_Statement.md](file:///d:/Food-Packaging-AI/docs/Problem_Statement.md) — Verbatim SIH26236 statement.
- [docs/SaaS_Playbook_Reference.md](file:///d:/Food-Packaging-AI/docs/SaaS_Playbook_Reference.md) — 15-Layer Playbook adaptation for SIH engineering discipline.
- [docs/Research_and_Evidence.md](file:///d:/Food-Packaging-AI/docs/Research_and_Evidence.md) — Peer-reviewed scientific evidence, ASTM standards, and safety boundaries.
- [docs/PRD.md](file:///d:/Food-Packaging-AI/docs/PRD.md) — Product requirements, input/output schemas, and functional requirements.
- [docs/System_Design.md](file:///d:/Food-Packaging-AI/docs/System_Design.md) — Logical system flows, actor interactions, produce respiration branch, and state management.
- [docs/Data_Model.md](file:///d:/Food-Packaging-AI/docs/Data_Model.md) — Relational entities, physical units, data validation rules, and citation keys.
- [docs/AI_Recommendation_Engine.md](file:///d:/Food-Packaging-AI/docs/AI_Recommendation_Engine.md) — Domain-guided constraint filtering, respiration physics, and multi-criteria utility ranking.
- [docs/Architecture.md](file:///d:/Food-Packaging-AI/docs/Architecture.md) — Modular Monolith technical architecture and stack specifications.
- [docs/Design.md](file:///d:/Food-Packaging-AI/docs/Design.md) — Decision-support workstation wireframes, component layouts, and accessibility standards.
- [docs/Rules.md](file:///d:/Food-Packaging-AI/docs/Rules.md) — Strict engineering, scientific, and testing guardrails.
- [docs/Phases.md](file:///d:/Food-Packaging-AI/docs/Phases.md) — 12-phase sequential engineering roadmap for Antigravity.
- [docs/Testing_Security.md](file:///d:/Food-Packaging-AI/docs/Testing_Security.md) — Test pyramid, boundary test matrix, and security threat mitigations.
- [docs/Evaluation.md](file:///d:/Food-Packaging-AI/docs/Evaluation.md) — SIH jury criteria, measurable prototype metrics, and 3-min/5-min demo scripts.
- [docs/Memory.md](file:///d:/Food-Packaging-AI/docs/Memory.md) — Living project state register and Architectural Decision Records (ADRs).
- [README.md](file:///d:/Food-Packaging-AI/README.md) — High-level overview and documentation sitemap.

---

# Scientific Data Rules
- **SIH problem statement is the primary product source.**
- **Never invent scientific facts.**
- **Never invent material properties.**
- **Never invent numeric thresholds.**
- **Never invent model accuracy.**
- **Never invent experimental results.**
- **Clearly label assumptions.** Always mark unverified baselines as `[PROTOTYPE ASSUMPTION]`.
- **Scientific claims require evidence.** Cite the author, standard (e.g. ASTM D3985, ASTM F1249), or reference book for every barrier value or respiration rate.
- **Separate scientific research from implementation decisions.** Food preservation physics and polymer properties must be validated independently of UI and database choices.
- **Do not silently change the problem statement.** Preserve requirements as defined.

---

# Engineering Principles
- **You are the architect; the agent is the builder.** Decide first, then delegate.
- **Plan before code, every time.** Fixing a plan in documentation is cheap; refactoring hallucinated code is expensive.
- **Follow the 5-step loop**: `Plan → Review → Implement small → Verify → Record decision`.
- **Do not over-engineer the SIH prototype.** Do not introduce microservices, distributed queues, or complex multi-tenant billing when a clean modular application is what the project demands.
- **Do not add features merely because they are technically interesting.** Stick strictly to the problem statement and justified extensions.
- **Keep recommendation logic explainable.** Users must see the scientific rationale, barrier requirements, and standard references behind each recommendation, not a black-box output.
- **Server is the source of truth.** All domain validations, barrier threshold evaluations, and optimization scores must be verified on the backend.

---

# Verification Rules
- **Every significant architectural decision must be recorded in Memory.md.**
- **Every implementation task must eventually be verified.**
- **Do not claim completion when verification has not been performed.**
- **Never edit a test to pass.** If a test exposes a flaw, fix the underlying calculation or logic.
- **Follow the universal verification standard**:
  1. Inspect real output from linters, typechecks, and tests.
  2. List every file modified and why.
  3. List anything skipped, stubbed, mocked, or hard-coded.
  4. Explicitly highlight assumptions requiring confirmation.

---

# Required Reading Before Coding
Before writing any backend, AI, or frontend code, every developer and AI agent must read:
1. [docs/Problem_Statement.md](file:///d:/Food-Packaging-AI/docs/Problem_Statement.md)
2. [docs/Research_and_Evidence.md](file:///d:/Food-Packaging-AI/docs/Research_and_Evidence.md)
3. [docs/SaaS_Playbook_Reference.md](file:///d:/Food-Packaging-AI/docs/SaaS_Playbook_Reference.md)
4. [docs/Rules.md](file:///d:/Food-Packaging-AI/docs/Rules.md)
5. [docs/Phases.md](file:///d:/Food-Packaging-AI/docs/Phases.md)

---

# Decision Recording
Record all architectural, scientific, and data schema choices in:
- `CLAUDE.md` (high-level stack and principles)
- `docs/Memory.md` (chronological decision log with context, decision, alternatives, and consequences)

---

# Known Unknowns
1. **Dynamic Shelf-Life Kinetics**: Mathematical modeling of moisture sorption isotherms (GAB equation) across dynamic ambient humidity shifts is currently open and marked for prototype simplification.
2. **Cultivar-Specific Respiration Rates**: Variability in respiration rates across produce cultivars and maturity stages requires curated range representations rather than single-point estimates.
3. **Pore-Diffusion Micro-Perforation Calculations**: Exact mathematical sizing of perforation diameter/frequency per packaging surface area requires further empirical validation.
4. **Multi-Criteria Optimization Weights**: Relative weighting between barrier performance, carbon footprint, recyclability, and economic cost needs human stakeholder calibration.

---

## Git Workflow
* main is the primary branch.
* Never force-push.
* Never commit secrets.
* Implementation tasks must be verified before shipping.
* Use scripts/git-ship.ps1 for the controlled commit/push workflow.
* Do not push unfinished work.

