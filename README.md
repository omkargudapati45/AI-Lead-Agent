# AI Lead Agent – Intelligent Lead Management System

An end-to-end full-stack Agentic AI application that automates the triage, classification, prioritization, and response drafting for inbound sales leads while maintaining strict **Human-in-the-Loop** approval.

Built with **React, TypeScript, Tailwind CSS, FastAPI, SQLAlchemy, PostgreSQL / SQLite**, and **Google Gemini (google-genai SDK)**.

---

## 🌟 Core Features

- **Automated Lead Registration**: Ingest leads via REST API or through the interactive web dashboard.
- **Agentic Analysis Pipeline**:
  - **Intent Classification**: Identifies whether inquiries are purchase requests, support queries, partnerships, or spam.
  - **Information Extraction**: Automatically extracts product requirements, requested quantities, and deadlines.
  - **Priority Scoring**: Categorizes leads into `HIGH`, `MEDIUM`, `LOW`, or `DISCARD` based on business urgency.
  - **Contextual Email Drafting**: Crafts customized, professional sales responses tailored to the lead's exact requirements.
  - **Next-Action Recommendation**: Recommends concrete operational next steps (e.g., schedule demo, prepare quotation, call customer).
- **Human-in-the-Loop Oversight**: Drafted responses and recommendations require sales representative review and approval before execution.
- **Asynchronous Processing**: Background workers process AI operations without blocking user interactions or API response times.
- **Audit History Trail**: Every lead creation, status transition, and AI evaluation is logged in the database.

---

## 🏗️ Architecture & Workflow

```text
Inbound Lead (Web Form / API / WhatsApp)
                  │
                  ▼
          FastAPI Backend
                  │ (Immediate 200 OK + Persist Lead)
                  ▼
        Background AI Worker
                  │
                  ▼
         Google Gemini Agent
   (System Prompts + Structured JSON Output)
                  │
                  ├── Intent Classification
                  ├── Requirement Extraction
                  ├── Priority Determination
                  ├── Response Drafting
                  └── Action Recommendation
                  │
                  ▼
      Update Database & Audit Trail
                  │
                  ▼
        React SPA Dashboard
                  │
                  ▼
       [ Human-in-the-Loop ]
   (Review / Edit / Approve & Send)
```

---

## 🛠️ Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| **Frontend** | React 19, TypeScript, Vite, Tailwind CSS v4, Lucide Icons | High-performance reactive UI with type safety and modern styling |
| **Backend** | Python 3.13, FastAPI, Uvicorn | Native async/await support, automatic Swagger documentation, Pydantic integration |
| **AI / Agent** | Google GenAI SDK (`gemini-3.8-flash`) | Schema-enforced structured JSON output for guaranteed reliable parsing |
| **Database** | PostgreSQL (Docker) & SQLite (Local fallback), SQLAlchemy ORM | Robust relational persistence with zero-config local development fallback |
| **Validation** | Pydantic v2 | Strict schema validation for requests, responses, and AI structured outputs |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+ & npm
- Google Gemini API Key ([Google AI Studio](https://aistudio.google.com/))

---

### 1. Backend Setup

```bash
# Navigate to the backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows (PowerShell):
.\venv\Scripts\activate
# macOS / Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `backend/.env` with your API key:
```env
# Database (defaults to local SQLite if left commented)
# DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/aileaddb

# Gemini API Key
GEMINI_API_KEY=your_actual_gemini_api_key_here
LLM_PROVIDER=gemini
```

### 3. Start the Backend Server

```bash
uvicorn app.main:app --reload
```
The backend API and Swagger UI will be available at:
- **API Base:** `http://localhost:8000`
- **Swagger Docs:** `http://localhost:8000/docs`

---

### 4. Frontend Setup

In a new terminal window:
```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Start Vite development server
npm run dev
```
The React dashboard will be live at `http://localhost:5173`.

---

## 📡 REST API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/leads/` | Register new lead & trigger background AI analysis |
| `GET` | `/api/leads/` | List all leads with pagination |
| `GET` | `/api/leads/{id}` | Retrieve specific lead details |
| `PUT` | `/api/leads/{id}` | Update lead status / priority / human review |
| `DELETE` | `/api/leads/{id}` | Remove a lead record |
| `GET` | `/api/leads/{id}/history` | Retrieve complete audit trail for a lead |

---

## 🧠 Testing the Workflow

1. Open the web dashboard at `http://localhost:5173`.
2. Click **"Simulate Inbound Lead"** to trigger a test inquiry.
3. Observe the lead appear in the table with status `NEW`.
4. As the background worker finishes, watch the **Intent**, **Priority**, and **Recommended Action** populate.
5. Click **"Review AI Draft →"** to inspect the original inquiry alongside the AI's drafted email.
6. Click **"Approve & Send Email"** or **"Discard Lead"** to execute the human-in-the-loop decision.

---

## 🔒 Security & Privacy

- Secret keys (`.env`) and local databases (`*.sqlite`) are strictly excluded via `.gitignore`.
- API keys are injected via environment variables and never exposed to the client.

---

## 📄 License

MIT License. Free for educational and portfolio use.
