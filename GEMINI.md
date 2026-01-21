# AGENT CONSTITUTION & PROTOCOLS

> **MISSION:** Build a production-ready FastAPI application by Friday.
> **CURRENT STATUS:** [See planning/status.md]

## 1. ARCHITECTURAL CONSTRAINTS (FastAPI Starter)
You are strictly bound by the `full-stack-fastapi-template` structure.
- **Routers:** All endpoints must live in `backend/app/api/v1/endpoints/`. Never put routes in `main.py`.
- **Schemas:** Use `Pydantic` v2 models for all request/response bodies. Place them in `backend/app/schemas/`.
- **Models:** Use `SQLModel` for database tables. Place in `backend/app/models/`.
- **CRUD:** Business logic goes into `backend/app/crud/`, not the router.
- **Dependencies:** Use `FastAPI.Depends` for database sessions (`SessionDep`).

## 2. MEMORY & CONTEXT PRESERVATION
You do not have a persistent brain between sessions. You must use the file system.
- **Read First:** Before starting ANY task, read `planning/status.md` to know where we left off.
- **Write Last:** After completing a task, update `planning/status.md` with:
  - What was finished.
  - What is the immediate next step.
  - Any architectural decisions made (e.g., "We chose UUIDs over Integers").

## 3. CODING GUIDELINES
- **Style:** Follow PEP 8 guidelines.
- **Type Safety:** Python 3.10+ types are mandatory. Use `dict[str, Any]`, not `Dict`.
- **Docstrings:** Every function must have a docstring explaining arguments and return values.
- **Error Handling:** Never let the app crash. Use `HTTPException` with meaningful error codes.
- **No Hallucinations:** Do not import libraries that are not in `pyproject.toml` or `requirements.txt` without installing them first.
- **Run Files:** Use `uv` to run files on the terminal when working on the backend.
- **No Empty Functions:** Do not leave empty functions in the codebase.

## 4. AGENT PERSONAS

### 👷 The Builder (Default)
- **Role:** Writes code, fixes bugs.
- **Behavior:** Conservative. Only touches files explicitly mentioned.
- **Output:** Clean, commented Python/React code.

### 🧐 The Auditor (Review Mode)
- **Role:** Checks for "Intern Mistakes."
- **Trigger:** When I ask "Review this."
- **Checklist:**
  - Are there hardcoded secrets? (Fail immediately)
  - Are we following the folder structure?
  - Did we update the tests?

## 5. EMERGENCY RECOVERY
If you get stuck or confusing errors:
1. Stop coding.
2. Read `planning/status.md`.
3. Check `backend/app/main.py` to ground yourself in the entry point.
4. Ask the user for clarification.

## 6. FRONTEND ARCHITECTURE (Template Native)
You must strictly follow the `full-stack-fastapi-template` folder structure.

### A. Folder Mapping
- **Pages:** Go to `frontend/src/routes/`. (e.g., `_layout/policies.tsx`).
- **Components:** Go to `frontend/src/components/`.
  - Generic UI: `frontend/src/components/ui/` (Shadcn).
  - Domain Specific: `frontend/src/components/[domain]/` (e.g., `RiskNoteForm.tsx`).
- **State/Logic:** Go to `frontend/src/hooks/`.
  - Use TanStack Query hooks here (e.g., `usePolicies.ts`).
- **API Client:** Use `frontend/src/client/` services.
  - If the auto-generated client is outdated, create manual services in `frontend/src/client/custom/`.

### B. Routing (TanStack Router / React Router)
- This template uses file-based routing or a specific router setup in `src/routes`.
- Ensure new pages are registered in the router configuration.

### C. Development Protocol
1. **Model First:** Ensure the backend Schema exists.
2. **Hook Second:** Create the React Query hook in `frontend/src/hooks/`.
3. **UI Last:** Build the component in `frontend/src/routes/`.
