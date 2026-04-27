# Operations & Rollback Guide

## 1. Database Rollback Protocol

### Alembic Downgrades
If a database migration causes issues, you can revert it using Alembic.

1.  **Identify current version:**
    ```bash
    cd backend
    uv run alembic current
    ```
2.  **Downgrade by one version:**
    ```bash
    uv run alembic downgrade -1
    ```
3.  **Downgrade to a specific version:**
    ```bash
    uv run alembic downgrade <revision_id>
    ```

**Caution:** Downgrading may result in data loss if columns or tables are dropped. Always backup before running migrations in production.

### Data Backups (Neon.tech)
Our Postgres database is hosted on Neon.tech.
- Use the Neon Console to create a branch/snapshot before major migrations.
- In case of catastrophic failure, point the application to a previous branch snapshot.

## 2. Deployment Rollback

### Docker / Railway
If a new deployment is unstable:
1.  **Revert to Previous Image:** Identify the previous successful build tag in the registry and redeploy it.
2.  **Git Revert:** 
    ```bash
    git revert <commit_hash>
    git push origin <branch>
    ```

## 3. Monitoring & Health Checks

### Backend Logs
- Logs are streamed to the console in structured format.
- Request logging middleware captures: `method`, `path`, `status_code`, and `duration`.

### Frontend Errors
- A global `ErrorBoundary` is in place to catch unhandled React crashes.
- Global API error toasts are handled via `TanStack Query`'s `onError` cache handlers.

## 4. Emergency Contacts
- **Primary Underwriter:** [Name]
- **Technical Lead:** [Name]
