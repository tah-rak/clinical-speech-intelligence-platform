# Clinical Speech Intelligence Platform

A production-quality healthtech AI platform that converts doctor-patient speech audio into structured clinical documentation — transcripts, medical entities, SOAP notes, and visit summaries.


## Project Overview

CSIP is an end-to-end clinical speech intelligence pipeline:

1. **Upload** clinical audio (WAV, MP3, M4A) or use a sample transcript
2. **Transcribe** with local faster-whisper (default) or optional Azure/GCP STT
3. **Extract** medical entities (symptoms, medications, allergies, etc.)
4. **Generate** SOAP notes via Ollama or template fallback
5. **Review** and edit documentation with clinician workflow status
6. **Evaluate** transcription quality with Word Error Rate (WER)

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────────────────────┐
│   React     │────▶│   FastAPI    │────▶│  PostgreSQL (local) / Firestore │
│   Frontend  │     │   Backend    │     └─────────────────────────────────┘
└─────────────┘     └──────┬───────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
  │ faster-     │   │ Entity      │   │ SOAP Gen    │
  │ whisper STT │   │ Extraction  │   │ Ollama/     │
  │ (local)     │   │ spaCy+rules │   │ Template    │
  └─────────────┘   └─────────────┘   └─────────────┘
         │                 │
         ▼                 ▼
  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
  │ Azure STT   │   │ Local       │   │ AWS S3      │
  │ (optional)  │   │ Storage     │   │ (optional)  │
  └─────────────┘   └─────────────┘   └─────────────┘
```

## Features

- Audio upload with visit metadata (patient, clinician, date, reason)
- Speech-to-text with provider abstraction (local Whisper, Azure, GCP)
- Speaker-aware transcript formatting (estimated turn-based labels)
- Medical entity extraction (rule-based + spaCy)
- SOAP note generation (Ollama or deterministic template)
- Visit summaries and action items
- Analytics dashboard with metrics and charts
- WER evaluation for transcription quality
- Optional cloud integrations: AWS S3, Azure Speech, GCP Firestore/Cloud Run/Firebase Hosting
- Dark/light mode UI

## Tech Stack

| Layer | Technologies |
|-------|-------------|
| Backend | Python 3.11, FastAPI, SQLAlchemy, PostgreSQL |
| ML/NLP | faster-whisper, spaCy, rule-based extraction |
| Frontend | React 18, Vite, Tailwind CSS, Recharts |
| DevOps | Docker, Docker Compose, Makefile |
| Cloud (optional) | AWS S3, Azure AI Speech, GCP Cloud Run, Firebase Hosting, Firestore |

## Security and public release

See [SECURITY.md](SECURITY.md) for what is safe to publish.

**Before your first public push:**

```bash
git status                    # ensure .env files are NOT listed
git check-ignore backend/.env # should print a .gitignore rule
```

- Never commit `backend/.env`, `frontend/.env`, API keys, or credential JSON files.
- Port numbers in this README (`5173`, `8000`) are **local development defaults** only — they are not a vulnerability on their own because they bind to `localhost`.
- Default Docker credentials (`csip`) are for **local dev only** — change them before any production deployment.

## Disclaimer

This application is a research and portfolio prototype. It is **not a medical device** and must not be used for diagnosis or treatment decisions. All generated notes require clinician review. Designed with privacy-aware architecture patterns, but **not certified for clinical production use** or HIPAA compliance.

## Quick Start (Docker)

```bash
# 1. Clone the repository
git clone 
cd clinical-speech-intelligence-platform

# 2. Copy environment files
make setup

# 3. Start all services
make docker-up

# 4. Open the app
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Local Development (without Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
cp .env.example .env
# Start PostgreSQL locally or update DATABASE_URL
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
# Open http://localhost:5173
```

## Process a Sample Visit

1. Go to **Upload Visit**
2. Enter patient/clinician info
3. Check **"Use sample transcript"** (no audio needed)
4. Click **Upload and Process**
5. View the visit detail: transcript → entities → SOAP note → summary

Or upload your own `.wav`, `.mp3`, or `.m4a` file for full transcription.

## Makefile Commands

| Command | Description |
|---------|-------------|
| `make dev` | Start Docker Compose stack |
| `make backend` | Run backend locally |
| `make frontend` | Run frontend dev server |
| `make test` | Run backend tests |
| `make docker-up` | Build and start containers |
| `make docker-down` | Stop containers |
| `make setup` | Copy `.env.example` files |

## Environment Variables

See `backend/.env.example` for the full list. Key variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `STT_PROVIDER` | `local` | `local`, `azure`, or `gcp` |
| `STORAGE_PROVIDER` | `local` | `local` or `s3` |
| `DATABASE_URL` | PostgreSQL connection string | |
| `WHISPER_MODEL` | `base` | Whisper model size |
| `AWS_ENABLED` | `false` | Enable S3 storage |
| `AZURE_SPEECH_ENABLED` | `false` | Enable Azure STT |
| `GCP_ENABLED` | `false` | Enable GCP services |
| `LLM_ENABLED` | `false` | Enable plug-and-play LLM for SOAP notes |
| `LLM_PROVIDER` | `openai` | Preset name — see `backend/app/services/llm/presets.py` |
| `OLLAMA_ENABLED` | `false` | Legacy flag; prefer `LLM_PROVIDER=ollama` |

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check and provider status |
| POST | `/api/uploads` | Upload audio and visit metadata |
| POST | `/api/visits/{id}/transcribe` | Run speech-to-text |
| POST | `/api/visits/{id}/entities` | Extract medical entities |
| POST | `/api/visits/{id}/soap` | Generate SOAP note |
| GET | `/api/visits` | List visits |
| GET | `/api/visits/{id}` | Get visit details |
| PATCH | `/api/visits/{id}/soap` | Update SOAP note |
| PATCH | `/api/visits/{id}/status` | Update review status |
| GET | `/api/analytics` | Dashboard metrics |
| POST | `/api/evaluation/wer` | Calculate Word Error Rate |

Interactive docs: `http://localhost:8000/docs`

## AWS S3 Setup

See [infra/aws/README.md](infra/aws/README.md) for bucket creation, IAM policy, and optional Lambda trigger.

```env
AWS_ENABLED=true
STORAGE_PROVIDER=s3
AWS_REGION=us-east-1
AWS_S3_BUCKET=your-bucket
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
```

## Azure Speech Setup

1. Create an [Azure Speech resource](https://portal.azure.com)
2. Copy the key and region

```env
STT_PROVIDER=azure
AZURE_SPEECH_ENABLED=true
AZURE_SPEECH_KEY=your-key
AZURE_SPEECH_REGION=eastus
```

Falls back to local Whisper if credentials are missing.

## GCP Deployment

### Cloud Run (Backend)

```bash
gcloud builds submit --config cloudbuild.yaml
# Or manually:
docker build -t gcr.io/PROJECT_ID/csip-backend ./backend
docker push gcr.io/PROJECT_ID/csip-backend
gcloud run deploy csip-backend \
  --image gcr.io/PROJECT_ID/csip-backend \
  --region us-central1
  # Add --allow-unauthenticated only if you intend a public API; use auth in production
```

### Firebase Hosting (Frontend)

```bash
cd frontend && npm run build
firebase init hosting
firebase deploy --only hosting
```

### Firestore (Optional Database)

```env
GCP_ENABLED=true
DATABASE_PROVIDER=firestore
FIRESTORE_PROJECT_ID=your-project
GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json
```

## Folder Structure

```
clinical-speech-intelligence-platform/
├── backend/
│   ├── app/
│   │   ├── api/routes/       # REST API endpoints
│   │   ├── core/             # Config, logging, security
│   │   ├── models/           # SQLAlchemy models & Pydantic schemas
│   │   ├── services/
│   │   │   ├── storage/      # Local & S3 providers
│   │   │   ├── transcription/  # Whisper, Azure, GCP
│   │   │   ├── nlp/          # Entity extraction
│   │   │   ├── soap/         # SOAP generation
│   │   │   ├── analytics/    # Dashboard metrics
│   │   │   └── evaluation/   # WER calculation
│   │   └── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/              # API client
│   │   ├── components/       # UI components
│   │   └── pages/            # Route pages
│   └── Dockerfile
├── infra/aws/                # Lambda & AWS setup guide
├── sample_data/              # Demo transcripts & mock outputs
├── docker-compose.yml
├── Makefile
└── README.md
```

## Future Improvements

- True speaker diarization with pyannote.audio
- scispaCy biomedical NER models
- Real-time streaming transcription
- User authentication and RBAC
- FHIR export for EHR integration
- Fine-tuned clinical NER models
- Batch processing queue (Celery/Redis)
- Audit logging for compliance patterns



