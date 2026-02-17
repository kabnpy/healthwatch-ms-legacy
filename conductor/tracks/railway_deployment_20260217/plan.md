# Implementation Plan: Railway Deployment

This plan details the steps to deploy the HealthWatch MS full-stack application to Railway.com using separate services for the backend and frontend, and a managed PostgreSQL database.

## Phase 1: Project Setup & CLI Configuration [checkpoint: 5d9c6b7]
Initial setup and linking the local environment to Railway.

- [x] Task: Install and authenticate the Railway CLI on the development machine. (manual)
- [x] Task: Create a new Railway project using the Railway CLI. (manual)
- [x] Task: Link the local repository to the newly created Railway project. (manual)
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Project Setup & CLI Configuration' (Protocol in workflow.md)

## Phase 2: Database Provisioning & Configuration [checkpoint: 03fae9b]
Setting up the persistent data layer.

- [x] Task: Provision a Managed PostgreSQL database service within the Railway project. (manual)
- [x] Task: Extract the database connection string and verify connectivity from the local environment using the Railway CLI. (manual)
- [x] Task: Synchronize database environment variables (e.g., `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`) with the Railway project. (manual)
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Database Provisioning & Configuration' (Protocol in workflow.md)

## Phase 3: Backend Deployment & Verification [checkpoint: ]
Deploying and hardening the API service.

- [ ] Task: Configure all required backend environment variables in Railway (e.g., `SECRET_KEY`, `CORS_ORIGINS`).
- [ ] Task: Deploy the backend service from the `backend/` directory using `railway up`.
- [ ] Task: Execute database migrations against the Railway PostgreSQL instance using the backend service.
- [ ] Task: Verify the backend health check endpoint on the public Railway URL.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Backend Deployment & Verification' (Protocol in workflow.md)

## Phase 4: Frontend Deployment & Verification [checkpoint: ]
Deploying and connecting the UI service.

- [ ] Task: Update the `VITE_API_URL` environment variable to point to the newly deployed backend public URL.
- [ ] Task: Configure frontend build and start commands in Railway (using Nixpacks or custom configuration).
- [ ] Task: Deploy the frontend service from the `frontend/` directory using `railway up`.
- [ ] Task: Verify the frontend accessibility and successful API connection on the public Railway URL.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Frontend Deployment & Verification' (Protocol in workflow.md)

## Phase 5: Integration & Final Smoke Test [checkpoint: ]
Ensuring the full system is functional in production.

- [ ] Task: Perform a comprehensive smoke test of the application in the production environment (Login, Policy Creation, Invoice Generation).
- [ ] Task: Document the final production URLs and any environment-specific maintenance procedures.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Integration & Final Smoke Test' (Protocol in workflow.md)
