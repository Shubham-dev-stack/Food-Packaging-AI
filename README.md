# AI-Based Intelligent Food Packaging Material Recommendation System for Food Commodities

**Smart India Hackathon (SIH 2026)**  
**Problem Statement ID:** SIH26236  
**Category:** Software | **Technology Bucket:** Agriculture, FoodTech & Rural Development  

---

## Project Overview

Packaging plays a critical role in preserving food quality, preventing moisture degradation, inhibiting lipid oxidation, suppressing microbial spoilage, and maintaining post-harvest shelf life. However, small food processors, farmers, startups, and local manufacturers often lack the packaging engineering expertise needed to evaluate barrier properties, gas permeability, and food-packaging interactions.

This project delivers an intelligent, evidence-backed **decision-support software system** that analyzes food commodity characteristics and storage/transportation environments to recommend optimal packaging materials, technical specifications (OTR, WVTR, film thickness, sealability, gas permeability, mechanical strength, and MAP suitability), and sustainable alternatives.

---

## Current Status: Phase 10 Complete (Production-Ready Prototype)

The system is fully implemented, verified, and hardened for SIH demonstration across **Phases 0 through 10**:
- **Pure Domain Physics Engine:** ASTM F1249/D3985 barrier modeling, Fonseca post-harvest respiration kinetics, and multi-criteria utility trade-off optimization.
- **REST API:** FastAPI application under canonical `/api` prefix, automated database initialization via lifespan hook, health/readiness probe, structured logging, and robust input validation.
- **Frontend Workstation:** Responsive React 19 + TypeScript + Tailwind CSS workspace with real-time constraint calculation, explainability panels, MAP produce workflows, and resilient timeout/retry error boundaries.
- **Test Coverage:** 100% verified test suite (85 backend unit/domain/smoke tests, 31 frontend component/integration tests).

---

## SIH Evaluator Quickstart Guide

Run the full system locally in two terminal windows:

### Prerequisites
- **Python 3.11+** (virtual environment recommended)
- **Node.js 18+** & `npm`

### 1. Backend Setup & Startup
```powershell
# From the repository root:
cd backend

# Setup virtual environment (if not already created)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# (Optional) Copy environment configuration
cp .env.example .env

# Run FastAPI backend (auto-initializes SQLite database & schema on boot)
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
* Backend API base URL: `http://127.0.0.1:8000/api`
* Interactive API Documentation (Swagger UI): `http://127.0.0.1:8000/docs`
* Health & Database Readiness Probe: `http://127.0.0.1:8000/api/health`

### 2. Frontend Setup & Startup
```powershell
# In a second terminal window, from repository root:
cd frontend

# Install npm packages
npm install

# Run Vite development server
npm run dev
```
* Frontend User Interface: `http://localhost:5173`

---

## Automated Verification & Test Commands

Run the comprehensive test suites across both tiers:

```powershell
# Run full backend test suite (85 tests covering domain physics, API contracts, invariants & smoke scenarios)
backend\.venv\Scripts\python.exe -m pytest backend/tests -v

# Run backend code quality & lint checks
backend\.venv\Scripts\python.exe -m ruff check backend data
backend\.venv\Scripts\python.exe -m ruff format --check backend data

# Run frontend test suite & typechecker
cd frontend
npm run typecheck
npm test
npm run build
```

---

## 4 Core SIH Demonstration Benchmark Scenarios

The system is tested end-to-end against 4 representative food commodity scenarios (`backend/tests/test_smoke.py`):

1. **Potato Chips (Crispy Snack, Moisture & Lipid-Oxidation Sensitive):**
   * *Regime:* Ambient, 25°C, 75% RH, 180 days.
   * *Output:* High-barrier metallized/aluminum foil laminate (`PET/ALU/PE` or `MET-PET/PE`), target WVTR < 5.0 g/(m²·day), target OTR < 10.0 cm³/(m²·day·atm), opaque light barrier enforced.
2. **Fresh Broccoli (High-Respiration Vegetable, Active MAP):**
   * *Regime:* Chilled, 4°C, 95% RH, 14 days.
   * *Output:* Laser micro-perforated film (`PERF-BOPP/PE`), adjusted respiration rate > 50 mg CO₂/(kg·h), equilibrium O₂ demand derived under coupled mass-balance to prevent anaerobic hypoxia.
3. **Uncharacterized Wild Produce (Research-Required Boundary):**
   * *Regime:* Respiring produce lacking peer-reviewed equilibrium gas recommendations.
   * *Output:* Explicit `[RESEARCH REQUIRED]` uncertainty warning without hallucinating or fabricating gas mixtures.
4. **Extreme / Unobtainable Constraints (Zero False Positives):**
   * *Regime:* Demands exceeding the barrier capabilities of the available catalog.
   * *Output:* Status `RESEARCH_REQUIRED`, clean enumeration of all disqualified materials with explicit engineering rejection reasons, zero fabricated candidates.

---

## Engineering Architecture & Tech Stack

```
d:/Food-Packaging-AI/
├── backend/                      # Python FastAPI application
│   ├── app/
│   │   ├── api/v1/               # REST endpoints (/api/commodities, /api/materials, /api/recommendations, /api/health)
│   │   ├── core/                 # App configuration (.env), DB engine, lifespan hook
│   │   ├── domain/               # Pure domain physics (ASTM barrier, Fonseca respiration, trade-off optimization)
│   │   ├── models/               # SQLAlchemy relational entities with foreign-key integrity
│   │   ├── repositories/         # Database access layer
│   │   ├── schemas/              # Pydantic validation models & schemas
│   │   └── services/             # Application orchestration and audit logging
│   └── tests/                    # 85 automated pytest test cases
├── frontend/                     # React 19 + TypeScript + Vite + Tailwind CSS
│   ├── src/
│   │   ├── components/           # Recommendation workspace, specifications grid, explainability panels
│   │   ├── pages/                # Main interactive Workspace
│   │   ├── services/api.ts       # Typed API client with 10s timeout & error classification
│   │   └── types/api.ts          # TypeScript interfaces mirror backend schemas
│   └── tests/                    # 31 Vitest component & integration tests
├── data/                         # Curated knowledge base
│   ├── processed/                # ASTM test standards, evidence citations, materials, commodities
│   └── knowledge_base/seed.py    # Idempotent database seeder
└── docs/                         # Formal architectural & domain documentation
```

---

## Decision-Support & Regulatory Notice

> [!IMPORTANT]
> **Advisory Nature:** This system is an intelligent decision-support software prototype designed to assist packaging technologists, food processors, and researchers by estimating indicative engineering specifications (OTR, WVTR, film gauge) from published food science literature and ASTM test standards.
> 
> **Commercial Validation:** Outputs generated by this software do NOT constitute formal regulatory compliance certificates (FSSAI, US FDA, EU EFSA). Commercial food distribution requires physical prototype laboratory testing under actual storage conditions (ASTM F1249, ASTM D3985, ASTM F1306, ASTM D4169, IS 9845 migration testing) and microbial challenge testing.

---

## Documentation Map

All core specifications and architectural decisions reside in the `docs/` directory:

| Document | Description |
| :--- | :--- |
| **[Problem Statement](docs/Problem_Statement.md)** | Verbatim SIH26236 problem statement (Primary product source of truth). |
| **[Research & Evidence](docs/Research_and_Evidence.md)** | Peer-reviewed food preservation physics, ASTM testing standards, and safety boundaries. |
| **[Product Requirements (PRD)](docs/PRD.md)** | Complete product scope, user personas, input/output schemas, and functional requirements. |
| **[System Design](docs/System_Design.md)** | Logical system flows, actor interactions, produce respiration branch, and state management. |
| **[Data Model](docs/Data_Model.md)** | Relational entities, physical units, data validation rules, and citation keys. |
| **[AI Recommendation Engine](docs/AI_Recommendation_Engine.md)** | Domain-guided constraint filtering, respiration physics, and multi-criteria utility ranking. |
| **[Architecture](docs/Architecture.md)** | Modular Monolith technical architecture (FastAPI + React/TypeScript + SQLite). |
| **[UX/UI Design](docs/Design.md)** | Decision-support workstation wireframes, component layouts, and accessibility standards. |
| **[Engineering Rules](docs/Rules.md)** | Guardrails against hallucinated data, secrets leakage, and test manipulation. |
| **[Implementation Phases](docs/Phases.md)** | 12-phase sequential engineering roadmap for implementation. |
| **[Testing & Security](docs/Testing_Security.md)** | Test pyramid, boundary test matrix, and security threat mitigations. |
| **[SIH Evaluation](docs/Evaluation.md)** | Hackathon jury criteria, measurable prototype metrics, and 3-min/5-min demo scripts. |
| **[Project Memory](docs/Memory.md)** | Persistent project state register and Architectural Decision Records (ADRs). |
| **[Agent Instructions (CLAUDE.md)](CLAUDE.md)** | Persistent guidelines, source hierarchy, and verification rules for AI agents. |

