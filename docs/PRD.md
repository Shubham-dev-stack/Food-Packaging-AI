# Product Requirements Document (PRD)

**Project Name:** AI-Based Intelligent Food Packaging Material Recommendation System for Food Commodities  
**Problem Statement ID:** SIH26236  
**Document Status:** Ready for Review (Planning-First Phase)  
**Primary Source:** [docs/Problem_Statement.md](file:///d:/Food-Packaging-AI/docs/Problem_Statement.md)  
**Scientific Foundation:** [docs/Research_and_Evidence.md](file:///d:/Food-Packaging-AI/docs/Research_and_Evidence.md)  
**Engineering Methodology:** [docs/SaaS_Playbook_Reference.md](file:///d:/Food-Packaging-AI/docs/SaaS_Playbook_Reference.md)  

---

## 1. Product Overview

The **AI-Based Intelligent Food Packaging Material Recommendation System** is an intelligent decision-support software platform designed to recommend optimal packaging materials and technical packaging specifications for food commodities.

### 1.1 What the System Is
The product is a domain-guided **decision-support system** that evaluates food physical, chemical, and biological properties alongside environmental and distribution conditions. It matches these requirements against a curated packaging material knowledge base to generate transparent, scientifically defensible packaging recommendations.

### 1.2 What Problem It Solves
Selecting proper food packaging currently demands specialized packaging engineering and food technology expertise. Small food processors, farmers, regional startups, and local manufacturers often lack access to packaging laboratories and technical barrier data. Consequently, improper packaging choices cause severe post-harvest losses, moisture ingress, lipid rancidity, premature spoilage, microbial growth, and economic waste.

### 1.3 Who It Helps
The platform directly empowers:
- **Farmers and agricultural producer organizations:** Preserving fresh produce post-harvest and selecting appropriate breathable/MAP packaging.
- **Small food industries and local manufacturers:** Specifying barrier films (OTR, WVTR, gauge) for packaged goods without expensive consultant fees.
- **Food startups:** Comparing sustainable, recyclable, and conventional barrier alternatives during early product packaging design.
- **Packaging and food science researchers:** Simulating barrier matching rules and validating technical criteria against benchmark food commodities.

### 1.4 Nature of the System
The system is explicitly an **evidence-backed decision-support tool**. It assists human users in narrowing down material options and understanding key barrier constraints. It **does not** claim to replace empirical laboratory validation, certified shelf-life testing, or regulatory food-contact migration assays.

---

## 2. Problem Statement

As established by SIH Problem Statement **SIH26236**:
- **Critical Role of Packaging:** Packaging is essential to maintain the quality, safety, nutritional integrity, and shelf life of food commodities during storage, transport, and retail distribution. Different commodities possess distinct physical, chemical, and biological sensitivities.
- **Consequences of Suboptimal Packaging:** Inappropriate material selection leads to moisture absorption, lipid auto-oxidation, microbial spoilage, texture degradation, flavor/nutrient loss, and drastic shelf-life reduction.
- **Industry Knowledge Barrier:** Currently, packaging selection is predominantly manual and dependent on scarce packaging specialists. Small enterprises, farmers, and startups lack actionable technical knowledge regarding barrier properties, gas permeabilities, sealability, and food-packaging interactions.
- **Produce Respiration Complexity:** Fresh fruits and vegetables continue active respiration post-harvest. Controlling oxygen ($\text{O}_2$) influx and carbon dioxide ($\text{CO}_2$) accumulation across packaging films is critical. Inadequate gas exchange leads to anaerobic fermentation, off-flavors, or cellular breakdown.
- **Need for Intelligent Decision Support:** There is a defined national need for an intelligent software system that analyzes commodity properties and environmental requirements to recommend optimized, sustainable, and cost-effective packaging materials and technical specifications.

---

## 3. Target Users

The SIH problem statement identifies 5 primary user groups:

| User Group | Primary Goal | Key Inputs Provided | Expected Output | Major Pain Point |
| :--- | :--- | :--- | :--- | :--- |
| **Farmers & FPOs** | Prevent post-harvest spoilage and weight loss in fresh horticultural produce during storage and transit. | Commodity type (e.g. tomatoes, apples), ambient/chilled temperature, transit conditions. | Respiration-compatible packaging (breathable/perforated), target gas composition for MAP, recommended storage conditions. | Lack of technical understanding of produce respiration, resulting in produce rotting inside airtight polythene bags. |
| **Small Food Industries** | Package dry, fried, or processed goods with reliable ambient or refrigerated shelf life. | Commodity type, moisture %, fat %, target shelf life (days), ambient humidity. | Suitable laminate/film material (e.g., metallized film, HDPE), required OTR and WVTR thresholds, recommended thickness. | Reliance on trial-and-error packaging from local converters without understanding technical barrier specifications. |
| **Food Startups** | Launch novel packaged food products with modern, eco-friendly, or recyclable packaging. | Product properties, desired shelf life, sustainability preferences. | Recyclable mono-material or biodegradable alternatives, barrier trade-offs, relative cost index. | High risk of launching with biodegradable films that lack necessary water vapor barriers, causing premature product failure. |
| **Local Manufacturers** | Standardize bulk and retail packaging across regional distribution networks. | Batch commodity type, handling/transport stress, storage mode (frozen, chilled, ambient). | Mechanical strength requirements, puncture resistance, sealability specs, primary packaging structure. | Product damage and seal bursting during rough transit over unpaved routes. |
| **Packaging Researchers** | Validate packaging rules, evaluate alternative barrier materials, and benchmark specs. | Granular commodity attributes ($a_w$, pH, respiration rate $R$), custom storage profiles. | Multi-candidate ranking, barrier gap analysis, evidence citations, scientific reference metadata. | Fragmented packaging data scattered across disparate literature sources and commercial data sheets. |

---

## 4. Product Goals

The product must achieve the following core objectives:
1. **Intelligent Material Recommendation:** Automatically evaluate commodity and environmental inputs to suggest suitable packaging materials from supported material classes.
2. **Barrier Requirement Specification:** Recommend quantitative, standards-aligned technical barrier specifications, specifically Oxygen Transmission Rate (OTR) and Water Vapor Transmission Rate (WVTR).
3. **Comprehensive Specification Delivery:** Provide supporting physical specifications: nominal film thickness, sealability criteria, gas permeability, mechanical strength, and MAP suitability.
4. **Respiration-Aware Produce Logic:** For respiring horticultural crops, provide respiration-aware packaging logic, evaluating breathable or micro-perforated films and safe equilibrium MAP guidelines.
5. **Transparent Explainability:** Provide human-readable, evidence-linked explanations for every recommendation, displaying why candidate materials were selected or disqualified.
6. **Sustainability & Eco-Friendly Evaluation:** Present recyclability classifications (mono-material vs multi-material laminates) and indicative environmental metrics to promote sustainable packaging alternatives.
7. **Accessibility & Usability:** Deliver an intuitive, responsive interface usable by non-technical operators (farmers, startups) as well as packaging professionals.

*(Note: Explicit numerical targets such as "95% recommendation accuracy" or "30% food waste reduction" are excluded at this stage because empirical validation metrics are **TBD** pending scientific benchmarking).*

---

## 5. Non-Goals

To maintain scientific credibility and prevent unsupported engineering claims, the initial system explicitly does **NOT** promise:
1. **Laboratory Testing or Empirical Validation:** The system does not conduct physical barrier tests or substitute for accredited laboratory testing (e.g., ASTM D3985, ASTM F1249).
2. **Guaranteed Shelf-Life Certification:** The system does not provide legal warranties or commercial guarantees of product shelf life.
3. **Food-Contact Regulatory Certification:** Recommending a polymer class (e.g., LDPE) does not certify that a specific commercial film lot complies with FSSAI, US FDA 21 CFR, or EU 10/2011 migration standards.
4. **Universal MAP Gas Compositions:** The system does not apply a single default gas mixture across all produce, recognizing that gas tolerance is strictly cultivar-dependent.
5. **Fabrication of Unverified Scientific Thresholds:** Where peer-reviewed scientific data for a specific crop or material is unavailable, the system will not guess or extrapolate.
6. **Live Industrial Resin Market Pricing:** The system will not integrate live commodity exchange pricing feeds; cost evaluations are restricted to normalized relative indices.
7. **Physical IoT Sensor Hardware Integration:** The system will not require or interface with physical IoT sensor hardware or RFID probes in this prototype phase.
8. **Dynamic Laboratory-Grade Differential Simulation:** Full dynamic non-isothermal finite-element diffusion modeling across fluctuating cold-chain cycles is deferred to future research phases.

---

## 6. Core User Journey

The primary end-to-end user workflow follows a clean, deterministic progression:

```
[1. Commodity Selection] 
       │
       ▼
[2. Parameter Input & Customization] (Moisture, Fat %, pH, Respiration, Shelf Life)
       │
       ▼
[3. Storage & Transit Environment Definition] (Temperature, RH, Ambient/Chilled/Frozen, Transit Stress)
       │
       ▼
[4. Input Validation & Sanity Check] ──(Invalid/Out-of-Bounds)──> [Error / Guidance State]
       │ (Valid)
       ▼
[5. Recommendation Engine Evaluation] (Barrier Calculation, Produce Respiration Branching)
       │
       ▼
[6. Candidate Material Filtering & Multi-Criteria Ranking]
       │
       ▼
[7. Results Presentation]
       ├─ Primary Recommended Packaging Material
       ├─ Alternative Materials (e.g. Eco-Friendly / Recyclable Alternative)
       ├─ Technical Packaging Specifications (OTR, WVTR, Thickness, Sealability, Mechanical Strength)
       ├─ Produce / MAP Guidance (if applicable)
       └─ Traceable Scientific Explanation Card & Evidence References
       │
       ▼
[8. Export / Traceability] (Optional specification summary / QR metadata export)
```

---

## 7. Product Inputs

The product input model directly incorporates all parameters mandated by SIH Problem Statement SIH26236:

| # | Input Parameter | Purpose | Required / Optional | Unit / Format | Validation Rules | Scientific Context & Notes |
|---|-----------------|---------|---------------------|---------------|------------------|----------------------------|
| 1 | **Commodity Type** | Primary entity key for auto-populating baseline scientific attributes. | **Required** | Selection from curated catalog (or Custom commodity option) | Must exist in reference catalog or supply custom baseline. | Baseline data sourced from USDA / FAO / ICAR compendiums. |
| 2 | **Moisture Content** | Evaluates moisture gain/loss risk and water activity driving force. | **Required** | Percentage (% by weight, 0.0–100.0%) | $0.0 \le \text{value} \le 100.0$ | Auto-populated by commodity; editable by user. |
| 3 | **Oil / Fat Content** | Evaluates sensitivity to lipid oxidation and light degradation. | **Required** | Percentage (% by weight, 0.0–100.0%) | $0.0 \le \text{value} \le 100.0$ | High fat triggers low OTR and light/UV barrier requirement. |
| 4 | **pH Level** | Determines microbial pathogen vulnerability and acid corrosion risk. | **Required** | Decimal (1.0–14.0) | $1.0 \le \text{value} \le 14.0$ | $pH < 4.6$ categorized as high-acid; $pH \ge 4.6$ low-acid (botulism risk in anaerobic packs). |
| 5 | **Respiration Rate** | Governs gas exchange requirements for fresh horticultural produce. | **Required for Produce**; N/A for non-respiring | Numeric ($\text{mg CO}_2 \cdot \text{kg}^{-1} \cdot \text{h}^{-1}$) or Qualitative class | Must be $\ge 0.0$; auto-disabled if commodity is non-respiring. | Temperature-dependent ($5^\circ\text{C}$ vs $20^\circ\text{C}$). Sourced from USDA Handbook 66. |
| 6 | **Desired Shelf Life** | Target duration the packaging must preserve commodity quality. | **Required** | Integer (Days or Months) | Integer $> 0$; realistic bounds defined per commodity category. | Higher shelf life tightens barrier thresholds (lower OTR/WVTR). |
| 7 | **Storage Temperature** | Dictates gas permeation flux and biological/chemical reaction kinetics. | **Required** | Degrees Celsius ($^\circ\text{C}$) | Range $-30.0^\circ\text{C} \le T \le 50.0^\circ\text{C}$ | Drives Arrhenius permeation and $Q_{10}$ respiration scaling. |
| 8 | **Relative Humidity (RH)** | Establishes the vapor pressure differential driving water vapor ingress/loss. | **Required** | Percentage (% RH, 0.0–100.0%) | $0.0 \le \text{value} \le 100.0$ | High ambient RH accelerates moisture uptake in dry goods. |
| 9 | **Transportation Conditions** | Determines mechanical resilience, puncture resistance, and seal integrity. | **Required** | Enum: `Local Standard`, `Long-Haul Refrigerated`, `Rough Terrain / Unpaved` | Valid enum selection | Rough terrain increases tensile, puncture, and tear requirements. |
| 10| **Storage Type** | Macro temperature classification mandated by SIH statement. | **Required** | Enum: `Ambient`, `Chilled`, `Frozen` | Valid enum selection | `Frozen` enforces low-$T_g$ polymer flexibility; `Chilled` requires anti-fog awareness. |

---

## 8. Product Outputs

For every valid recommendation query, the system must produce a structured output package:

### 8.1 Primary Material Recommendation
- **Recommended Material Identity:** Specific material structure (e.g. *Biaxially Oriented PET / LDPE Laminate*, *Metallized BoPET / PE*, *Micro-Perforated LDPE*).
- **Material Classification:** Monolayer film, coextrusion, metallized film, foil laminate, biodegradable/compostable, or breathable membrane.
- **Suitability Score / Status:** Clear confirmation of barrier compatibility against the commodity's decay mechanisms.

### 8.2 Technical Packaging Specifications
The system must provide quantitative and standards-referenced technical specifications:
1. **Oxygen Transmission Rate (OTR):** Target specification expressed in $\text{cm}^3 / (\text{m}^2 \cdot \text{day} \cdot \text{atm})$ referenced to standard test conditions (**ASTM D3985**, $23^\circ\text{C}$).
2. **Water Vapor Transmission Rate (WVTR):** Target specification expressed in $\text{g} / (\text{m}^2 \cdot \text{day})$ referenced to standard gradient conditions (**ASTM F1249**, $37.8^\circ\text{C}, 90\%\text{ RH}$).
3. **Film Thickness:** Recommended nominal gauge expressed in micrometers ($\mu\text{m}$) or Mils (**ASTM D6988**).
4. **Sealability:** Heat seal rating, recommended seal initiation window, and seal strength expectations (**ASTM F88**).
5. **Gas Permeability & Selectivity:** Permeability notes and required permselectivity ($\text{CO}_2/\text{O}_2$) for gas-sensitive or respiring products (**ASTM D1434**).
6. **Mechanical Strength:** Tensile strength (**ASTM D882**), Elmendorf tear resistance (**ASTM D1922**), and puncture resistance (**ASTM F1306**) ratings based on transit profile.
7. **Modified Atmosphere Packaging (MAP) Suitability:** Binary suitability indicator (`Suitable`, `Not Recommended`, `Ventilated Only`, or `Conditional`) with technical justification.

### 8.3 Fresh Produce & MAP Specific Outputs
When the commodity is an actively respiring horticultural item:
- **Respiration Consideration:** Produce respiration category and temperature-adjusted respiration intensity.
- **Packaging Structure Recommendation:** Specific recommendation between micro-perforated films, macro-ventilated packages, or high-breathability membranes.
- **Target Equilibrium MAP Gas Composition:** Recommended internal headspace concentrations ($\% \text{O}_2$ and $\% \text{CO}_2$, balance $\text{N}_2$) **strictly where verified commodity evidence exists**.
- **Critical Safety Ceilings:** Cultivar-specific lower $\text{O}_2$ fermentation threshold and upper $\text{CO}_2$ injury limit. If evidence is absent, the system displays `[RESEARCH REQUIRED]` rather than fabricating a gas mixture.

### 8.4 Alternative & Eco-Friendly Options
- **Sustainable / Recyclable Alternative:** Recommends recyclable mono-material structures (e.g. BoPE/PE) or certified industrially compostable films (e.g. PLA/PBAT) where technically viable.
- **Trade-Off Summary:** Clear comparison between conventional barrier performance and eco-friendly alternatives (highlighting moisture barrier limitations where applicable).

---

## 9. Recommendation Explanation

Explainability is a mandatory, first-class requirement of the decision-support system. Every recommendation must feature a dedicated **Explanation Card** answering the user's implicit question: *"Why did the system recommend this packaging?"*

The explanation must communicate:
1. **Dominant Spoilage Driver:** Which commodity property drove the primary constraint (e.g., *"High fat content (28%) makes lipid oxidation the primary decay pathway, demanding an OTR < 2.0"*).
2. **Environmental Impact:** How storage conditions influenced the recommendation (e.g., *"High ambient humidity (85% RH) at 30°C necessitates a high moisture barrier to prevent soggy texture"*).
3. **Candidate Disqualification Rationale:** Why alternative common materials were rejected (e.g., *"Plain LDPE was rejected because its high oxygen transmission (7,000 cm³) would cause rancidity within 14 days"* or *"Neat PLA was disqualified due to high water vapor transmission (200 g/m²·day)"*).
4. **Underlying Assumptions & Standards:** Explicitly lists the ASTM standards and scientific literature citations backing the recommendation.

---

## 10. Uncertainty & Evidence Handling

The system must never guess, hallucinate, or fabricate packaging data. When user inputs or knowledge base entries involve incomplete data, the system must transition into explicit, transparent operational states:

```
+───────────────────────────────────────────────────────────────────────────────+
| RECOMMENDATION STATE MODEL                                                    |
+───────────────────────────────────────────────────────────────────────────────+
| 1. Supported Recommendation  | Full scientific evidence & barrier data exist. |
| 2. Conditional Recommendation| Valid recommendation, but subject to specific  |
|                              | environmental or transit caveats.              |
| 3. Insufficient Evidence     | Critical property missing; system prompts user |
|                              | for required parameter before recommending.    |
| 4. Research Required         | Commodity/material lacks published postharvest |
|                              | or barrier literature; transparently flagged.  |
+───────────────────────────────────────────────────────────────────────────────+
```

### 10.1 Out-of-Bounds & Conflicting Input Handling
- If a user inputs impossible physical values (e.g., moisture $>100\%$, $pH < 0$ or $>14$, storage temperature $>60^\circ\text{C}$), the system displays immediate inline validation blocking evaluation.
- If a user selects conflicting parameters (e.g., Storage Type = `Frozen` but Storage Temperature = `25°C`), the system highlights the logical contradiction and requests correction.

---

## 11. Fresh Produce Requirements

Because fresh fruits and vegetables are living, respiring biological entities, the system enforces evidence-grounded domain rules:
1. **Respiration-Driven Branching:** Whenever an input commodity is marked as respiring, the system activates produce respiration logic, evaluating the coupled interaction of commodity respiration rate, produce mass, package surface area, free headspace volume, storage temperature, and film gas transmission rates.
2. **Prohibition of Universal Gas Mixtures:** The system strictly rejects applying a universal gas mixture across all fresh produce. Gas recommendations are mapped strictly to documented postharvest literature. Where data is absent, the system returns `[RESEARCH REQUIRED]`.
3. **Commodity- and Condition-Dependent Packaging:** Packaging candidates are evaluated based on whether film transmission rates can maintain internal oxygen above the cultivar's critical extinction threshold without inducing toxic carbon dioxide accumulation. Continuous barrier films are disqualified only when mass-transfer calculations show they fail this criterion for the specific crop and packaging geometry, rather than by a blanket disqualification rule.
4. **Breathable & Micro-Perforated Sizing:** The system evaluates micro-perforated or breathable films for medium-to-high respiration produce where pore diffusion ($\text{CO}_2/\text{O}_2 \approx 0.81$) prevents toxic $\text{CO}_2$ buildup while limiting transpirational desiccation.
5. **Anti-Fog Property Guidance:** For chilled produce subject to retail temperature variations, the system recommends packaging with anti-fog surface treatments to prevent condensation droplets that encourage mold growth.

---

## 12. Packaging Material Coverage

The system must support the 7 material families explicitly enumerated in SIH Problem Statement SIH26236:

| Material Family | SIH Status | Domain Role & Coverage in System | Primary Scientific Caveat |
| :--- | :--- | :--- | :--- |
| **Low-Density Polyethylene (LDPE)** | Explicitly Named | Moisture barrier, heat-sealing layer, fresh produce bags, frozen food packaging. | High gas permeability; unusable alone for oxygen-sensitive shelf-stable goods. |
| **High-Density Polyethylene (HDPE)** | Explicitly Named | High moisture barrier, rigid bottles, cereal liners, dry powder packaging. | Moderate gas permeability; translucent/milky opacity. |
| **Polyethylene Terephthalate (PET/BoPET)** | Explicitly Named | High tensile strength, optical clarity, aroma barrier, outer printing laminate web. | Poor heat sealability to itself; requires a sealant inner web (PE/PP). |
| **Metallized Films (MET-PET, MET-BOPP)** | Explicitly Named | Snack foods, potato chips, biscuits, confectionery; high light/gas/moisture barrier. | Vulnerable to flex-cracking; barrier degrades if pinholed or creased. |
| **Aluminum Foil Laminates (PET/Alu/PE)** | Explicitly Named | Retort pouches, infant milk powder, pharmaceuticals; near-absolute gas/moisture barrier. | Non-recyclable in standard mechanical recycling; high embodied energy. |
| **Biodegradable Films (PLA, PBAT, Blends)**| Explicitly Named | Short-shelf-life produce trays, organic dry food bags, compostable packaging. | High WVTR ($>10\times$ LDPE); requires industrial composting ($>58^\circ\text{C}$). |
| **Breathable & Microporous Films** | Explicitly Named | Actively respiring fresh vegetables, cut salads, mushrooms; controlled gas exchange. | Zero barrier to moisture and external contaminants; specialized produce use only. |

---

## 13. Packaging Specification Requirements

The recommendation output must provide technical clarity across 7 core specification dimensions:

### 13.1 Oxygen Transmission Rate (OTR)
- **Presentation:** Supported requirement range or target cutoff expressed in $\text{cm}^3 / (\text{m}^2 \cdot \text{day} \cdot \text{atm})$ at $23^\circ\text{C}$ (**ASTM D3985**).
- **Functional Importance:** Prevents oxidative rancidity in fats, color fading, and aerobic microbial growth.

### 13.2 Water Vapor Transmission Rate (WVTR)
- **Presentation:** Supported requirement range or target cutoff expressed in $\text{g} / (\text{m}^2 \cdot \text{day})$ at $37.8^\circ\text{C}, 90\%\text{ RH}$ (**ASTM F1249**).
- **Functional Importance:** Prevents crispness loss, staling, moisture caking in powders, or dehydration in fresh items.

### 13.3 Film Thickness
- **Presentation:** Recommended nominal gauge expressed in micrometers ($\mu\text{m}$) or Mils (**ASTM D6988**).
- **Functional Importance:** Balances permeation resistance against packaging material mass, conversion cost, and seal thermal transfer.

### 13.4 Sealability & Seal Integrity
- **Presentation:** Categorical rating (`Excellent`, `Good`, `Critical`) and recommended seal type (e.g. Heat Seal, Ultrasonic, Lap/Fin Seal) with reference to **ASTM F88**.
- **Functional Importance:** Guarantees hermetic package closure and prevents ambient air ingress through micro-channels.

### 13.5 Gas Permeability & Selectivity
- **Presentation:** Permselectivity ratio ($\beta = \text{CO}_2/\text{O}_2$) and gas permeability notes (**ASTM D1434**).
- **Functional Importance:** Critical for fresh produce EMAP to balance $\text{O}_2$ influx against $\text{CO}_2$ venting.

### 13.6 Mechanical Strength
- **Presentation:** Minimum tensile strength (MPa, **ASTM D882**), tear resistance (**ASTM D1922**), and puncture resistance (**ASTM F1306**) ratings based on transit profile.
- **Functional Importance:** Prevents package bursting, tearing, or pinholing during handling, stacking, and rough transit.

### 13.7 MAP Suitability
- **Presentation:** Status indicator (`Suitable`, `Not Recommended`, `Ventilated Only`, or `Conditional`) with gas flush compatibility notes (**ASTM F2096**).
- **Functional Importance:** Indicates whether the packaging material and hermetic format can maintain an altered atmosphere without collapse.

---

## 14. Optional Features & Phase Classification

SIH Problem Statement SIH26236 mentions several possible extension features: *"The proposed solution may further include shelf-life prediction, sustainability analysis, cost optimization, QR-based traceability, and eco-friendly packaging recommendations."*

These extensions are strictly categorized to preserve MVP focus:

| Feature Extension | SIH Description | PRD Phase Classification | Justification & Prototype Scope |
| :--- | :--- | :--- | :--- |
| **Eco-Friendly Recommendations** | Suggest recyclable / sustainable alternatives | **MVP** `[PROTOTYPE ASSUMPTION]` | Presenting recyclable mono-material alternatives alongside conventional multi-layer laminates is central to modern packaging decision-making. |
| **Sustainability Analysis** | Carbon & recyclability metrics | **MVP** (Indicative) `[PROTOTYPE ASSUMPTION]` | Displaying indicative recyclability classes (Mono-material PE vs Non-recyclable Foil Laminate) and indicative carbon indices. |
| **Cost Optimization** | Suggest cost-effective materials | **MVP** (Relative Index) `[PROTOTYPE ASSUMPTION]` | Normalized relative cost multiplier index (LDPE = 1.0) rather than volatile live currency values. |
| **QR-Based Traceability** | QR code generation for packaging specs | **MVP (Secondary / Export)** `[OPTIONAL]` | Generates a scannable QR code encoding the recommendation summary, target specs, and batch ID. |
| **Shelf-Life Prediction** | Predict product shelf life | **FUTURE SCOPE / TBD** | Dynamic kinetic non-isothermal modeling requires laboratory calibration. MVP will display empirical benchmark shelf life only. |

---

## 15. MVP Definition

The **SIH MVP** demonstrates end-to-end, scientifically defensible packaging recommendation without premature architectural or algorithmic complexity.

### 15.1 Core Value Delivery
```
Input Food & Storage Parameters ➔ Validate ➔ Evaluate Barrier & Respiration Needs ➔ Output Ranked Recommendations + Detailed Specs + Traceable Explanation
```

### 15.2 Explicit Prototype Assumptions `[PROTOTYPE ASSUMPTION]`
1. **Curated Benchmark Catalog:** The MVP includes a curated reference dataset of common agricultural and processed food commodities (fruits, vegetables, grains, fried snacks, dairy powder) to demonstrate breadth across all food categories.
2. **Standardized Material Catalog:** The MVP includes the 7 primary material families and representative commercial laminate structures.
3. **Relative Economic Multipliers:** Cost comparisons use normalized indices based on published polymer resin averages rather than real-time procurement feeds.
4. **Transparent Rule-Based / Multi-Criteria Evaluation:** The engine uses transparent, explainable multi-attribute matching and scoring rather than opaque black-box models.

---

## 16. Functional Requirements

### 16.1 Commodity & Input Management
- **FR-001 (MUST):** The system shall allow the user to select a commodity from a curated catalog or enter a custom commodity.
  - *Acceptance Criteria:* Selecting a catalog commodity automatically populates baseline values for moisture %, fat %, pH, and respiration rate.
- **FR-002 (MUST):** The system shall validate all numerical inputs against physical boundaries ($0 \le \text{moisture} \le 100\%$, $0 \le \text{fat} \le 100\%$, $1 \le pH \le 14$).
  - *Acceptance Criteria:* Out-of-bounds entries display immediate inline error messages and block recommendation generation.
- **FR-003 (MUST):** The system shall capture environmental conditions: storage temperature, relative humidity, transit stress, and storage type (`Ambient`, `Chilled`, `Frozen`).
  - *Acceptance Criteria:* Storage conditions are successfully factored into barrier requirements and material temperature constraints.

### 16.2 Recommendation Engine & Evaluation
- **FR-004 (MUST):** The system shall determine supported barrier requirement ranges (OTR and WVTR) based on commodity sensitivity and storage conditions.
  - *Acceptance Criteria:* Output displays evidence-backed target requirement ranges in ASTM-standardized units.
- **FR-005 (MUST):** The system shall branch into produce-specific respiration logic whenever an active respiring commodity is evaluated.
  - *Acceptance Criteria:* Respiring commodities trigger multi-factor gas balance evaluation (respiration, weight, pack geometry, permeability, temperature) and reject continuous barrier films when asphyxiation/fermentation risks exist.
- **FR-006 (MUST):** The system shall filter and rank candidate packaging materials, presenting the top recommended solution and viable alternatives.
  - *Acceptance Criteria:* Recommendations clearly identify the material structure, trade code, and suitability score.
- **FR-007 (MUST):** The system shall provide technical packaging specifications: OTR, WVTR, film thickness, sealability, gas permeability, mechanical strength, and MAP suitability.
  - *Acceptance Criteria:* Each specification card displays the value, unit, relevant ASTM testing standard, and functional rationale.

### 16.3 Explainability & Evidence
- **FR-008 (MUST):** The system shall generate an Explanation Card detailing why the top material was selected and why unsuitable candidates were rejected.
  - *Acceptance Criteria:* Explanation references the dominant degradation pathway, environmental driving force, and material barrier limits.
- **FR-009 (MUST):** The system shall link recommendations and barrier values to scientific literature references and ASTM test standards.
  - *Acceptance Criteria:* Users can inspect citation metadata for underlying scientific claims.
- **FR-010 (MUST):** The system shall transition into an explicit `Insufficient Evidence` or `Research Required` state if required parameters or crop data are unverified.
  - *Acceptance Criteria:* System refuses to fabricate unverified gas mixtures or barrier thresholds.

### 16.4 Optional & Extended Features
- **FR-011 (SHOULD):** The system should provide an eco-friendly/sustainable alternative alongside the primary recommendation, noting recyclability trade-offs.
  - *Acceptance Criteria:* Recyclable mono-material or compostable option is displayed with an objective comparison of barrier limitations.
- **FR-012 (SHOULD):** The system should display a relative cost index comparing recommended materials against baseline LDPE.
  - *Acceptance Criteria:* Economic comparison is explicitly labeled as an indicative relative index.
- **FR-013 (COULD):** The system could generate a scannable QR code containing the summary recommendation specifications and batch metadata.
  - *Acceptance Criteria:* Scanning the QR code displays the commodity name, recommended material, target OTR/WVTR, and storage instructions.
- **FR-014 (FUTURE):** The system may support dynamic shelf-life simulation based on mathematical kinetic decay equations.

---

## 17. Non-Functional Requirements

### 17.1 Usability & Accessibility
- **NFR-001:** Interface must provide clear tooltips explaining technical packaging terms (e.g. OTR, WVTR, MAP, $a_w$) for non-specialist users (farmers, small startups).
- **NFR-002:** The user interface must be fully responsive across mobile (minimum 375px width) and desktop screen viewports.
- **NFR-003:** Color schemes must maintain high contrast (WCAG 2.1 AA compliance) to ensure readability in field conditions.

### 17.2 Performance & Responsiveness
- **NFR-004:** Recommendation evaluation and output generation must complete within $\le 1.0\text{ second}$ for standard catalog queries under normal load.
- **NFR-005:** Input validation feedback must be instantaneous ($\le 100\text{ ms}$).

### 17.3 Reliability & System Integrity
- **NFR-006:** All domain calculations, barrier matching rules, and validations must execute on the backend; client-side state is strictly presentation-only.
- **NFR-007:** The system must handle unexpected or null data gracefully without unhandled exceptions or blank screens.

### 17.4 Evidence Traceability & Maintainability
- **NFR-008:** Every scientific rule and reference benchmark in the database must be traceable to a bibliographic source ID in the metadata table.
- **NFR-009:** Business logic and recommendation rules must remain decoupled from UI components and API route handlers.

---

## 18. Error & Edge Cases

| Edge Case Scenario | Expected System Behavior | User Communication |
| :--- | :--- | :--- |
| **Missing Required Input** | Evaluation button disabled; highlighted input field. | *"Please specify storage temperature to calculate permeation barrier requirements."* |
| **Physically Impossible Input** | Immediate inline validation error; field resets to acceptable bounds. | *"Moisture content must be between 0.0% and 100.0%."* |
| **Conflicting Storage Inputs** | System flags incompatibility (e.g. Frozen storage at $25^\circ\text{C}$). | *"Storage type 'Frozen' requires a temperature $\le -18^\circ\text{C}$."* |
| **Unsupported / Unknown Commodity** | System prompts user to input custom baseline attributes ($a_w$, fat %, respiration). | *"Commodity not in catalog. Please enter baseline moisture, fat, and respiration properties."* |
| **No Material Meets Strict Criteria** | System returns `Zero Matching Candidates` state; displays closest candidate with barrier deficit. | *"No single standard film satisfies these extreme barrier requirements. Consider a multi-layer foil laminate or adjust storage temperature."* |
| **High Respiration Crop in Chilled Storage** | System identifies condensation risk; enforces anti-fog and breathable/perforated film. | *"High respiration generates moisture condensation; anti-fog breathable film required to prevent mold."* |
| **Low-Acid Food in Reduced-Oxygen Packaging** | System checks pH $\ge 4.6$ under reduced-oxygen atmosphere; attaches contextual safety advisory on *Clostridium botulinum* hazard without claiming commercial safety certification. | *"Food Safety Notice: Low-acid food ($pH \ge 4.6$) packaged under reduced oxygen presents a botulism risk requiring licensed process validation (FDA 21 CFR 114 / FSSAI)."* |

---

## 19. Data & Evidence Requirements

The system mandates complete data auditability:
1. **Traceability of Property Values:** Every barrier transmission rate, respiration constant, and gas limit stored in the database must maintain an active relationship to a `reference_id` linking to peer-reviewed literature or standards documentation.
2. **Explicit Labeling of Assumptions:** Where empirical data is missing and an engineering estimate is used, the system interface must explicitly display the `[PROTOTYPE ASSUMPTION]` tag.
3. **Data Quality Governance:** Datasets must undergo peer review against official publications (USDA, FAO, ASTM) prior to ingestion.

---

## 20. Success Criteria

The success of the SIH prototype will be measured by testable functional and usability criteria:
- **Criterion 1 (Workflow Completion):** A user can complete the entire journey from commodity selection to recommendation display in $\le 5$ user interactions.
- **Criterion 2 (Input Validation Coverage):** 100% of out-of-bounds and contradictory inputs are caught and blocked before execution.
- **Criterion 3 (Domain Rule Accuracy):** 100% of respiring produce queries trigger multi-factor produce respiration evaluation (evaluating breathable/perforated films against continuous barrier films based on gas balance).
- **Criterion 4 (Explainability Completeness):** 100% of generated recommendations include an Explanation Card identifying the primary degradation driver and disqualified alternatives.
- **Criterion 5 (Safety Boundary Enforcement):** 100% of low-acid food queries under reduced-oxygen conditions display the contextual ROP safety advisory.
- **Criterion 6 (Traceability Display):** Every technical specification card displays the corresponding ASTM standard and measurement unit.

*(Quantitative claims of real-world food waste reduction or commercial shelf-life extension are marked **TBD** as they require post-hackathon commercial trials).*

---

## 21. SIH Demonstration Scope

The SIH live evaluation demonstration will prove the core capabilities through 4 dedicated benchmark scenarios:

1. **Scenario A: Moisture-Sensitive Dry Commodity (Potato Chips / Biscuits):**
   - Inputs: High fat ($30\%$), low moisture ($2\%$), ambient storage ($30^\circ\text{C}, 80\%\text{ RH}$), 180 days shelf life.
   - Demonstration: Engine specifies low OTR and low WVTR; selects **Metallized Film (MET-PET/PE)**; rejects plain LDPE due to oxygen permeability; explains crispness staling risk.
2. **Scenario B: High-Respiration Fresh Produce (Broccoli / Mushrooms):**
   - Inputs: Respiring vegetable, high respiration rate, chilled storage ($4^\circ\text{C}$), 14 days shelf life.
   - Demonstration: Engine identifies produce respiration; evaluates gas balance under package dimensions; identifies asphyxiation risk for continuous barrier films; recommends **Micro-Perforated LDPE / Breathable Film**; displays target equilibrium gas composition ($1-2\%\text{ O}_2, 5-10\%\text{ CO}_2$); explains risk of sulfurous off-odors.
3. **Scenario C: Acidic Processed Food (Tomato Ketchup / Citrus Juice):**
   - Inputs: High acid ($pH = 3.8$), moderate moisture, ambient storage.
   - Demonstration: System confirms absence of anaerobic *C. botulinum* risk; evaluates acid corrosion and oxygen barrier; recommends PET/PE or glass/rigid alternative; explains delamination resistance.
4. **Scenario D: Eco-Friendly / Recyclable Trade-Off:**
   - Inputs: User selects eco-friendly preference for dry cereal packaging.
   - Demonstration: System compares recyclable mono-material BoPE/PE against conventional multi-layer laminates; displays recyclability classification and relative cost index.

---

## 22. Future Scope

The following capabilities are excluded from the initial prototype and formally reserved for future phases:
- **Phase 2:** Dynamic kinetic shelf-life prediction algorithms integrating non-isothermal cold-chain fluctuations.
- **Phase 3:** Automated laser micro-perforation density sizing calculator based on produce mass and pack geometry.
- **Phase 4:** Live API integration with raw polymer resin market pricing (ICIS) and regional packaging converter databases.
- **Phase 5:** Enterprise multi-tenant packaging audit portal with automated export regulatory compliance checks (FSSAI / US FDA / EU).
- **Phase 6:** IoT smart sensor integration (time-temperature indicators, RFID cold-chain loggers).

---

## 23. Assumptions & Open Questions

### 23.1 Prototype Assumptions `[PROTOTYPE ASSUMPTION]`
1. **Curated Baseline Data:** Curated catalog of benchmark commodities represents valid general baselines for testing, recognizing cultivar variations.
2. **Simplified Packaging Geometries:** Package surface-area-to-volume ratio ($A/V$) is assumed to follow standard commercial packaging pouch dimensions unless customized.
3. **Relative Economic Weights:** Normalized cost indices represent indicative economic relationships, not commercial binding quotes.

### 23.2 Open Questions & Research Gaps (From Research & Evidence)
1. **Closed-Form Shelf-Life Cutoff Equations:** Establishing exact closed-form algebraic equations mapping target shelf-life days to precise OTR/WVTR numerical cutoffs remains an active research item.
2. **Thickness Optimization Heuristics:** Balancing barrier permeation ($J \propto 1/l$) against mechanical puncture resistance and converter line sealability requires standardized heuristic rules.
3. **Cultivar-Specific Respiration Uncertainty:** Managing wide biological variances in crop respiration within a single user-friendly slider interface.

---

## 24. Scientific Safety Boundary

> **MANDATORY NOTICE ON DECISION SUPPORT AND REAL-WORLD IMPLEMENTATION**

1. **Decision Support, Not Laboratory Certification:** The system operates strictly as an intelligent decision-support tool. Recommendations generated by the software do not constitute certified laboratory test results or regulatory approvals.
2. **Requirement for Physical Verification:** All suggested packaging structures, barrier specifications, and gas compositions must undergo physical verification prior to commercial packaging:
   - Accelerated Shelf-Life Testing (**ASLT**) under controlled environmental chambers.
   - Seal integrity and leak testing (**ASTM F2096**, **ASTM F1929**).
   - Real-world transit vibration simulation (**ASTM D4169**).
3. **Food Contact Safety Compliance:** Users must verify that commercial packaging films procured from converters hold certified regulatory compliance (FSSAI Packaging Regulations 2018 in India, US FDA 21 CFR 175–178, or EU Regulation 10/2011) for overall and specific migration limits.
4. **Contextual Reduced-Oxygen Packaging (ROP) Safety Advisory:** Low-acid foods ($pH \ge 4.6$) packaged under reduced-oxygen conditions present a recognized risk of *Clostridium botulinum* intoxication. The system displays contextual warnings and notes that commercial implementation mandates validated multi-hurdle controls (retort sterilization, acidification, water activity controls, or strict cold chain below $3^\circ\text{C}$). The software does not provide commercial process safety certification.
