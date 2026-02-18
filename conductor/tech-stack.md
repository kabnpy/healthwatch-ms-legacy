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
