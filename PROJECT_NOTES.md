# Project Notes: AI Lead Agent

## Phase 1: Environment & Database Foundation
- Initialized frontend with React (Vite + TypeScript + TailwindCSS).
- Initialized backend with FastAPI and Python.
- Created `docker-compose.yml` for PostgreSQL database.
- Created initial database models (`Lead`, `LeadHistory`) using SQLAlchemy.

## Architecture
- **Frontend**: React (Vite, TypeScript, TailwindCSS)
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL (SQLAlchemy ORM)
- **AI Agent**: To be implemented via a configurable LLM service layer.

## Important Files
- `docker-compose.yml`: Local PostgreSQL database setup.
- `backend/app/models/lead.py`: Database schema for Leads.

## Technologies Used & Why
- **FastAPI**: Extremely fast, built-in async support, automatic Swagger UI documentation, natively uses Pydantic which is great for validating AI outputs.
- **React**: Industry standard for building interactive dashboards.
- **PostgreSQL**: Reliable, structured relational database perfect for storing leads and history.
- **Docker**: Simplifies running the database locally without complex installations.

## Interview Preparation (Ongoing)
### 30-Second Pitch
"I built an AI-powered Lead Management System that acts as an intelligent agent. It ingests inbound leads, uses an LLM to classify their intent, extract key requirements, and draft a response. It features a human-in-the-loop dashboard where users can review the AI's recommendations before taking action."

### 1-Minute Explanation
(To be written...)

### Technical Explanation
(To be written...)

### Q&A
1. **Why FastAPI instead of Django/Flask?**
   *Answer*: FastAPI is built for speed and asynchronous operations, which is crucial when making API calls to an LLM. It also integrates perfectly with Pydantic for data validation, making it easier to parse structured JSON from the AI.

## Phase 2: Core REST API Development
- Built Pydantic schemas (`app/schemas/lead.py`) to enforce strict input/output data validation.
- Created CRUD operations (`app/crud/lead.py`) to handle database interactions securely.
- Exposed REST endpoints (`app/api/leads.py`) for creating, reading, updating, and deleting leads.
- Configured CORS in `main.py` to allow our future React frontend to communicate with the backend.

### Q&A
2. **Why use Pydantic for schemas?**
   *Answer*: Pydantic guarantees that the data entering our system is exactly what we expect (e.g. checking that an email is actually an email). It also automatically generates the Swagger API documentation in FastAPI. When working with LLMs, Pydantic is incredibly useful for forcing the AI to return structured, predictable JSON objects instead of messy text.

## Phase 3: The Agentic AI Workflow (The Brain)
- Integrated the `google-genai` SDK to interact with Google's Gemini models.
- Created `app/agent/prompts.py` containing the precise system instructions to analyze intent, extract requirements, determine priority, draft a response, and recommend the next action.
- Built the core agent workflow in `app/agent/workflow.py`. This uses **Structured Outputs** (forcing the LLM to return a strict JSON matching our Pydantic schema) for 100% reliable data parsing.
- Connected the workflow to the `POST /api/leads` endpoint using FastAPI's `BackgroundTasks`, so the AI analysis happens asynchronously and doesn't slow down the immediate API response.

### Q&A
3. **What is an Agentic Workflow and how is it different from a simple LLM call?**
   *Answer*: A simple LLM call just returns a block of text. An Agentic Workflow involves giving the AI specific roles, strict output formats (like JSON), and integrating it into a pipeline where its output directly drives system state changes (like updating database priorities and recommending human actions).
4. **Why run the AI analysis as a Background Task?**
   *Answer*: LLM APIs can take several seconds to respond. If we waited for the AI to finish during the HTTP request, the user interface would freeze. By using FastAPI's `BackgroundTasks`, we save the lead immediately, return a fast 200 OK response to the user, and let the AI do its heavy lifting in the background.

## Phase 4: Frontend Dashboard & Lead Management
- Created the React frontend using Vite.
- Installed and configured **TailwindCSS v4** for rapid UI styling.
- Built a clean, modern dashboard layout displaying system metrics.
- Connected the frontend to our FastAPI backend using `axios`.
- Built the **Simulate Inbound Lead** button to trigger full-stack testing instantly.

### Q&A
5. **How does the frontend stay up to date?**
   *Answer*: Currently, the React dashboard polls the backend API every 5 seconds to automatically fetch any updates. This ensures that as soon as the background Agentic Workflow finishes analyzing a lead, it appears live on the user's screen without a manual refresh. In a more advanced production environment, this could be upgraded to WebSockets for true real-time streaming.

## Phase 5: Human-in-the-Loop & Final Polish
- Built the **Review Modal** in React to display the AI's intent classification, extracted requirements, and the drafted email.
- Implemented human oversight actions: "Approve & Send Email" or "Discard Lead", which immediately update the backend database.
- Finalized architecture and technical explanation resources for interviews.

---

# 🎓 INTERVIEW PREPARATION GUIDE

## ⏱️ The 1-Minute Pitch
"For my portfolio, I built the AI Lead Agent, an end-to-end full-stack application designed to automate the initial triage of sales leads. 

When a new lead submits a message, the system uses an Agentic AI workflow powered by Google's Gemini to analyze their intent, extract key product requirements, and assign a priority level. It even drafts a highly contextual email response based on their exact needs.

However, I intentionally designed it with a 'Human-in-the-loop' architecture. Instead of automatically sending the email, the AI places the lead on a React dashboard. A sales rep can open the lead, review the AI's extracted data and drafted email, and click 'Approve & Send'.

I built the backend with FastAPI and Python because of its excellent asynchronous support for LLM API calls, used PostgreSQL with SQLAlchemy for data integrity, and React with Tailwind for a clean, responsive interface."

## 🧠 Detailed Technical Explanations & Q&A

**6. What makes this 'Agentic' instead of just an AI wrapper?**
An AI wrapper simply takes a user prompt, sends it to an LLM, and prints the text back. An Agentic Workflow involves giving the AI a specific persona, enforcing strict JSON output structures (using Pydantic and Structured Outputs), and writing business logic that reads that JSON to update database states, trigger background tasks, and recommend physical next actions.

**7. How did you ensure the AI's response doesn't break the application?**
I used Pydantic on the backend to define a strict JSON Schema, and passed that schema directly into the Gemini API `response_schema` parameter. This forces the LLM to output valid JSON matching my exact fields (`intent`, `priority`, `draft_response`). If it fails, Pydantic throws a validation error which I catch safely.

**8. Why did you use FastAPI?**
FastAPI is the industry standard for AI applications because it is built entirely around Python async/await, which is critical when waiting for third-party LLM APIs. It also natively integrates with Pydantic for data validation, which makes parsing AI JSON responses incredibly clean.

**9. How do you handle long AI wait times?**
I implemented FastAPI's `BackgroundTasks`. When a lead is submitted, the API saves the initial data to the database and immediately returns a `200 OK` response to the user. The heavy AI analysis runs asynchronously in the background.

**10. How would you scale this application?**
- **Database**: Add indexing to the `status` and `priority` columns for faster dashboard querying.
- **Background Tasks**: Replace FastAPI `BackgroundTasks` with a dedicated task queue like Celery and Redis to handle thousands of inbound leads without overwhelming the web server.
- **Frontend**: Replace API polling with WebSockets to stream AI completion events directly to the dashboard in real-time.
