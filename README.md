# Digital Fraud Investigation System

AI-assisted fraud detection, investigation and case management across digital lending, insurance and core banking. It ingests CSV, Excel and JSON data, flags suspicious activity with explainable risk scores, and routes alerts into an investigation queue.

## Features

- **Ingestion**: upload customers/accounts, transactions, device and login logs, and loan applications (CSV, XLSX, JSON). Column alias mapping, row validation, and rejected rows kept with reason codes. Nothing is silently dropped.
- **Detection**: suspicious transfers, shared devices, repeated login failures, legitimate-lookalike suppression, and loan application stacking. Cross-system link graph for organised fraud.
- **Risk scoring**: 0-100 score (Low 0-39, Medium 40-69, High 70-100) from weighted indicators, with mitigating factors and a combination bonus. Every score is explained.
- **Dashboard**: processed records, flagged events, risk distribution, fraud categories. Filter by customer, transaction, product, risk level, date and detection type.
- **Case queue**: unique case IDs, evidence, status, decisions (Requires Investigation, False Positive, Escalate, Dismiss). Original alerts are immutable; changes are append-only audit events.

## Tech stack

| Layer | Choice |
| --- | --- |
| API | Python 3.12, FastAPI, Pydantic v2 |
| Ingestion | pandas, openpyxl |
| Storage | SQLite (demo), PostgreSQL 16 (production), SQLAlchemy 2, Alembic |
| Detection | Python detector classes, YAML config, numpy, scikit-learn, NetworkX, rapidfuzz |
| Front end | React 18, TypeScript, Vite, TanStack Query/Table, Tailwind, Recharts, Cytoscape.js |
| Packaging | Docker Compose |
| Testing | pytest, Ruff, Playwright |

## Project layout

```text
fraud-investigation/
  docker-compose.yml
  backend/
    app/
      api/          routers: ingest, detect, alerts, cases, config
      ingest/       loaders, alias maps, validators
      models/       SQLAlchemy tables
      detectors/    transfers, devices, logins, loans, lookalikes, graph
      scoring/      indicators, scorer, explain
      config/       rules.yaml
    tests/
    seed/           generate_sample_data.py
  frontend/
    src/pages/      Overview, Alerts, AlertDetail, Cases, CaseDetail, Rules, Upload
    src/components/ RiskBadge, EvidenceList, LinkGraph, Filters
```

## Getting started

### With Docker

```bash
docker compose up --build
```

- Web UI: http://localhost:5173
- API docs: http://localhost:8000/docs

### Without Docker

```bash
# backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload --port 8000

# frontend (new terminal)
cd frontend
npm install
npm run dev
```

## Quick demo

1. Open the UI and click **Load sample data** (or `POST /api/v1/seed`).
2. Go to **Upload**, add a file with bad rows, and review the validation errors.
3. Click **Run detection** and check the Overview counts.
4. Open the account-takeover alert: failed logins, new device, beneficiary add, large transfer, High score with reasons.
5. Open the family shared-phone and regular-large-transfer cases: both stay Low with mitigating factors listed.
6. Mark a case **False Positive** and confirm the original alert is unchanged beside the audit trail.
7. Edit a threshold on the **Rules** page, re-run, and watch alerts change.

## Input data

| Dataset | Key fields |
| --- | --- |
| Customers and accounts | customer_id, account_id, full_name, dob, national_id, phone, email, address, onboarded_at |
| Transactions | txn_id, account_id, counterparty_account, amount, currency, ts, channel, status |
| Device and login logs | event_id, account_id, device_id, ip, ts, outcome, event_type |
| Loan applications | application_id, customer_id, device_id, amount, submitted_at, disbursement_account |

Records link through customer_id, account_id, device_id, application_id and txn_id.

## API overview

All endpoints are under `/api/v1`.

| Endpoint | Purpose |
| --- | --- |
| POST /ingest/preview, /ingest/commit | Validate and load a file |
| GET /ingest/batches | Batch history and counts |
| POST /detect/run | Run all detectors |
| GET /stats | Dashboard summary |
| GET /alerts, /alerts/{id} | List and inspect alerts |
| GET /customers/{id}/timeline | Customer context |
| GET /cases, /cases/{id} | Case queue and detail |
| POST /cases/{id}/decision | Record a decision |
| GET, PUT /config/rules | View and edit thresholds |
| POST /seed | Load sample data |
| GET /export/cases.csv | Export cases |

## How scoring works

```text
score = clamp( sum(weight x confidence) + combination_bonus - sum(mitigations), 0, 100 )
```

A high-value transfer scores Low for a customer who regularly sends similar sums, but High when it follows repeated failed logins, a new-device login and a beneficiary change. Weights and thresholds are in `backend/app/config/rules.yaml`.

## Testing

```bash
cd backend && pytest
cd frontend && npx playwright test
```

The seeded dataset contains labelled fraud and legitimate-lookalike cases. Tests assert expected alerts, risk bands and reasons.

## Security and privacy

- Use synthetic data only; no real customer data in the repository.
- Phone, national ID and email are masked in list views.
- JWT roles: Analyst (triage) and Supervisor (edit rules, close escalations).

## Roadmap

- Level 2: insurance claims (duplicate claims), deeper ring and mule-chain detection.
- Optional Claude API summaries that rephrase deterministic reasons; the model never scores.
- Neo4j for graph analysis at scale.

## License

Add your preferred license here.
