# Commercial Real Estate — Organizational Process Map

> A comprehensive mapping of departments, roles, and their 289 facility management processes in a Nordic commercial real estate company. Each process is rated for AI automation potential.

## How to Read This Document

**Organization**: 6 departments → 18 roles → 289 processes

**Automation scale** (from the AI Automation Potential assessment):

| Tag | Meaning | Description |
|-----|---------|-------------|
| `FULL` | Fully automatable | AI can run end-to-end without human intervention |
| `LARGE` | Largely automatable | AI handles most work; human provides oversight or approval |
| `PARTIAL` | Partially automatable | AI assists with analysis/scheduling; human executes |
| `MANUAL` | Minimally automatable | Requires human judgment, negotiation, or physical work |

**Process ownership**: Each process is listed under its primary owner. Some processes span multiple departments — the primary accountable role is listed.

---

## Organizational Overview

```
Corporate Leadership
├── Chief Executive Officer (CEO)
├── General Counsel (CLO)
└── Investor Relations Director

Finance
├── Chief Financial Officer (CFO)
├── Investment Officer
├── Controller
└── Rent Administrator

Asset Management & Property Operations
├── Asset Manager
├── Business Developer
├── Property Manager
└── Leasing Manager

Technology & Sustainability
├── Technical Manager
├── Energy Strategist
└── Chief Digital Officer / Proptech Manager

Project Development
├── Project Manager
└── Urban Developer / Planning Strategist

Field Operations
├── Building Technician
└── Facilities Custodian
```

---

## 1. Corporate Leadership

Strategic direction, governance, and legal compliance for the real estate portfolio.

---

### Chief Executive Officer (CEO)

> Overall vision, board relations, capital allocation, and organizational development.
> **KPIs**: Total shareholder return (TSR), net asset value (NAV), corporate reputation.

The CEO owns enterprise-level strategic and cross-cutting processes.

**FM Strategy & Cross-Cutting**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| FM strategy and planning | Develop and execute overall FM strategy aligned with organizational objectives | Annual | `MANUAL` |  |
| Change management | Manage organizational change for new systems, processes, and workplace transformations | Per initiative | `MANUAL` |  |
| Stakeholder relationship management | Manage relationships with tenants, owners, vendors, regulators, and internal stakeholders | Ongoing | `MANUAL` |  |
| Business continuity planning | Develop and maintain business continuity plans for FM operations | Annual / As needed | `PARTIAL` |  |

---

### General Counsel (CLO)

> Legal compliance, contract management, due diligence, dispute resolution, and board governance.
> **KPIs**: Legal cost, risk exposure level, time-to-resolution for legal matters.

The General Counsel owns regulatory and compliance governance. Operational compliance execution is delegated to Technical Manager (see Dept 5).

**Quality & Compliance Governance**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Quality management system | Maintain ISO 41001 or equivalent QMS for FM operations | Ongoing | `PARTIAL` |  |

---

### Investor Relations Director

> Transparent communication with shareholders and analysts; annual reports, quarterly presentations, capital markets days.
> **KPIs**: Analyst rating, share liquidity, investor confidence index.

No FM operational processes are directly owned by this role. IR consumes outputs from Financial Reporting and ESG Reporting processes.

---

## 2. Finance

Financial strategy, capital markets, portfolio transactions, financial reporting, budgeting, and rent administration.

---

### Chief Financial Officer (CFO)

> Financing strategy, debt portfolio, capital allocation, risk management, and regulatory compliance (CSRD).
> **KPIs**: Loan-to-value (LTV), interest coverage ratio (ICR), average cost of debt.

The CFO owns strategic financial planning, budgeting, treasury, and investment analysis processes.

**Budgeting & Forecasting**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Operating budget development | Develop annual FM operating budget by building, category, and vendor | Annual | `LARGE` |  |
| Budget reforecasting | Update budget forecasts quarterly based on actuals and changed conditions | Quarterly | `LARGE` |  |

**Procurement & Spend**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Procurement and purchasing | Manage the procurement process for goods, services, and materials | Ongoing | `LARGE` |  |

**Lease & Tax**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Lease financial management | Manage financial aspects of leases: rent, escalations, options, terminations | Ongoing | `LARGE` |  |
| Tax and depreciation tracking | Track asset depreciation schedules and property tax implications | Ongoing | `LARGE` |  |
| Insurance claims management | Manage property damage and liability insurance claims | As needed | `PARTIAL` |  |

**Investment Analysis**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Cost-benefit analysis | Evaluate proposed projects or changes using CBA methodology | Per project | `PARTIAL` |  |
| ROI calculation for FM initiatives | Calculate and track return on investment for FM projects and programs | Per project | `PARTIAL` |  |
| Total cost of ownership analysis | Calculate TCO for assets including acquisition, operation, maintenance, and disposal | Per asset/decision | `PARTIAL` |  |

---

### Investment Officer

> Sourcing acquisition and divestment opportunities, executing transactions, and portfolio analysis.
> **KPIs**: Transaction volume, IRR, realized value growth.

The Investment Officer consumes outputs from facility condition assessments, capital planning, and financial analysis to inform acquisition/disposition decisions. No FM operational processes are directly owned.

---

### Controller

> Financial reporting accuracy, period-end close, internal controls, cost tracking, and audit compliance.
> **KPIs**: Reporting accuracy, close cycle time, audit finding count, variance explanation rate.

The Controller owns financial control, reporting, and audit-readiness processes.

**Financial Reporting & Control**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Cost tracking and variance analysis | Track actual costs against budget; analyze and explain variances | Monthly | `FULL` |  |
| CapEx/OpEx classification | Correctly classify expenditures as capital or operating per accounting standards | Per transaction | `LARGE` |  |
| Financial reporting | Generate financial reports: actuals vs. budget, variance, forecast, trend analysis | Monthly | `FULL` |  |
| FM cost benchmarking | Benchmark FM costs per sq ft against industry data (IFMA, BOMA) | Annual | `LARGE` |  |
| Accrual management | Manage monthly accruals for incurred but not-yet-invoiced FM expenses | Monthly | `LARGE` |  |

**Accounts & Audit**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Accounts payable processing | Process all FM-related vendor invoices through approval and payment | Ongoing | `FULL` |  |
| Accounts receivable processing | Track and collect tenant charges, service fees, and reimbursements | Ongoing | `FULL` |  |
| Spend categorization | Categorize all FM spend by vendor, category, building, and period for analysis | Ongoing | `FULL` |  |
| Financial audit preparation | Prepare documentation and support for internal and external financial audits | Annual | `LARGE` |  |

---

### Rent Administrator

> Rent invoicing, payment collection, arrears management, tenant charge-backs, and contract register maintenance.
> **KPIs**: Payment rate, invoicing error rate, turnaround time for rent adjustments.

The Rent Administrator owns tenant billing and charge-back processes.

**Tenant Billing**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Charge-backs to tenants | Calculate and invoice tenants for services per lease terms | Monthly | `LARGE` |  |
| Utility billing and cost allocation | Allocate utility costs to tenants based on sub-metering or agreed formulas | Monthly | `LARGE` |  |
| CAM reconciliation | Reconcile common area maintenance charges against actual expenses | Annual | `LARGE` |  |

---

## 3. Asset Management & Property Operations

Portfolio strategy, value creation, tenant-facing management, leasing, and operational service delivery.

---

### Asset Manager

> Value strategy for property clusters; maximize NOI and reduce yield through strategic investments.
> **KPIs**: Direct yield, NOI growth, portfolio market value.

The Asset Manager owns strategic capital planning and assessment processes.

**Capital Strategy**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| CapEx planning and budgeting | Develop multi-year capital expenditure plan based on asset condition and business needs | Annual | `LARGE` |  |
| Budgeting and forecasting | Develop and manage facility operating and capital budgets | Annual / Quarterly reforecast | `LARGE` |  |
| Asset lifecycle management | Track asset condition, age, maintenance cost, and plan for replacement | Ongoing | `LARGE` |  |

**Capital Assessment**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Facility condition assessment (FCA) | Comprehensive assessment of building systems and components condition | Triennial-Quinquennial | `LARGE` |  |
| Deferred maintenance prioritization | Rank and prioritize backlog of deferred maintenance items by risk and impact | Annual | `FULL` |  |

**Capital Closeout**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Post-occupancy evaluation | Evaluate project outcomes vs. design intent after occupancy | Per project | `LARGE` |  |
| Value engineering | Analyze project designs to achieve required functions at lowest lifecycle cost | Per project | `PARTIAL` |  |
| Change order management | Track, evaluate, and approve/reject project change orders | Per project | `LARGE` |  |
| Project closeout documentation | Compile as-built drawings, warranties, O&M manuals, commissioning reports | Per project | `LARGE` |  |

---

### Business Developer

> Refine the business model, develop new service offerings (coworking, service packages), and optimize internal processes.
> **KPIs**: Revenue from additional services, innovation rate (implemented projects).

**Workplace Experience**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Workplace experience platform management | Operate employee-facing workplace app for bookings, services, community, wayfinding | Continuous | `LARGE` |  |
| Real-time occupant feedback collection | Collect and respond to real-time occupant comfort and satisfaction feedback | Continuous | `FULL` |  |
| Workplace analytics | Analyze workplace utilization, satisfaction, and productivity metrics | Continuous | `FULL` |  |
| Occupant wellbeing programs | Manage workplace wellness initiatives: fitness, nutrition, mental health, ergonomics | Ongoing | `PARTIAL` |  |

---

### Property Manager

> P&L responsibility for properties, customer relationships, budgeting, and service delivery.
> **KPIs**: NOI (net operating income), economic occupancy rate, tenant satisfaction index (NKI).

The Property Manager owns tenant services, space management, vendor management, and operational billing.

**Tenant Services — Help Desk**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Help desk / service desk | Central point of contact for all occupant requests, issues, and inquiries | Continuous | `FULL` | complaint-triage-temp, service-object-enricher |
| Complaint and feedback management | Track, respond to, and resolve occupant complaints; analyze feedback trends | Ongoing | `FULL` | complaint-pattern-analyzer, complaint-triage-temp |

**Tenant Services — Communications**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Occupant communications | Proactive communications: building notices, event info, service updates, emergency alerts | Ongoing | `FULL` |  |
| Tenant onboarding | Orient new tenants: building rules, contacts, access, services, amenities | Per tenant | `LARGE` |  |
| Community engagement | Build community: events, programming, networking, wellness initiatives | Ongoing | `PARTIAL` |  |

**Tenant Services — Surveys & Moves**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Satisfaction surveys | Conduct occupant satisfaction surveys; analyze results; track improvement actions | Quarterly-Annual | `FULL` |  |
| Move-in/move-out coordination | Coordinate tenant moves: scheduling, elevator reservations, damage protection, inspections | As needed | `PARTIAL` |  |

**Tenant Services — Amenities & Front Desk**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Amenity management | Manage building amenities: fitness center, lounge, conference center, bike storage, showers | Ongoing | `LARGE` |  |
| Event space management | Manage event/meeting space bookings, setup, AV, catering coordination | As needed | `PARTIAL` |  |
| Reception/front desk services | Greet visitors, manage deliveries, provide information, coordinate with security | Business hours | `PARTIAL` |  |
| Concierge services | Premium tenant services: dry cleaning, restaurant reservations, transportation, personal requests | Business hours | `PARTIAL` |  |

**Tenant Services — Mail & Food**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Mail and package handling | Receive, log, notify, distribute, and track mail and packages for tenants | Daily | `LARGE` |  |
| Food service management | Manage cafeteria, vending, pantry, catering, and food-related services | Daily | `PARTIAL` |  |

**Space Management — Planning**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Space planning and allocation | Plan and allocate spaces to tenants, departments, and functions | Quarterly / As needed | `LARGE` |  |
| Neighborhood/zone planning | Design activity-based work neighborhoods within open-plan offices | Quarterly / As needed | `LARGE` |  |
| Capacity planning | Forecast future space needs based on headcount projections and utilization data | Quarterly-Annual | `FULL` | density-analysis |

**Space Management — Occupancy & Operations**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Occupancy tracking and analytics | Monitor real-time and historical space utilization via sensors, WiFi, badge data | Continuous | `FULL` | density-analysis, ghost-booking-killer |
| Desk/hot-desk booking | Manage flexible desk reservation systems | Continuous | `FULL` |  |
| Meeting room booking and optimization | Manage conference room reservations; optimize for utilization and no-shows | Continuous | `FULL` | ghost-booking-killer |
| Wayfinding and navigation | Provide indoor navigation for occupants to find desks, rooms, amenities, people | Continuous | `FULL` |  |
| Parking management | Manage parking allocation, reservations, access, EV charging assignments | Continuous | `LARGE` |  |
| Move management | Plan and execute office moves: furniture, IT, access changes, communications | As needed | `PARTIAL` |  |
| Floor plan management | Maintain accurate floor plans reflecting current layouts, furniture, and occupancy | Ongoing | `LARGE` |  |

**Space Management — Lease & Reporting**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Lease administration | Manage lease terms, dates, options, escalations, compliance, abstractions | Ongoing | `FULL` |  |
| Space utilization reporting | Generate utilization reports, density metrics, cost-per-seat analysis | Monthly-Quarterly | `FULL` | density-analysis |

**Vendor Management — Procurement**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Procurement (RFP/RFQ process) | Source, evaluate, and select vendors through structured procurement | As needed | `FULL` |  |
| Bid management and evaluation | Manage competitive bidding process; evaluate proposals against criteria | As needed | `FULL` |  |
| Market benchmarking | Benchmark vendor pricing and service levels against market rates | Annual | `LARGE` |  |

**Vendor Management — Contracts**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Contract negotiation and renewal | Negotiate terms, pricing, SLAs, and renewal conditions with vendors | Per contract cycle | `PARTIAL` |  |
| SLA monitoring | Continuously monitor vendor performance against contractual SLAs | Continuous | `FULL` | elevator-availability-logger |
| Insurance certificate tracking | Track and verify vendor insurance certificates for currency and compliance | Ongoing | `FULL` |  |

**Vendor Management — Onboarding & Performance**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Contractor onboarding | Onboard new vendors: safety training, credential verification, system access, orientation | Per vendor | `LARGE` |  |
| Vendor compliance monitoring | Monitor ongoing vendor compliance with safety, labor, environmental requirements | Ongoing | `FULL` |  |
| Vendor performance scorecards | Rate and track vendor performance using KPIs and balanced scorecards | Quarterly | `FULL` |  |
| Vendor risk assessment | Assess financial, operational, safety, and reputational risk of vendors | Annual / Per vendor | `LARGE` |  |

**Vendor Management — Financial**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Invoice processing | Receive, validate, match, approve, and process vendor invoices | Per invoice | `FULL` |  |
| Purchase order management | Create, approve, track, and close purchase orders | Per order | `FULL` |  |
| Spend analysis | Analyze spend by vendor, category, building, and period to identify savings | Monthly-Quarterly | `FULL` |  |

**Vendor Management — Operations**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Work order assignment to vendors | Assign and dispatch work orders to external vendor technicians | As needed | `FULL` |  |
| Service delivery verification | Verify vendor work was completed to specification before approving payment | Per WO | `PARTIAL` |  |
| Subcontractor management | Manage vendors' use of subcontractors; verify qualifications and insurance | Ongoing | `PARTIAL` |  |
| Preferred vendor list management | Maintain curated list of approved vendors by trade, region, and capability | Ongoing | `LARGE` |  |

**Cross-Cutting (shared ownership)**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| FM performance analytics and dashboards | Generate cross-functional FM performance dashboards and KPI tracking | Continuous | `FULL` | alarm-consolidator |
| SLA management (all services) | Define, monitor, report, and enforce SLAs across all FM service lines | Continuous | `FULL` |  |
| Workforce scheduling and optimization | Schedule and optimize FM workforce across shifts, buildings, and tasks | Continuous | `LARGE` |  |
| FM benchmarking (overall) | Benchmark overall FM performance against industry peers using IFMA, BOMA, RICS data | Annual | `LARGE` |  |

---

### Leasing Manager

> Active sales to minimize vacancies and secure the right tenant mix.
> **KPIs**: Net leasing (new contracts minus terminated), signed rental value, time-on-market for vacancies.

No FM operational processes from the 289 corpus are directly owned. The Leasing Manager operates in the commercial/sales domain, consuming space utilization data and tenant satisfaction metrics produced by FM processes.

---

## 4. Technology & Sustainability

The technical backbone: maintenance strategy, energy optimization, regulatory compliance, ESG, and digital transformation.

---

### Technical Manager

> Technical operations, regulatory compliance (OVK, SBA), maintenance planning, and contractor management.
> **KPIs**: Energy use (kWh/m2), fault reports per building, planned vs. reactive maintenance ratio.

The Technical Manager owns the largest share of processes: all preventive maintenance, predictive maintenance, regulatory compliance, and HSE.

**Preventive Maintenance — HVAC**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| HVAC filter replacement | Replace AHU and RTU filters per manufacturer schedule or differential pressure reading | Monthly-Quarterly | `PARTIAL` | supply-air-filter-analyzer |
| HVAC belt inspection and replacement | Inspect and replace fan belts on AHUs, RTUs, and exhaust fans | Quarterly-Semi-annual | `PARTIAL` |  |
| Coil cleaning (evaporator/condenser) | Clean HVAC coils to maintain heat transfer efficiency | Semi-annual-Annual | `PARTIAL` |  |
| Chiller maintenance | Comprehensive chiller PM: oil analysis, refrigerant levels, tube cleaning, control calibration | Quarterly-Annual | `PARTIAL` | chiller-efficiency-monitor |
| Cooling tower maintenance | Water treatment, basin cleaning, fill replacement, fan/motor service, Legionella testing | Monthly-Quarterly | `PARTIAL` |  |
| Boiler maintenance | Burner tuning, heat exchanger inspection, safety controls testing, water treatment | Annual (pre-season) | `PARTIAL` | fjarrvarme-return-guard |
| VAV box calibration | Calibrate variable air volume terminal units: flow sensors, damper actuators, reheat valves | Annual | `PARTIAL` |  |
| Ductwork inspection | Inspect ductwork for leaks, insulation damage, microbial growth, obstruction | Annual-Biennial | `PARTIAL` |  |
| Refrigerant leak detection | Check HVAC systems for refrigerant leaks per EPA requirements | Quarterly-Annual | `PARTIAL` |  |
| BMS/controls calibration | Calibrate BMS sensors, verify control sequences, update schedules and setpoints | Quarterly-Annual | `LARGE` | hvac-setpoint-deviation-checker |
| Thermostat/sensor calibration | Verify and calibrate space temperature, humidity, CO2, and pressure sensors | Annual | `PARTIAL` | iaq-sensor-drift-detector, sensor-stuck-check |
| Economizer inspection and testing | Verify economizer operation: damper stroke, controls, changeover setpoints | Semi-annual | `LARGE` | free-cooling-maximizer |

**Preventive Maintenance — Electrical**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Electrical panel inspection | Inspect electrical panels: tighten connections, check for overheating, verify breaker operation | Annual | `PARTIAL` |  |
| Emergency generator testing | Test emergency generators under load; check fuel, coolant, battery, transfer switch | Weekly (no-load) / Monthly (load) | `PARTIAL` |  |
| UPS battery testing | Test uninterruptible power supply batteries and systems | Quarterly-Semi-annual | `PARTIAL` | ups-battery-health-predictor |
| Lighting system maintenance | Replace lamps/LEDs, clean fixtures, verify emergency lighting, test controls/sensors | Quarterly-Annual | `PARTIAL` | lighting-dali-health-monitor |
| Transformer inspection | Inspect dry and oil-filled transformers: oil testing, thermal scanning, connection checks | Annual | `PARTIAL` |  |
| Switchgear maintenance | Clean, test, and maintain medium/high voltage switchgear | Annual-Triennial | `PARTIAL` |  |
| Infrared thermography scan | Thermal imaging of electrical systems to detect hot spots and potential failures | Annual | `LARGE` | electrical-thermal-monitor |

**Preventive Maintenance — Plumbing**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Plumbing fixture maintenance | Inspect and service faucets, toilets, urinals, drains, water heaters | Quarterly-Annual | `PARTIAL` |  |
| Backflow preventer testing | Annual testing by certified tester per code requirements | Annual | `PARTIAL` |  |
| Grease trap cleaning | Clean commercial kitchen grease traps per health code requirements | Monthly-Quarterly | `PARTIAL` |  |
| Sump pump testing | Test sump pumps, float switches, and alarm systems | Quarterly | `PARTIAL` |  |
| Water heater maintenance | Flush tanks, inspect anodes, test T&P valves, check thermostats | Annual | `PARTIAL` | vvc-temp-monitor |
| Domestic water system flushing | Flush low-use outlets to prevent Legionella; maintain water temperatures | Weekly-Monthly | `PARTIAL` | vvc-temp-monitor |

**Preventive Maintenance — Fire/Life Safety**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Fire alarm system testing | Test fire alarm control panel, pull stations, smoke/heat detectors, notification appliances | Quarterly-Annual per NFPA 72 | `PARTIAL` |  |
| Sprinkler system inspection | Inspect sprinkler heads, piping, valves, flow switches per NFPA 25 | Quarterly-Annual | `PARTIAL` |  |
| Fire extinguisher inspection | Monthly visual inspection and annual maintenance of portable extinguishers | Monthly/Annual | `PARTIAL` |  |
| Fire pump testing | Test fire pump performance: flow, pressure, electrical, diesel engine | Weekly (churn) / Annual (flow) | `PARTIAL` |  |
| Emergency exit/egress inspection | Verify exit signs, emergency lighting, stairwell doors, egress paths clear | Monthly-Quarterly | `PARTIAL` |  |
| Fire door inspection | Inspect fire doors: self-closing, latching, gaps, signage per NFPA 80 | Annual | `PARTIAL` |  |
| Smoke control system testing | Test stairwell pressurization, smoke evacuation, dampers | Annual | `PARTIAL` | fire-damper-auto-test |
| Kitchen hood suppression testing | Test commercial kitchen fire suppression systems | Semi-annual | `PARTIAL` |  |

**Preventive Maintenance — Elevators/Conveyance**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Elevator preventive maintenance | Routine PM per OEM schedule: lubrication, adjustment, cleaning, testing | Monthly | `PARTIAL` | elevator-availability-logger |
| Elevator annual safety test | Full load, overspeed governor, and safety device testing per ASME A17.1 | Annual | `MANUAL` |  |
| Escalator/moving walk maintenance | PM for escalators and moving walkways | Monthly | `PARTIAL` |  |

**Preventive Maintenance — Building Envelope**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Roof inspection and maintenance | Inspect roofing membrane, flashings, drains, penetrations; make repairs | Semi-annual | `PARTIAL` |  |
| Window/curtain wall inspection | Inspect glazing seals, frames, hardware, weatherstripping | Annual | `PARTIAL` |  |
| Exterior caulking/sealant inspection | Check expansion joints, perimeter sealants, waterproofing | Annual | `PARTIAL` |  |
| Parking structure inspection | Inspect structural concrete, expansion joints, drainage, lighting, striping | Annual | `PARTIAL` |  |

**Preventive Maintenance — Interior**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Ceiling tile replacement | Replace damaged or stained ceiling tiles | As needed / Quarterly sweeps | `PARTIAL` |  |
| Door hardware maintenance | Adjust closers, replace hinges/locks, verify access control integration | Semi-annual | `PARTIAL` |  |
| Flooring maintenance | Repair/replace damaged flooring; strip/refinish hard floors | Quarterly-Annual | `PARTIAL` |  |
| Painting and wall repair | Touch up paint, repair drywall damage, maintain appearance standards | Annual / As needed | `MANUAL` |  |

**Preventive Maintenance — Grounds**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Landscaping maintenance | Mowing, trimming, planting, mulching, tree care | Weekly-Monthly (seasonal) | `PARTIAL` |  |
| Irrigation system maintenance | Inspect/adjust sprinkler heads, controllers, backflow preventers; winterize | Seasonal | `LARGE` |  |
| Snow and ice removal | Plowing, salting, shoveling for building entrances, parking, walkways | As needed (winter) | `PARTIAL` |  |
| Exterior lighting maintenance | Replace lamps, clean fixtures, adjust photocells/timers, repair bollards | Quarterly | `PARTIAL` |  |

**Preventive Maintenance — Pest Control**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Pest control treatment | Scheduled pest management: inspection, treatment, monitoring stations | Monthly-Quarterly | `PARTIAL` |  |

**Predictive Maintenance — Condition Monitoring**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Vibration analysis | Continuous or periodic vibration monitoring on rotating equipment (motors, fans, pumps, compressors) | Continuous/Monthly | `FULL` | pump-cavitation-bearing-monitor |
| Oil/fluid analysis | Analyze lubricant samples for wear metals, contamination, viscosity degradation | Quarterly-Semi-annual | `LARGE` |  |
| Thermal imaging (predictive) | Scheduled IR scanning of electrical, mechanical, and building envelope systems | Quarterly-Annual | `LARGE` | electrical-thermal-monitor |
| Ultrasonic testing | Detect compressed air/steam/gas leaks, bearing defects, electrical arcing using ultrasound | Quarterly-Annual | `LARGE` |  |
| Motor current analysis | Analyze motor current signatures to detect rotor bar, stator, and mechanical faults | Quarterly-Annual | `FULL` | pump-cavitation-bearing-monitor |

**Predictive Maintenance — Analytics**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| IoT sensor data analysis | Continuous analysis of IoT sensor streams for anomaly detection and trend deviation | Continuous | `FULL` | alarm-consolidator, water-leak-detector |
| Remaining useful life (RUL) prediction | Estimate when equipment components will fail based on condition and operational data | Continuous | `FULL` | ups-battery-health-predictor, pump-cavitation-bearing-monitor |
| Anomaly detection | Identify unusual patterns in equipment performance data that precede failures | Continuous | `FULL` | alarm-consolidator, sensor-stuck-check, water-leak-detector |
| Fault detection and diagnostics (FDD) | Automated detection and diagnosis of HVAC and building system faults from BMS data | Continuous | `FULL` | hvac-setpoint-deviation-checker, alarm-consolidator |
| Energy pattern analysis | Detect energy consumption anomalies that indicate equipment degradation | Continuous | `FULL` | ashrae-level-1, ashrae-level-2 |
| Acoustic monitoring | Analyze equipment sound profiles for abnormal patterns indicating developing faults | Continuous | `FULL` |  |

**Predictive Maintenance — Planning**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Maintenance schedule optimization | AI-optimized scheduling based on condition data, risk, and resource availability | Continuous | `FULL` | pump-runtime-balancer |
| Digital twin simulation | Use digital twin models to simulate failure scenarios and optimize maintenance strategies | As needed | `LARGE` |  |

**Regulatory Compliance — Fire Safety**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Fire alarm system annual certification | Annual inspection and certification by licensed fire protection company per NFPA 72 | Annual | `PARTIAL` |  |
| Sprinkler system certification | Annual/quarterly inspection per NFPA 25 by licensed contractor | Quarterly/Annual | `PARTIAL` |  |
| Fire door annual inspection | Inspect all fire doors per NFPA 80; document condition and deficiencies | Annual | `PARTIAL` |  |
| Fire safety plan maintenance | Maintain and update fire safety/evacuation plan per local fire code | Annual / As changed | `LARGE` | fire-damper-auto-test |

**Regulatory Compliance — Elevators**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Elevator periodic inspection | State/municipal periodic inspection by certified inspector | Annual-Triennial | `MANUAL` |  |
| Elevator permit renewal | Renew operating permits per jurisdiction | Annual | `LARGE` |  |

**Regulatory Compliance — Water Quality**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Legionella risk assessment | Assess and manage Legionella risk in water systems per ASHRAE 188/HSG274 | Annual / Ongoing | `PARTIAL` | vvc-temp-monitor |
| Legionella water sampling | Collect and test water samples from cooling towers, hot water systems, decorative fountains | Monthly-Quarterly | `PARTIAL` | vvc-temp-monitor |

**Regulatory Compliance — Hazardous Materials**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Asbestos management plan | Maintain asbestos register, conduct periodic re-inspections, manage abatement | Annual / Ongoing | `PARTIAL` |  |
| Lead paint management | Manage lead-based paint in pre-1978 buildings per EPA RRP Rule | As needed | `PARTIAL` |  |
| Hazmat storage and handling | Ensure proper storage, labeling, SDS availability, and handling per OSHA/EPA | Ongoing | `PARTIAL` |  |

**Regulatory Compliance — Environmental & Accessibility**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Environmental compliance monitoring | Monitor compliance with air quality permits, wastewater discharge, stormwater, refrigerant management | Ongoing | `LARGE` |  |
| EPA refrigerant management | Track refrigerant usage, repairs, leak rates per EPA Section 608/Clean Air Act | Ongoing | `LARGE` |  |
| ADA compliance assessment | Assess and maintain compliance with ADA accessibility requirements | Annual / Ongoing | `PARTIAL` |  |

**Regulatory Compliance — Energy & Safety**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Energy performance certification | Obtain/renew energy performance certificates (EPC, ENERGY STAR, local benchmarking) | Annual | `LARGE` | taxonomy-tracker |
| Building energy benchmarking | Report building energy data per local benchmarking ordinances | Annual | `FULL` | ashrae-level-1, iso-50002-audit-data-quality, sveby-energy-verifier |
| OSHA compliance management | Maintain OSHA compliance: recordkeeping, posting, training, hazard communication | Ongoing | `LARGE` |  |
| Building code compliance tracking | Track and maintain compliance with applicable building codes as they change | Ongoing | `LARGE` |  |

**Regulatory Compliance — Insurance, Electrical, Gas, Permits**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Insurance inspection coordination | Coordinate property and liability insurance inspections; address findings | Annual | `PARTIAL` |  |
| Electrical safety testing | Periodic testing per NFPA 70B/70E: arc flash studies, protective device testing | Annual-Triennial | `PARTIAL` |  |
| Gas system safety inspection | Inspect gas piping, appliances, and safety devices per code | Annual | `PARTIAL` |  |
| Operating permit management | Track and renew all building operating permits | Annual / As needed | `FULL` | taxonomy-tracker |

**Health, Safety & Environment — Incidents**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Incident reporting and investigation | Report, investigate, and document workplace incidents and near-misses | As needed | `LARGE` |  |
| First aid management | Maintain first aid supplies, AED units; coordinate medical response | Ongoing | `PARTIAL` |  |

**Health, Safety & Environment — Risk**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Risk assessments | Identify and evaluate workplace hazards; develop controls | Annual / As needed | `PARTIAL` |  |
| Slip/trip/fall prevention | Identify and mitigate slip/trip/fall hazards: wet floors, uneven surfaces, poor lighting | Ongoing | `PARTIAL` |  |
| Chemical safety management | Manage chemical inventory, SDS, storage, handling, and disposal | Ongoing | `LARGE` |  |

**Health, Safety & Environment — Training & Emergency**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Safety training tracking | Track and manage safety training requirements, completions, and certifications for all personnel | Ongoing | `FULL` |  |
| Emergency preparedness planning | Develop and maintain emergency response plans for all building hazards | Annual / As needed | `PARTIAL` |  |
| Emergency evacuation planning | Plan, test, and maintain evacuation procedures and assembly points | Annual | `PARTIAL` |  |

**Health, Safety & Environment — Environmental & Monitoring**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Indoor air quality monitoring | Monitor CO2, VOCs, particulates, temperature, humidity for occupant health | Continuous | `FULL` | indoor-climate-reviewer, iaq-sensor-drift-detector |
| Noise monitoring | Monitor and manage workplace noise levels | As needed | `LARGE` |  |

**Health, Safety & Environment — Ergonomics, PPE & Lone Worker**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Ergonomic assessments | Evaluate and optimize workstation ergonomics | As requested | `PARTIAL` |  |
| PPE tracking and compliance | Track PPE issuance, condition, replacement schedules, and compliance via computer vision | Ongoing | `FULL` |  |
| Lone worker safety | Monitor and protect employees working alone in remote or hazardous areas | Ongoing | `LARGE` |  |

---

### Energy Strategist

> Energy guidelines, energy investigations, operational data analysis, and climate neutrality targets.
> **KPIs**: CO2 footprint, energy savings target, share of self-produced energy (solar PV).

The Energy Strategist owns all energy management and sustainability/ESG processes.

**Energy Management — Auditing & Monitoring**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Energy audit | Comprehensive building energy audit (ASHRAE Level I/II/III) | Triennial-Quinquennial | `PARTIAL` | ashrae-level-1, ashrae-level-2, ashrae-level-3, belok-totalmetodiken, en-16247-energy-balance, iso-50002-audit-data-quality |
| Utility monitoring and bill validation | Track utility consumption, validate bills, detect anomalies | Continuous/Monthly | `FULL` | en-16247-energy-balance, enterprise-energy-aggregator, iso-50001-enpi-tracker, iso-50002-audit-data-quality |
| Sub-metering and tenant billing | Monitor sub-meters for individual tenant or system-level energy use; generate bills | Continuous/Monthly | `FULL` | enterprise-energy-aggregator |

**Energy Management — Optimization**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| HVAC energy optimization | AI-driven optimization of HVAC schedules, setpoints, and sequences for energy efficiency | Continuous | `FULL` | free-cooling-maximizer, night-setback-optimizer, nighttime-ventilation-saver, fjarrvarme-return-guard |
| Lighting controls optimization | Optimize lighting schedules, daylight harvesting, occupancy-based controls | Continuous | `FULL` | lighting-dali-health-monitor |
| BAS schedule optimization | Optimize building automation system operating schedules based on occupancy and weather | Continuous | `FULL` | night-setback-optimizer, nighttime-ventilation-saver |
| Peak demand management / load shedding | Reduce peak electrical demand through load curtailment and shifting strategies | Continuous | `FULL` | peak-shaving-effektvakt |
| Demand response participation | Participate in utility demand response programs; curtail load during grid events | Event-driven | `FULL` | peak-shaving-effektvakt |
| Fault detection and diagnostics (energy) | Detect energy-wasting faults in HVAC and building systems | Continuous | `FULL` | chiller-efficiency-monitor, free-cooling-maximizer, nighttime-ventilation-saver, fjarrvarme-return-guard |
| Retro-commissioning | Systematically review building systems to restore optimal performance | Triennial-Quinquennial | `PARTIAL` | ashrae-level-2, ashrae-level-3, belok-totalmetodiken |

**Energy Management — Reporting & Procurement**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Energy benchmarking and reporting | Benchmark against ENERGY STAR, GRESB, local requirements; generate reports | Annual | `FULL` | en-16247-energy-balance, iso-50001-enpi-tracker, sveby-energy-verifier |
| Carbon emissions tracking | Calculate and track Scope 1, 2, and 3 carbon emissions from building operations | Monthly-Annual | `LARGE` | ghg-climate-auditor |
| Energy procurement | Manage electricity and gas supply contracts, rate analysis, hedging | Annual | `PARTIAL` |  |
| Utility rebate management | Identify, apply for, and track utility incentive programs and rebates | Ongoing | `LARGE` |  |

**Energy Management — Renewables & Envelope**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Renewable energy management | Manage on-site solar, battery storage, or other renewable systems | Continuous | `LARGE` | solar-pv-yield-anomaly-detector |
| EV charging management | Manage electric vehicle charging infrastructure: scheduling, load balancing, billing | Continuous | `FULL` | peak-shaving-effektvakt |
| Microgrid management | Operate building or campus microgrid systems | Continuous | `FULL` |  |
| Building envelope energy analysis | Assess and improve envelope thermal performance: insulation, glazing, air sealing | As needed | `PARTIAL` | ashrae-level-3 |
| Measurement and verification | Verify energy savings from efficiency projects per IPMVP protocols | Per project | `LARGE` | iso-50001-enpi-tracker, sveby-energy-verifier |

**Sustainability & ESG — Reporting**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| ESG reporting and data collection | Collect, validate, and report ESG data per GRESB, TCFD, CDP, GRI frameworks | Annual | `LARGE` | ghg-climate-auditor, taxonomy-tracker |
| Sustainability communications | Communicate sustainability initiatives, progress, and achievements to stakeholders | Ongoing | `PARTIAL` |  |

**Sustainability & ESG — Certifications**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Green building certifications | Obtain and maintain LEED, BREEAM, WELL, Fitwel, or other green certifications | Per certification cycle | `PARTIAL` |  |

**Sustainability & ESG — Emissions**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Scope 1 emissions accounting | Calculate direct emissions from owned/controlled sources (boilers, generators, fleet) | Monthly-Annual | `FULL` | ghg-climate-auditor |
| Scope 2 emissions accounting | Calculate indirect emissions from purchased electricity, steam, heating, cooling | Monthly-Annual | `FULL` | ghg-climate-auditor |
| Scope 3 emissions accounting | Calculate other indirect emissions (commuting, waste, supply chain, embodied carbon) | Annual | `PARTIAL` | ghg-climate-auditor |
| Embodied carbon tracking | Track embodied carbon in construction materials and building components | Per project | `PARTIAL` |  |
| Net-zero pathway planning | Develop and track progress toward net-zero carbon emissions targets | Annual | `PARTIAL` |  |

**Sustainability & ESG — Resources & Risk**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Waste reduction programs | Implement and manage waste minimization, diversion, and circular economy programs | Ongoing | `PARTIAL` |  |
| Water conservation | Implement water efficiency measures: fixture upgrades, leak detection, rainwater harvesting | Ongoing | `PARTIAL` |  |
| Sustainable procurement | Source environmentally preferable products, materials, and services | Ongoing | `PARTIAL` |  |
| Climate risk assessment | Assess physical and transition climate risks to building portfolio | Annual-Triennial | `PARTIAL` |  |

**Sustainability & ESG — Biodiversity, Supply Chain, IEQ**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Biodiversity management | Manage green roofs, pollinator gardens, bird-safe design, habitat preservation | Ongoing | `PARTIAL` |  |
| Supply chain sustainability | Assess and improve sustainability performance of FM supply chain | Ongoing | `PARTIAL` |  |
| Indoor environmental quality management | Manage IEQ: air quality, thermal comfort, lighting quality, acoustics for occupant health | Continuous | `LARGE` | indoor-climate-reviewer |

**Sustainability & ESG — Social, Leasing, Circular**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Social impact measurement | Measure and report social impacts: community engagement, DEI, living wage, local hiring | Annual | `PARTIAL` |  |
| Green lease administration | Manage green lease clauses: data sharing, efficiency targets, fit-out standards | Ongoing | `PARTIAL` |  |
| Circular economy initiatives | Implement asset reuse, material recovery, waste-to-resource programs | Ongoing | `PARTIAL` |  |

---

### Chief Digital Officer / Proptech Manager

> Digital transformation, smart building technology, IoT infrastructure, IT security, and data-driven services.
> **KPIs**: Digitalization rate of portfolio, system uptime, cost synergies through technology.

**Smart Building / IoT**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| BAS/BMS management and optimization | Operate, maintain, and optimize building automation/management systems | Continuous | `LARGE` |  |
| Digital twin management | Maintain and operate digital twin models for building operations | Continuous | `LARGE` |  |
| IoT sensor network management | Deploy, maintain, calibrate, and manage building IoT sensor infrastructure | Ongoing | `PARTIAL` |  |
| System integration management | Manage integration between building systems: BMS, CMMS, IWMS, ERP, security, lighting | Ongoing | `PARTIAL` |  |
| Building data analytics | Analyze cross-system building data for operational insights and optimization | Continuous | `FULL` | alarm-consolidator, service-object-enricher |
| OT cybersecurity management | Protect building operational technology networks and devices from cyber threats | Continuous | `LARGE` |  |

**Document Management — Digital**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| BIM management | Maintain and leverage Building Information Models for FM operations | Ongoing | `PARTIAL` |  |
| Digital asset register | Maintain comprehensive digital register of all building assets with metadata | Ongoing | `FULL` |  |
| Historical maintenance records | Maintain searchable archive of all maintenance history for every asset | Ongoing | `FULL` |  |
| Floor plan management (digital) | Maintain accurate digital floor plans reflecting current conditions | Ongoing | `LARGE` |  |

**Document Management — Building Records**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Building documentation maintenance | Maintain and organize all building documentation: drawings, manuals, certificates, plans | Ongoing | `LARGE` |  |
| As-built drawing management | Maintain current as-built architectural, structural, MEP, and fire protection drawings | Ongoing / Per project | `PARTIAL` |  |
| Equipment manuals and data sheets | Maintain organized library of O&M manuals, submittals, and technical data for all equipment | Ongoing | `FULL` |  |
| Warranty tracking | Track warranty terms, expiration dates, and claims for all building equipment and systems | Ongoing | `FULL` |  |

**Document Management — Compliance & Procedures**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Compliance certificate management | Track and maintain all compliance certificates, permits, and licenses with expiration alerting | Ongoing | `FULL` |  |
| Regulatory submission management | Prepare and track required regulatory filings and submissions | Per requirement | `LARGE` |  |
| Standard operating procedures (SOPs) | Develop, maintain, and distribute SOPs for all FM operations | Ongoing | `LARGE` |  |
| O&M manuals compilation | Compile and maintain operations and maintenance manuals for each building system | Per project / Ongoing | `LARGE` |  |

**Document Management — Handover & Knowledge**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Building handover documentation | Manage document handover between construction and FM teams at building delivery | Per project | `PARTIAL` |  |
| Knowledge base management | Maintain searchable knowledge base of troubleshooting guides, lessons learned, FAQs | Ongoing | `LARGE` |  |

---

## 5. Project Development

New construction, tenant improvements, major renovations, and urban development.

---

### Project Manager

> Drive construction projects within time, quality, and budget constraints.
> **KPIs**: Budget adherence, project margin, environmental certification level (BREEAM).

**Capital Projects**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Renovation/construction project management | Manage capital improvement projects from design through construction | Per project | `PARTIAL` |  |
| Project scoping and estimating | Define project scope, develop cost estimates, evaluate alternatives | Per project | `LARGE` |  |
| Contractor selection for capital work | Select contractors for capital projects through competitive process | Per project | `LARGE` |  |
| Commissioning / retro-commissioning | Verify new or existing systems perform per design intent | Per project / Triennial | `PARTIAL` |  |

---

### Urban Developer / Planning Strategist

> Drive zoning processes, municipal collaboration, and long-term site development strategy.
> **KPIs**: Increase in building rights portfolio (sqm), number of legally binding detailed plans.

No FM operational processes from the 289 corpus are directly owned. This role operates in the pre-construction planning domain.

---

## 6. Field Operations

On-site execution: daily building operations, reactive maintenance, cleaning, and security.

---

### Building Technician

> Operate and optimize HVAC, electrical, and plumbing systems; respond to faults and emergencies.
> **KPIs**: Response time on fault reports, energy performance at building level.

The Building Technician executes reactive maintenance and daily operational tasks.

**Reactive Maintenance — HVAC**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| HVAC system failure response | Respond to complete HVAC system failures (chiller, boiler, AHU, RTU down) | As needed | `PARTIAL` | alarm-consolidator |
| Comfort complaint response | Address occupant hot/cold/humid/stuffy complaints | As needed | `PARTIAL` | complaint-triage-temp, heating-comfort-analyzer |

**Reactive Maintenance — Electrical**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Power outage response | Respond to partial or complete power failures; coordinate with utility | As needed | `PARTIAL` |  |
| Electrical fault repair | Repair tripped breakers, failed fixtures, damaged wiring, outlet issues | As needed | `PARTIAL` |  |

**Reactive Maintenance — Plumbing**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Water leak response | Emergency response to pipe bursts, valve failures, fixture leaks, roof leaks | As needed | `PARTIAL` | water-leak-detector |
| Clogged drain/sewer response | Clear clogged drains, toilets, sewer lines | As needed | `PARTIAL` |  |
| Domestic water system failure | Respond to water heater failures, booster pump issues, water quality problems | As needed | `PARTIAL` |  |

**Reactive Maintenance — Fire/Life Safety**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Fire alarm trouble signal response | Investigate and resolve fire alarm system trouble signals | As needed | `PARTIAL` | alarm-consolidator |
| Sprinkler system leak/activation | Respond to accidental sprinkler activation or system leak | As needed | `PARTIAL` |  |

**Reactive Maintenance — Elevators**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Elevator entrapment rescue | Respond to passenger entrapment; coordinate rescue per ASME code | As needed | `PARTIAL` |  |
| Elevator malfunction response | Address door issues, leveling problems, ride quality complaints | As needed | `PARTIAL` | elevator-availability-logger |

**Reactive Maintenance — Building Envelope & Interior**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Roof leak response | Emergency response to active roof leaks | As needed | `PARTIAL` |  |
| Broken window/glass response | Secure and replace broken glazing | As needed | `PARTIAL` |  |
| Lock/access issue response | Respond to lockouts, broken locks, access control failures | As needed | `PARTIAL` |  |
| General repair requests | Handle miscellaneous tenant repair requests: furniture, fixtures, signage, etc. | As needed | `PARTIAL` |  |

---

### Facilities Custodian

> Property upkeep, grounds care, cleaning oversight, and daily tenant contact.
> **KPIs**: Tenant satisfaction with premises maintenance, "clean & safe" index.

The Facilities Custodian owns cleaning/janitorial and security/access operations.

**Cleaning & Janitorial — Routine**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Routine daily cleaning | Standard office cleaning: vacuuming, trash, dusting, restroom cleaning, kitchen/breakroom | Daily | `LARGE` |  |
| Occupancy-based smart cleaning | IoT sensor-driven cleaning triggered by actual usage rather than fixed schedule | Continuous | `FULL` | usage-based-cleaning |
| Restroom cleaning and supply monitoring | Clean restrooms, restock supplies; IoT sensors monitor supply levels and traffic | Multiple daily | `LARGE` |  |

**Cleaning & Janitorial — Deep Cleaning**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Deep cleaning | Comprehensive cleaning: furniture, fixtures, high surfaces, vents, behind equipment | Monthly-Quarterly | `PARTIAL` |  |
| Carpet care (extraction/shampooing) | Deep clean carpets using hot water extraction or encapsulation | Quarterly-Annual | `PARTIAL` |  |
| Hard floor maintenance | Strip, seal, wax, buff hard flooring. Autonomous floor scrubbers handle routine maintenance | Monthly-Quarterly | `LARGE` |  |
| Window cleaning | Interior and exterior window cleaning | Quarterly-Annual | `PARTIAL` |  |

**Cleaning & Janitorial — Specialized**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Sanitization/disinfection | Enhanced sanitization of high-touch surfaces, common areas | Daily / As needed | `PARTIAL` |  |
| Kitchen/food service area cleaning | Specialized cleaning of commercial kitchens, cafeterias, vending areas | Daily | `PARTIAL` |  |
| Exterior cleaning (pressure washing) | Pressure wash building facades, sidewalks, parking structures, loading docks | Quarterly-Annual | `PARTIAL` |  |

**Cleaning & Janitorial — Waste Management**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Waste collection and disposal | Collect, transport, and dispose of general waste from all areas | Daily | `LARGE` |  |
| Recycling program management | Manage recycling streams: paper, plastic, glass, e-waste, organic; track diversion rates | Ongoing | `LARGE` |  |
| Trash compactor management | Monitor fill levels, schedule pickups, maintain compactor equipment | Ongoing | `FULL` |  |

**Cleaning & Janitorial — Quality & Supply**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Cleaning quality inspections | Inspect cleaning quality; score against standards; provide feedback | Weekly-Monthly | `LARGE` | usage-based-cleaning |
| Cleaning supply inventory management | Track and replenish cleaning chemicals, paper products, bags, equipment | Ongoing | `FULL` |  |
| Green cleaning program | Manage environmentally preferable cleaning products and practices | Ongoing | `LARGE` |  |

**Cleaning & Janitorial — Robotics**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Autonomous cleaning robot deployment | Deploy and manage robotic vacuums, floor scrubbers, window cleaners | Daily | `FULL` |  |

**Security & Access — Physical**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Physical security management | Manage guards, patrols, access policies, perimeter security | Continuous | `PARTIAL` |  |
| Security patrol scheduling | Schedule and optimize guard patrol routes and coverage | Continuous | `FULL` |  |
| Loading dock management | Manage deliveries, vehicle access, scheduling, security screening at loading docks | Daily | `PARTIAL` |  |

**Security & Access — Electronic**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| CCTV/video surveillance | Operate and monitor video surveillance system; AI-powered analytics for detection | Continuous | `FULL` |  |
| Access badge/credential management | Issue, manage, deactivate access credentials; manage access levels | Ongoing | `LARGE` |  |
| Visitor management | Register, badge, and track visitors; integrate with access control | Ongoing | `FULL` |  |
| Alarm monitoring | Monitor intrusion, duress, and panic alarms; coordinate response | Continuous | `FULL` |  |
| License plate recognition | Automated vehicle identification for parking and security | Continuous | `FULL` |  |

**Security & Access — Cyber & Incidents**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| OT/BAS cybersecurity | Protect building operational technology from cyber threats | Continuous | `LARGE` |  |
| Security incident investigation | Investigate security incidents using CCTV, access logs, and other evidence | As needed | `LARGE` |  |
| Emergency lockdown procedures | Execute building lockdown in response to security threats | As needed | `PARTIAL` |  |

**Security & Access — Keys, Mail & After-Hours**

| Process | Description | Frequency | Automation | Agent |
|---------|-------------|-----------|------------|-------|
| Key management | Manage physical key inventory, issuance, and tracking | Ongoing | `PARTIAL` |  |
| Mailroom/package handling | Receive, log, notify, and distribute mail and packages | Daily | `LARGE` |  |
| After-hours access management | Manage and log after-hours building access requests | Ongoing | `FULL` |  |

---

## Summary Statistics

### Processes by Department

| Department | Roles | Processes | Share |
|------------|-------|-----------|-------|
| Corporate Leadership | 3 | 5 | 2% |
| Finance | 4 | 21 | 7% |
| Asset Management & Property Operations | 4 | 59 | 20% |
| Technology & Sustainability | 3 | 154 | 53% |
| Project Development | 2 | 4 | 1% |
| Field Operations | 2 | 46 | 16% |
| **Total** | **18** | **289** | **100%** |

### Automation Potential Breakdown

| Automation Level | Count | Share | Examples |
|------------------|-------|-------|----------|
| `FULL` — Fully automatable | 74 | 26% | FDD, utility monitoring, IoT analytics, occupancy tracking, invoice processing |
| `LARGE` — Largely automatable | 80 | 28% | BMS calibration, budgeting, vendor onboarding, ESG reporting, document management |
| `PARTIAL` — Partially automatable | 129 | 44% | Physical maintenance, inspections, emergency response, negotiations, audits |
| `MANUAL` — Minimally automatable | 6 | 2% | Strategy, change management, elevator safety tests, stakeholder management |
| **Total** | **289** | **100%** | |

### Automation by Department

| Department | FULL | LARGE | PARTIAL | MANUAL | Most Automatable Area |
|------------|------|-------|---------|--------|----------------------|
| Corporate Leadership (5) | 0 | 0 | 2 | 3 | Business continuity planning |
| Finance (21) | 5 | 12 | 4 | 0 | AP/AR, cost tracking, financial reporting |
| Asset Mgmt & Property Ops (59) | 26 | 21 | 12 | 0 | Help desk, space booking, vendor monitoring, deferred maint. |
| Technology & Sustainability (154) | 33 | 34 | 84 | 3 | Predictive analytics, energy optimization |
| Project Development (4) | 0 | 2 | 2 | 0 | Project scoping & contractor selection |
| Field Operations (46) | 10 | 11 | 25 | 0 | Video surveillance, smart cleaning, alarm monitoring |

### Agent Coverage by Department

| Department | Processes | With Agent | Coverage |
|------------|-----------|------------|----------|
| Corporate Leadership | 5 | 0 | 0% |
| Finance | 21 | 0 | 0% |
| Asset Mgmt & Property Ops | 59 | 8 | 14% |
| Technology & Sustainability | 154 | 51 | 33% |
| Project Development | 4 | 0 | 0% |
| Field Operations | 46 | 7 | 15% |
| **Total** | **289** | **66** | **23%** |

### Key Insight

**54% of all processes (FULL + LARGE) are substantially automatable with current AI/IoT technology.** The highest automation potential lies in:
1. **Predictive maintenance analytics** (100% FULL automatable)
2. **Energy optimization** (85% FULL automatable)
3. **Tenant self-service** (help desk, booking, wayfinding — all FULL)
4. **Financial transaction processing** (AP/AR, invoicing — all FULL)

The remaining 46% (PARTIAL + MANUAL) requires human presence for physical tasks, complex negotiations, regulatory inspections, or strategic judgment.

---

## Agent Roster

42 autonomous expert agents are currently defined. Each agent continuously monitors specific building systems and triggers actions when anomalies are detected. Agents are referenced in the process tables above by their short name.

### Energy Auditing & Compliance (11 agents)

| Agent | Full Name | What It Does | Processes Covered |
|-------|-----------|-------------|-------------------|
| ashrae-level-1 | ASHRAE Energy Audit Level I | Performs data-driven walk-through audits identifying no-cost/low-cost energy savings | Energy audit, Energy pattern analysis, Building energy benchmarking |
| ashrae-level-2 | ASHRAE Energy Audit Level II | Detailed energy surveys breaking consumption into end-uses with ECM financial analysis | Energy audit, Retro-commissioning, Energy pattern analysis |
| ashrae-level-3 | ASHRAE Energy Audit Level III | Investment-grade analysis of capital-intensive ECMs with engineering rigor | Energy audit, Retro-commissioning, Building envelope energy analysis |
| belok-totalmetodiken | BeLok Totalmetodiken ECM Packager | Bundles energy conservation measures into investment packages per Swedish BeLok methodology | Energy audit, Retro-commissioning |
| en-16247-energy-balance | EN 16247 Energy Balance Compiler | Maintains continuously updated, audit-ready energy balance across all energy carriers | Energy audit, Utility monitoring, Energy benchmarking and reporting |
| enterprise-energy-aggregator | Enterprise Energy Aggregator (EKL/Energisyn) | Compiles enterprise-wide energy reporting for mandatory audit compliance (Swedish EKL) | Utility monitoring, Sub-metering and tenant billing |
| iso-50001-enpi-tracker | ISO 50001 EnPI Tracker | Tracks Energy Performance Indicators and maintains baselines for ISO 50001 cycles | Energy benchmarking, Utility monitoring, Measurement and verification |
| iso-50002-audit-data-quality | ISO 50002 Audit Data Quality Monitor | Verifies metering coverage and data quality sufficient for energy audits per ISO 50002 | Energy audit, Utility monitoring, Building energy benchmarking |
| sveby-energy-verifier | SVEBY Energy Performance Verifier | Verifies actual energy performance against design predictions using SVEBY methodology | Energy benchmarking, Building energy benchmarking, Measurement and verification |
| ghg-climate-auditor | GHG Climate Auditor | Compiles greenhouse gas inventories and supports climate audit requirements | Carbon emissions tracking, Scope 1/2/3 emissions, ESG reporting |
| taxonomy-tracker | EU Taxonomy Tracker | Continuously assesses whether buildings meet EU Taxonomy energy thresholds | ESG reporting, Energy performance certification |

### HVAC & Thermal Systems (8 agents)

| Agent | Full Name | What It Does | Processes Covered |
|-------|-----------|-------------|-------------------|
| chiller-efficiency-monitor | Chiller Plant Efficiency Monitor | Detects COP degradation indicating fouling, refrigerant loss, or mechanical wear | Fault detection (energy), Chiller maintenance |
| free-cooling-maximizer | Free Cooling Maximizer | Detects wasted mechanical cooling; maximizes free cooling when outdoor temps permit | HVAC energy optimization, Economizer testing, Fault detection (energy) |
| heating-comfort-analyzer | Heating Comfort Analyzer | Assesses thermal comfort and detects misalignment between heating and occupant needs | Comfort complaint response, HVAC energy optimization |
| hvac-setpoint-deviation-checker | HVAC Setpoint Deviation Checker | Detects rooms where actual temperature consistently deviates from setpoint | Fault detection (FDD), BMS/controls calibration |
| night-setback-optimizer | Night Setback Optimizer | Calculates optimal heating start times using weather forecasts and thermal inertia | HVAC energy optimization, BAS schedule optimization |
| nighttime-ventilation-saver | Nighttime Ventilation Saver | Identifies energy waste from unnecessary ventilation during unoccupied periods | HVAC energy optimization, BAS schedule optimization, Fault detection (energy) |
| fjarrvarme-return-guard | District Heating Return Guard | Detects high return temperatures causing utility penalty charges in substations | HVAC energy optimization, Fault detection (energy), Boiler maintenance |
| indoor-climate-reviewer | Indoor Climate Reviewer | Monitors real-time temperature, CO2, humidity for climate threshold breaches | Indoor air quality monitoring, Indoor environmental quality management |

### Ventilation & Air Quality (3 agents)

| Agent | Full Name | What It Does | Processes Covered |
|-------|-----------|-------------|-------------------|
| ovk-pre-check | OVK Pre-Check (Airflow) | Continuously verifies ventilation airflows meet Swedish mandatory OVK requirements | (Regulatory compliance — ventilation) |
| iaq-sensor-drift-detector | IAQ Sensor Drift Detector | Detects calibration drift in CO2, humidity, and VOC sensors | Thermostat/sensor calibration, Indoor air quality monitoring |
| supply-air-filter-analyzer | Supply Air Filter Analyzer | Assesses AHU filter condition using airflow and pressure differential sensors | HVAC filter replacement |

### Power & Electrical (3 agents)

| Agent | Full Name | What It Does | Processes Covered |
|-------|-----------|-------------|-------------------|
| electrical-thermal-monitor | Electrical Distribution Thermal Monitor | Detects overheating connections, phase imbalance, and load anomalies in switchgear | Infrared thermography scan, Thermal imaging (predictive) |
| peak-shaving-effektvakt | Peak Shaving Agent (Effektvakt) | Prevents monthly power demand peaks from exceeding target thresholds | Peak demand management, Demand response, EV charging management |
| ups-battery-health-predictor | UPS Battery Health Predictor | Predicts remaining UPS battery life and flags units approaching failure | UPS battery testing, RUL prediction |

### Mechanical Systems (4 agents)

| Agent | Full Name | What It Does | Processes Covered |
|-------|-----------|-------------|-------------------|
| pump-cavitation-bearing-monitor | Pump Cavitation & Bearing Monitor | Detects cavitation, bearing wear, and mechanical degradation in circulation pumps | Vibration analysis, Motor current analysis, RUL prediction |
| pump-runtime-balancer | Pump Runtime Balancer | Equalizes wear across redundant pump pairs to extend equipment lifespan | Maintenance schedule optimization |
| valve-exerciser | Valve Exerciser (Motionering) | Prevents valves from seizing by periodically cycling them through full range | (Preventive maintenance — HVAC valves) |
| water-leak-detector | Water Leak Detector | Detects leaks and high-usage anomalies through statistical water meter analysis | Water leak response, Anomaly detection, IoT sensor data analysis |

### Lighting & Renewables (2 agents)

| Agent | Full Name | What It Does | Processes Covered |
|-------|-----------|-------------|-------------------|
| lighting-dali-health-monitor | Lighting/DALI Health Monitor | Detects driver failures, communication faults, and battery degradation in DALI lighting | Lighting system maintenance, Lighting controls optimization |
| solar-pv-yield-anomaly-detector | Solar PV Yield Anomaly Detector | Detects underperforming strings, inverter faults, soiling in rooftop/facade PV systems | Renewable energy management |

### Safety & Compliance (3 agents)

| Agent | Full Name | What It Does | Processes Covered |
|-------|-----------|-------------|-------------------|
| fire-damper-auto-test | Fire Damper Auto-Test (SBA) | Automates periodic functional testing of fire dampers per Swedish fire protection regs | Fire safety plan maintenance, Smoke control system testing |
| vvc-temp-monitor | VVC Temperature Monitor | Monitors hot water circulation return temps to detect Legionella risk conditions | Legionella risk assessment/sampling, Domestic water system flushing |
| sensor-stuck-check | Sensor Stuck Check | Detects temperature and analog sensors frozen at fixed values | Thermostat/sensor calibration, Anomaly detection |

### Operations & Tenant Experience (8 agents)

| Agent | Full Name | What It Does | Processes Covered |
|-------|-----------|-------------|-------------------|
| alarm-consolidator | Alarm & Service Object Consolidator | Consolidates and deduplicates alarms to prevent downstream noise | IoT sensor data, Anomaly detection, Fault detection (FDD), FM analytics |
| service-object-enricher | Service Object Enricher | Enriches fault reports and work orders with telemetry and historical context | Help desk, Building data analytics |
| complaint-triage-temp | Complaint Triage (Temperature) | Instantly validates temperature complaints; auto-resolves phantom issues | Comfort complaint response, Help desk, Complaint management |
| complaint-pattern-analyzer | Complaint Pattern Analyzer | Uncovers systemic causes behind recurring complaints using correlation analysis | Complaint and feedback management |
| elevator-availability-logger | Elevator Availability Logger | Tracks elevator uptime and verifies service contract SLAs | Elevator preventive maintenance, SLA monitoring |
| ghost-booking-killer | Ghost Booking Killer | Detects and releases no-show meeting room bookings in real time | Meeting room booking, Occupancy tracking |
| usage-based-cleaning | Usage-Based Cleaning Scheduler | Replaces static cleaning schedules with demand-driven task assignment | Occupancy-based smart cleaning, Cleaning quality inspections |
| density-analysis | Density Analysis Agent | Identifies underutilized zones for subletting or consolidation | Occupancy tracking, Space utilization, Capacity planning |

### Agent Coverage Summary

| Metric | Value |
|--------|-------|
| Total agents deployed | 42 |
| Processes with agent coverage | 66 of 289 (23%) |
| Processes without agent coverage | 223 of 289 (77%) |
| Department with most agent coverage | Technology & Sustainability |
| Highest agent density | Energy Management (18 processes × 11 agents) |
