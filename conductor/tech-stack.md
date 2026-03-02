# Tech Stack: HealthWatch MS

## Backend
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **ORM:** SQLModel (with SQLAlchemy and Pydantic)
- **Database:** PostgreSQL
- **Migrations:** Alembic
- **Authentication:** JWT (PyJWT) with Passlib (bcrypt) and **Simplified RBAC**
- **Testing:** Pytest (TDD driven with focus on precision and state filtering)
- **Financial Precision:** Python `Decimal` with fixed-point arithmetic for all premium math.
- **Data Patterns:**
    - **Atomic Snapshots:** Every policy transaction (New Business, Renewal) is stored
 as a 100% complete snapshot of the cover in the `RiskNote` table.
    - **Dynamic Snapshot Storage:** Flexible JSON schemas are used for product-specific cover data within snapshots, ensuring the system can support multiple insurance classes without migrations.
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
