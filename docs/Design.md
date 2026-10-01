# UX/UI Design Specification: Food Packaging Decision-Support System

**Document Type:** UX/UI Design Specification  
**Problem Statement ID:** SIH26236  
**Primary Source:** [docs/Problem_Statement.md](file:///d:/Food-Packaging-AI/docs/Problem_Statement.md)  
**Product Requirements:** [docs/PRD.md](file:///d:/Food-Packaging-AI/docs/PRD.md)  
**System Design:** [docs/System_Design.md](file:///d:/Food-Packaging-AI/docs/System_Design.md)  

---

## 1. Design Philosophy: Decision-Support, Not a Chatbot

The interface is intentionally designed as an **expert decision-support workstation**, not an open-ended AI chatbot. 
- **Clarity Over Novelty:** Structured forms, parameter sliders, clear unit labels, and visual specification badges.
- **Immediate Feedback:** Selecting a commodity immediately previews standard biological/chemical baseline values.
- **Explainability Front and Center:** Users are never presented with a naked recommendation without an associated Explanation Card and standards citation.
- **Accessibility & Field Readiness:** High-contrast color palette, readable typography, and responsive touch-friendly targets for mobile devices in agricultural pack-houses.

---

## 2. Information Architecture & Navigation

The application consists of a single cohesive workflow layout with 3 key views:

```
+─────────────────────────────────────────────────────────────────────────────+
| HEADER: App Title | Benchmark Presets | Evidence Library Modal | About / Docs|
+─────────────────────────────────────────────────────────────────────────────+
|                                                                             |
|  LEFT PANEL: Input Workspace (40%)     │  RIGHT PANEL: Results Dashboard (60%)
|  ───────────────────────────────────── │  ──────────────────────────────────
|  1. Commodity Selector & Baseline      │  [State: Ready / Results / Alert]  
|     - Category Filter (Produce, Dry...)│  1. Primary Recommended Material   
|     - Crop / Item Dropdown             │     - Structure, Trade Code, Score 
|     - Auto-populated baseline preview  │  2. Technical Specifications Card  
|  2. Food Property Sliders & Inputs     │     - OTR, WVTR, Gauge, Sealability
|     - Moisture % | Fat % | pH          │     - Gas Permeability & Strength  
|     - Respiration Rate (Produce only)  │  3. Fresh Produce & MAP Advisory   
|  3. Storage & Transit Environment      │     - Headspace O2/CO2, Breathability
|     - Temperature (°C) Slider          │  4. Alternative & Sustainable Pack 
|     - Relative Humidity (% RH) Slider  │     - Recyclable Mono-material     
|     - Storage Mode (Ambient/Chill/Frz) │  5. Transparent Explanation Card   
|     - Transit Profile (Road/Rough)     │     - Dominant Spoilage Driver     
|  4. Recommendation Preferences         │     - Disqualified Materials Log   
|     - Target Shelf Life (Days)         │     - Scientific Citations Link    
|     - Eco-Friendly Priority Toggle     │  6. Actions: Export Spec / View QR 
|                                        │                                    
|  [ ACTION BUTTON: Generate Packaging ] │                                    
+─────────────────────────────────────────────────────────────────────────────+
```

---

## 3. Screen States & Core Components

### 3.1 Input Workspace Components
- **Commodity Picker:** Searchable dropdown categorized into *Fresh Produce*, *Dry & Fried Snacks*, *Dairy & Powders*, *Grains & Bakery*, and *Processed Foods*.
- **Baseline Preview Card:** When a commodity is selected, displays typical moisture, critical $a_w$, fat %, and pH with an "Override" toggle allowing manual adjustment.
- **Environmental Controls:**
  - Storage Temperature slider (range: $-25^\circ\text{C}$ to $45^\circ\text{C}$).
  - Relative Humidity slider (range: $20\%$ to $95\%\text{ RH}$).
  - Segmented toggle for Storage Type: `[ Ambient ]` `[ Chilled ]` `[ Frozen ]`.
  - Transit Severity selector: `[ Local Standard ]` `[ Refrigerated Long-Haul ]` `[ Rough Terrain ]`.

### 3.2 Results Dashboard Components
1. **Primary Material Banner:** Prominent display of recommended structure (e.g., *Metallized BoPET / PE Laminate (12 μm BoPET + 35 μm PE)*) with suitability badge.
2. **Technical Specifications Grid:**
   - **OTR Card:** Value in $\text{cm}^3 / (\text{m}^2 \cdot \text{day} \cdot \text{atm})$ + ASTM D3985 badge + rationale tooltip.
   - **WVTR Card:** Value in $\text{g} / (\text{m}^2 \cdot \text{day})$ + ASTM F1249 badge + rationale tooltip.
   - **Nominal Gauge Card:** Value in $\mu\text{m}$ (and mil) + thickness selection reasoning.
   - **Sealability & Mechanical Card:** Recommended seal type (Heat seal, $120-140^\circ\text{C}$), tensile and puncture ratings.
3. **Fresh Produce & MAP Panel (Conditional):**
   - Active only when commodity is respiring.
   - Displays recommended micro-perforation density, target headspace $\text{O}_2 / \text{CO}_2$ window, and warning against airtight barrier films.
4. **Explanation & Audit Card:**
   - Bulleted explanation of the primary decay mechanism.
   - Expandable "Disqualified Candidates" section explaining why conventional alternatives (e.g. plain LDPE or PLA) were rejected.
   - Bibliographic source citation pill (e.g. *Source: Robertson (2012), USDA Handbook 66*).
5. **QR Code Traceability Modal:**
   - Generates a clear vector QR code containing structured JSON of the packaging specification for converter handover.

---

## 4. Operational & Edge States

| State | Visual Presentation | User Guidance |
| :--- | :--- | :--- |
| **Empty State** | Clean illustration of food packaging; placeholder text in results panel. | *"Select a commodity and configure storage parameters to generate evidence-backed packaging recommendations."* |
| **Loading State** | Skeleton loaders mirroring the specification cards; animated status indicator. | *"Calculating barrier requirements & evaluating candidate polymers against ASTM standards..."* |
| **Validation Error State** | Red input border; inline error text below offending field; primary button disabled. | *"Temperature -10°C is invalid for 'Ambient' storage mode. Please select 'Frozen' or adjust temperature."* |
| **Insufficient Evidence State** | Amber banner; custom attribute form enabled. | *"Custom commodity lacks baseline water activity and fat content. Enter estimates to proceed with barrier calculation."* |
| **Botulism Safety Warning** | Prominent red warning banner with alert icon at top of results. | *"CRITICAL HAZARD: Low-acid food under anaerobic storage must be kept strictly below 3°C to prevent Clostridium botulinum toxin formation."* |

---

## 5. Responsive Behavior & Accessibility (WCAG 2.1 AA)

- **Mobile Viewport (375px+):** Layout collapses into a sequential 2-step tabbed view: `[ 1. Parameters ]` $\rightarrow$ `[ 2. Recommendation Results ]`. Sticky footer button triggers evaluation.
- **Keyboard Navigation:** Full tab-order navigation across all dropdowns, sliders, and modal triggers; visible focus rings (`ring-2 ring-primary-500`).
- **Contrast & Typography:** Strict adherence to 4.5:1 text-to-background contrast ratios for normal text; semantic HTML5 markup (`<main>`, `<section>`, `<article>`, `<label>`).
- **ARIA Attributes:** Screen-reader live regions (`aria-live="polite"`) for real-time validation alerts and result updates.
