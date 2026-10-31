# Digital Fraud Investigation System (SentinelTrust Enterprise)

SentinelTrust is an enterprise-grade digital fraud detection, intelligence, and case management platform built for digital banking, lending, and insurance institutions. It executes real-time multi-signal analysis—linking customer identities, device telemetry, transaction patterns, and cross-system applications—to detect synthetic identity rings, account takeovers, and organized fraud while eliminating false positives through contextual lookalike filtering.

---

### User Review & Critical Decisions

> [!IMPORTANT]
> The following architectural and workflow decisions were confirmed in Phase 1 clarification:
> - **Primary Highlight Scenario**: Lending & onboarding synthetic identity fraud (detecting fabricated personas, credit-washing patterns, shared identifiers across disparate loan applicants).
> - **Onboarding & Streaming Experience**: Dual-mode interactive customer onboarding flow (real-time KYC & device risk evaluation) alongside a streaming pipeline sandbox demonstrating horizontal ingestion with backpressure management.
> - **Compliance & Audit Architecture**: Automated Suspicious Activity Report (SAR / FinCEN-compliant draft generator), immutable cryptographically-hashed audit ledger, and one-click regulatory PDF/CSV evidence dossier exports.

---

### 1. Overview & Core Concept

- **What It Does**: SentinelTrust ingests heterogeneous data feeds (customer profiles, transaction streams, login/device logs, and loan/insurance applications) via batch upload (CSV, JSON, Excel) or real-time streaming. It normalizes inputs into a canonical identity graph, validates payloads via a dedicated Reject Queue, and runs 4 parallel detection engines (Configurable Rules, Historical Baselines, Graph Link Analysis, and Multi-Dimensional Anomaly Scoring). Detected threats are scored (0–100), filtered for legitimate lookalikes (e.g. verified family shared devices), and dispatched to an Alert Dashboard, an investigative Case Queue, and an automated Compliance SAR Reporting module.
- **Target Audience / Persona**: Financial Crime Investigators, AML/Fraud Analysts, Chief Risk Officers (CRO), and Compliance Operations teams in retail banks, digital lenders, and insurance underwriters.
- **Key Value**: Replaces siloed transaction monitoring with identity-centric cross-product risk intelligence, shrinking investigation cycle time from hours to seconds and surfacing coordinated fraud rings that evade single-point threshold rules.

---

### 2. User Experience & Visual Design

#### Key User Flows & Modules
1. **Command Center Overview (Alert Dashboard)**: High-level KPI strip (Records Ingested, Flagged Alerts, Average Risk Score, False Positive Ratio, Active Cases), real-time risk severity distribution, interactive fraud scenario breakdown, and a multi-dimensional alert grid with granular filters (product, risk tier, scenario, date range, customer).
2. **Interactive Customer Onboarding Simulator**: Live interactive onboarding journey where users can register new applicant profiles, choose biometric/device parameters, and test synthetic identity, device spoofing, or genuine applicant scenarios in real-time with instant risk scoring before account issuance.
3. **Investigation Case Queue & Detail Drawer**: Interactive case management workflow featuring status transitions (`Under Review`, `Escalate to AML`, `False Positive`, `Confirmed Fraud - Restrict Account`), immutable original alert preservation, investigator notes, and case evidence binding.
4. **Entity Link Graph Explorer**: Visual interactive node-and-link network mapping connections between shared devices, IP subnets, phone numbers, tax IDs, and beneficiary accounts to reveal organized syndicates.
5. **Data Ingestion & Reject Queue Hub**: Multi-file batch uploader (CSV, JSON, sample scenario packages) paired with an explicit Schema Validation & Reject Queue displaying rejected malformed records with exact error reasons.
6. **Streaming Pipeline Sandbox**: Real-time high-volume ingestion simulator modeling horizontal worker streams, throughput rates, sliding time windows, and backpressure buffers.
7. **Compliance SAR & Audit Ledger**: Automated regulatory filing generator creating structured Suspicious Activity Reports (FinCEN / FIU template), an append-only immutable audit trail with SHA-256 hash chaining, and one-click PDF/CSV export.

#### Visual Identity & Theme
- **Aesthetic Direction**: High-density institutional fintech / financial intelligence console. Crisp, distraction-free surfaces with purposeful typographic hierarchy and zero decorative clutter.
- **Palette Tokens**: 
  - Canvas: Deep charcoal neutral `#090D16` (Dark) / Crisp slate `#F8FAFC` (Light)
  - Surface: Layered dark slate `#0F172A` / Clean card `#FFFFFF`
  - Structural Lines: Hairline borders `rgba(255,255,255,0.08)` / `rgba(0,0,0,0.08)`
  - Primary Accent: Precision Cobalt Blue `#2563EB`
  - Semantic Risk Accents: Low Risk `#10B981` (Emerald), Medium Risk `#F59E0B` (Amber), High/Critical Risk `#EF4444` (Crimson)
- **Typography**: `Plus Jakarta Sans` for clean, modern interface headings and labels; `IBM Plex Mono` / `tabular-nums` for timestamps, transaction amounts, hash digests, and risk scores.
- **Top Bar Contract**: Single brand wordmark (`SentinelTrust`), 5 single-line navigation tabs (`Dashboard`, `Cases`, `Onboarding`, `Ingestion & Sandbox`, `Compliance & Audit`), and a primary quick-action control (`Upload Batch`).

---

### 3. Key Product Decisions & Trade-Offs

- **Decision 1: Client-Side Parallel Detection Engine vs. Remote Microservices**
  - *Chosen Approach*: Implement a fully operational, zero-lag in-browser multi-signal detection engine running pure TypeScript rule processors, z-score customer baselines, graph adjacency algorithms, and multi-factor anomaly scoring.
  - *Why*: Delivers instant interactive feedback, eliminates backend setup friction, allows immediate evaluation in AI Studio preview, and processes thousands of synthetic records with zero network latency.
- **Decision 2: Explicit Reject Queue Architecture**
  - *Chosen Approach*: Strictly enforce validation rules on ingested records; malformed records (missing customer IDs, invalid timestamps, corrupt monetary formats) are routed into an inspectable Reject Queue rather than dropped silently.
  - *Why*: Directly aligns with regulatory data governance requirements and the user's provided architecture diagram.
- **Decision 3: Immutable Original Alert Storage**
  - *Chosen Approach*: When an investigator marks an alert as "False Positive" or "Dismissed", the original alert snapshot, raw payload, and initial detection score are permanently locked in an append-only ledger; only case metadata and disposition state mutate.
  - *Why*: Ensures tamper-proof chain of custody required for bank audits and legal regulatory filings.

---

### 4. Technical Architecture & Data Strategy

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                            DATA INGESTION LAYER                              │
│  ┌───────────────────────┐  ┌───────────────────────┐  ┌──────────────────┐  │
│  │ CSV / JSON / Excel    │  │ Streaming Ingestion   │  │ Customer App     │  │
│  │ Batch File Uploader   │  │ Simulated Stream Feed │  │ Onboarding Flow  │  │
│  └───────────┬───────────┘  └───────────┬───────────┘  └────────┬─────────┘  │
│              └──────────────────────────┼───────────────────────┘            │
│                                         ▼                                    │
│                    ┌──────────────────────────────────────┐                  │
│                    │     Schema Parser & Validator        │                  │
│                    └───────┬──────────────────────┬───────┘                  │
│           (Validation Fail)│                      │(Valid Canonical Model)   │
│                            ▼                      ▼                          │
│               ┌──────────────────────┐  ┌──────────────────────┐             │
│               │  Reject Queue Hub    │  │ Linked Canonical DB  │             │
│               │ (Inspect & Download) │  │ Entities & Events    │             │
│               └──────────────────────┘  └──────────┬───────────┘             │
└────────────────────────────────────────────────────┼─────────────────────────┘
                                                     ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                    PARALLEL MULTI-SIGNAL DETECTION ENGINE                    │
│  ┌─────────────────┐ ┌──────────────────┐ ┌──────────────┐ ┌──────────────┐  │
│  │ 1. Rules Engine │ │ 2. Customer Base │ │ 3. Entity    │ │ 4. Anomaly   │  │
│  │ (Velocity/Rapid/│ │    Lines (Z-Score│ │    Graph     │ │    ML Score  │  │
│  │  High Amounts)  │ │    & Deviation)  │ │ (Device/Net) │ │  (Multi-Dim) │  │
│  └────────┬────────┘ └────────┬─────────┘ └──────┬───────┘ └──────┬───────┘  │
│           └───────────────────┼──────────────────┼────────────────┘          │
│                               ▼                                              │
│               ┌───────────────────────────────────────┐                      │
│               │  Multi-Signal Risk Scorer (0–100)     │                      │
│               │  + Legitimate Lookalike Context Filter│                      │
│               │  + Explainable Reason Codes Generator │                      │
│               └───────────────────┬───────────────────┘                      │
└───────────────────────────────────┼──────────────────────────────────────────┘
                                    ▼
┌──────────────────────────────────────────────────────────────────────────────┐
│                         PRESENTATION & CASE WORKFLOW                         │
│  ┌─────────────────────────┐  ┌────────────────────────┐  ┌────────────────┐ │
│  │ Alert Dashboard         │  │ Investigation Case     │  │ Compliance &   │ │
│  │ (Drill-down & Filters)  │  │ Management Queue       │  │ Audit Store    │ │
│  │ - Scenario Breakdown    │  │ - Assignee & Status    │  │ - FinCEN SAR   │ │
│  │ - Event Timeline        │  │ - Evidence Binder      │  │ - SHA256 Ledger│ │
│  │ - Entity Graph View     │  │ - Audit Lock Snapshot  │  │ - CSV/PDF Export││
│  └─────────────────────────┘  └────────────────────────┘  └────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

#### Core Data Entities
- **CustomerProfile**: `id`, `name`, `email`, `phone`, `ssn_tax_id`, `address`, `dob`, `employmentStatus`, `riskRating`, `createdAt`.
- **Transaction**: `id`, `customerId`, `accountId`, `amount`, `currency`, `timestamp`, `beneficiaryId`, `beneficiaryName`, `channel` (Mobile, Web, ATM, Wire), `status`.
- **DeviceLog**: `id`, `customerId`, `deviceId`, `deviceModel`, `os`, `ipAddress`, `geoCity`, `timestamp`, `authOutcome` (SUCCESS, FAILED, MFA_CHALLENGE), `isVpn`.
- **ApplicationRecord**: `id`, `customerId`, `productType` (Personal Loan, SME Credit, Auto Insurance, Core Account), `amountRequested`, `statedIncome`, `timestamp`, `status`.
- **FraudAlert**: `id`, `timestamp`, `scenarioId` (`SUSPICIOUS_TRANSFERS`, `SHARED_DEVICES`, `REPEATED_LOGIN_FAILURES`, `SYNTHETIC_IDENTITY_LENDING`, `LEGITIMATE_LOOKALIKE`), `severity` (`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`), `score` (0-100), `customerId`, `entityRefs`, `reasonCodes`, `evidenceRecords`, `lookalikeAdjusted`.
- **FraudCase**: `id`, `alertId`, `title`, `category`, `status` (`NEW`, `IN_REVIEW`, `ESCALATED`, `FALSE_POSITIVE`, `CONFIRMED_FRAUD`), `assignedTo`, `priority`, `createdAt`, `notes`, `auditHistory`.
- **AuditRecord**: `id`, `caseId`, `action`, `actor`, `timestamp`, `previousState`, `newState`, `hashDigest`.

#### High-Fidelity Pre-Configured Test Suites
To allow immediate end-to-end evaluation out of the box, SentinelTrust will include 5 pre-packaged institutional datasets:
1. **Device Farm Syndicate**: 6 loan applications with synthetic identities originating from the same device fingerprint and IP range.
2. **Account Takeover Burst**: 7 failed login attempts across multiple cities, immediate password reset, followed by a $18,500 wire transfer to a newly added offshore beneficiary.
3. **Structuring & Velocity Transfers**: Smurfing transaction sequence ($9,950 transfers in rapid 3-minute intervals).
4. **Legitimate Family Lookalike**: Parent and student sharing an iPad to pay university tuition (flagged by simple rules, but accurately discounted by SentinelTrust's lookalike filter via matching home address and historical payer patterns).
5. **Clean Baseline Batch**: 50 ordinary banking transactions demonstrating low false-positive rates.
