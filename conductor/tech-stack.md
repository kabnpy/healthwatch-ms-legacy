# Tech Stack: HealthWatch MS

## Backend
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **ORM:** SQLModel (with SQLAlchemy and Pydantic)
- **Database:** PostgreSQL
- **Migrations:** Alembic
- **Authentication:** JWT (PyJWT) with Passlib (bcrypt) and **Simplified RBAC**
- **Testing:** Pytest (TDD driven with focus on precision and state filtering)
- **PDF Generation:** WeasyPrint (High-fidelity HTML-to-PDF conversion for A4 documents)
- **Financial Precision:** Python `Decimal` with fixed-point arithmetic for all premium math.
- **Data Patterns:**
    - **Modular Domain Architecture:** Models and CRUD logic are organized into specialized domain-specific modules (Clients, Policies, Claims, Auth) with a unified export pattern for maintainability.
    - **Atomic Snapshots:** Every policy transaction (New Business, Renewal) is stored
 as a 100% complete snapshot of the cover in the `RiskNote` table.
    - **Hybrid Snapshot Storage:** Flexible JSON schemas are used for product-specific cover data, complemented by a static template selection engine in the backend to ensure precise document layouts for different insurance classes.
    - **Clean Container Pattern:** The `Policy` table is a stable identity container, free of temporal state, which instead resides in the versioned `RiskNote` snapshots.

## Frontend
- **Language:** TypeScript
- **Framework:** React 19 (using Vite)
- **Routing:** TanStack Router
- **Data Fetching:** TanStack Query
- **Styling:** Tailwind CSS v4 & Shadcn/UI
- **Validation:** Zod & React Hook Form
- **Testing:** Playwright (E2E)

## Infrastructure & DevOps
- **Containerization:** Docker & Docker Compose
- **Reverse Proxy:** Traefik
- **Package Management:** UV (Backend), PNPM/NPM (Frontend)
