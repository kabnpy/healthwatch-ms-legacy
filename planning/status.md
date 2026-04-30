# Project Status (Current Session: 2026-04-30)

## Executive Summary
The project has moved into a **System Architecture Refinement** phase, focusing on strict decoupling of business logic from data models, centralization of frontend utilities, and route modularization. Core document generation is stable and unified across the stack.

## Major Milestones (Completed)
- **Backend Decoupling**: Business logic moved from SQLModel classes (Product, RiskNote) to dedicated Service layers (`ProductService`, `RiskNoteService`).
- **Frontend Centralization**: Document URL generation and download orchestration unified in `DocumentService`.
- **Error Boundary Standardization**: Implemented standard `ErrorFallback` components and route-level error boundaries.
- **Model Hardening**: Added strict schema validation for Motor Private risk details to prevent data corruption.
- **Dashboard Modularization**: Extracted `ActionToolbar` as part of the decomposition of the Policy Dashboard "God" file.

## Current Status (Ongoing)
- **Phase 3: Frontend Route Modularization**: Further decomposing the Policy Dashboard into domain-specific components (`TransactionHistory`, `FinancialOverview`).
- **Phase 4: E2E Test Suite**: Preparing Playwright foundation for full workflow verification.

## Immediate Next Steps
1. **Decompose Policy Dashboard**: Complete extraction of `TransactionHistory` and refactor the main dashboard route.
2. **Audit "God" Files**: Review and modularize `NewPolicyWizard.tsx` and `ClientInvoices.tsx`.
3. **E2E Foundation**: Setup Playwright fixtures for authenticated user states.

## Key Architectural Decisions
- **Anemic Models**: SQLModel classes are strictly for data definition and relationships. All business logic must reside in services.
- **Service-Driven UI**: Frontend components use dedicated service classes for complex orchestrations (e.g., DocumentService) instead of scattered utility functions.
- **Standardized Fallbacks**: Every major UI section must have a corresponding error fallback to ensure graceful degradation.
