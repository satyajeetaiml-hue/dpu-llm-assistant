# University AI Assistant

A multi-agent, Retrieval-Augmented-Generation (RAG) assistant for universities,
built on **Azure AI Foundry** (Azure OpenAI), **Azure AI Search**, and
**Azure Blob Storage**. A triage agent routes each question to a specialist —
student services, admissions, compliance/CIQA, or marketing — and every answer
is grounded in indexed university documents with inline citations.

```
┌──────────┐   /api/chat   ┌──────────────┐   route    ┌──────────────────┐
│ React UI │ ────────────► │ Triage Agent │ ─────────► │ Specialist Agent │
└──────────┘               └──────────────┘            └─────────┬────────┘
                                                                 │ retrieve
                                                       ┌─────────▼────────┐
                                                       │ Azure AI Search  │◄── embeddings
                                                       └──────────────────┘     (Azure OpenAI)
```

## Tech stack

| Layer        | Technology                                              |
|--------------|---------------------------------------------------------|
| Frontend     | React 18, Vite, React Router, Recharts, Axios           |
| Backend      | FastAPI, Pydantic v2, Uvicorn                           |
| LLM / Embed  | Azure AI Foundry (Azure OpenAI chat + embeddings)       |
| Retrieval    | Azure AI Search (hybrid keyword + vector)               |
| Storage      | Azure Blob Storage                                      |
| Infra        | Bicep, Terraform, Azure Pipelines, GitHub Actions       |

## Project structure

```
backend/    FastAPI app — api/, agents/, services/, rag/, models/
frontend/   Vite + React SPA — pages/, components/, hooks/, services/
scripts/    Index creation, document ingestion, blob sync
infrastructure/  Bicep + Terraform + Azure Pipelines
documents/  Source documents by category (admissions, policies, ciqa, …)
```

## Prerequisites

- Python 3.12+
- Node.js 20+
- An Azure subscription with: an Azure OpenAI resource (a chat + an embedding
  deployment), an Azure AI Search service, and a Storage account.

## Quick start (local)

### 1. Configure environment

```bash
cp .env.example .env
# Fill in the AZURE_* values.
```

### 2. Backend

```bash
cd backend
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs · Health: http://localhost:8000/api/health

### 3. Frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173 (the Vite dev server proxies `/api` → `:8000`).

### 4. Build the index and ingest documents

Drop `.txt` / `.md` files into `documents/<category>/`, then:

```bash
python scripts/build_index.py        # create the Azure AI Search index
python scripts/sync_blob_storage.py  # upload raw files to Blob Storage
python scripts/ingest_documents.py   # chunk + embed + index for retrieval
```

> The upload API and ingestion script parse `.txt`/`.md` in this scaffold.
> Wire in `pypdf` / `python-docx` in `backend/app/api/upload.py` and
> `scripts/ingest_documents.py` to support PDFs and Word docs.

## Run with Docker

```bash
docker compose up --build
# Frontend → http://localhost:8080   Backend → http://localhost:8000
```

## API surface

| Method | Path                       | Description                          |
|--------|----------------------------|--------------------------------------|
| GET    | `/api/health`              | Service health / version             |
| POST   | `/api/chat`                | Ask a question (auto-routed)         |
| POST   | `/api/upload`              | Upload + index a document            |
| GET    | `/api/analytics/admissions`| Admission metrics (sample data)      |

## Agents

| Agent       | Scope                                            | Doc category |
|-------------|--------------------------------------------------|--------------|
| `triage`    | Classifies intent and routes the message         | —            |
| `student`   | Courses, results, fees, general student queries  | all          |
| `admission` | Eligibility, programs, deadlines, applications   | admissions   |
| `compliance`| Policies, exam regulations, CIQA accreditation   | ciqa         |
| `marketing` | Prospectus, events, promotional content          | all          |

## Deployment

- **Bicep:** `az deployment group create -g <rg> -f infrastructure/bicep/main.bicep`
- **Terraform:** `cd infrastructure/terraform && terraform init && terraform apply`
- **CI:** GitHub Actions in `.github/workflows/` lint/build each side; an Azure
  Pipelines template builds & pushes container images.

## Notes & TODOs

- `analytics` returns sample data — connect it to your data warehouse.
- Auth is JWT-based; in `development` the API allows anonymous access. Set
  `ENVIRONMENT` to anything else to enforce bearer tokens.
- Consider `azure-identity` (managed identity) instead of API keys in production.
