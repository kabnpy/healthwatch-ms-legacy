# Initial Concept
NONE OF THESE HAVE IMMEDIATE PRIORITY WE HAVE MOST OF THE BASE FUNCTIONALITY WORKING SO WE NEED TO REFINE THAT UNTIL WE HAVE A PRODUCT WE CAN SHIP BEFORE IMPLEMENTING NEW FEATURES. BUT WE CAN FOCUS ON ENDORSMENTS NEXT

# Product Definition: HealthWatch MS

## 1. Vision & Purpose
HealthWatch MS is a high-performance Insurance Management System designed for minimalist efficiency. Inspired by the "Linear/Papermark" aesthetic, it unifies Client Management, Policy Administration, and Financial Invoicing into a streamlined workspace. The core goal is to provide insurance professionals with a "Dashboard" centric view that prioritizes context isolation and deep nesting to manage the inherent complexity of insurance data.

## 2. Product Quality & Evolution
- **Design Philosophy:** While grounded in the "Papermark" grid and 3-column tabbed interface, the product is in an experimental refinement phase. We actively seek to modernize UI patterns and variations that improve user experience.
- **Technical Excellence:** We maintain a balanced approach to technical debt. New features must be implemented with full TypeScript integrity, while existing type-safety issues are resolved incrementally as related modules are modified.
- **Development Priority:** The immediate focus is on refining the core "shippable" product. We prioritize stability, UX polish, and the hardening of existing base functionality over the introduction of new modules.

## 3. Core Functional Pillars
- **Client Hub:** A "Papermark" inspired portfolio view using a physical file/folder card metaphor for active covers.
- **Insurance Dashboard:** A deep-dive environment for policy management, history logging, and document storage.
- **Transaction Engine (Risk Notes):** Every policy change (New Business, Renewal, Endorsement) generates a locked Risk Note snapshot, ensuring temporal integrity and a clear audit trail.
- **Integrated Invoicing:** The Risk Note doubles as a Debit Note, providing valid tax invoice generation directly from policy data.

## 4. Immediate Roadmap Focus
1. **Stabilization & Refinement:** Hardening the base functionality and resolving UI/Type inconsistencies to reach a "shippable" state.
2. **Endorsement Flow:** Implementing mid-term policy modifications, including delta calculations and pro-rata adjustments.
