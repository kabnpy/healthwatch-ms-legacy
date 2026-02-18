# Product Guidelines: HealthWatch MS

## 1. Visual Identity & Design Principles
- **Aesthetic Core:** Prioritize **Modern Minimalism**. Use high-quality typography and intentional whitespace to create a clean, professional workspace. The design should feel airy and efficient, removing all unnecessary metaphors or "boxed-in" containers.
- **Brand Palette:** Employ **Subtle Neutrals**. Use a soft palette of grays and off-whites consistently across the entire system. Reserve professional accents (like corporate blue or green) for primary actions and system feedback.
- **Visual Weight:** Let spacing and type scale carry the design. Use borders and dividers sparingly to define structure without adding visual clutter.

## 2. User Experience & Interaction
- **Workflow Management:** Use **Sequential Wizards** for complex, multi-step processes (e.g., Endorsements, New Business). Break down data entry into logical, manageable steps to minimize cognitive load.
- **Authoritative Feedback:** Ensure wizards provide real-time, backend-validated calculations (e.g., live quotes) to maintain a "Single Source of Truth" and prevent client-side discrepancies.
- **Navigation:** Utilize a **Minimalist Sidebar (inset variant)** for high-level navigation. Within content areas, use **Layered Navigation** driven by clear typographic headers and breadcrumbs to ensure the user always feels grounded in their context.
- **State Feedback:** Implement **Contextual & Instructive** empty states. Guide the user toward the next logical action. Use skeleton loaders to maintain layout stability during data fetching.

## 3. Prose & Communication
- **Tone:** **Direct & Clear**. Use simple, action-oriented language. Eliminate jargon where possible while maintaining professional insurance accuracy (e.g., Endorsement, Risk Note).
- **Action Labels:** Use high-frequency, descriptive verbs for buttons and links (e.g., "Issue Risk Note" instead of just "Create").
- **Guidance:** Microcopy should be concise and helpful, focusing on the "what" and "how" of the immediate task.

## 4. Technical Standards for UI
- **Type Safety:** All new UI components must be fully typed. Use Zod for schema validation and ensure tight integration with the auto-generated backend client.
- **Consistency:** Leverage the existing Shadcn/UI component library and Tailwind CSS v4 patterns to ensure a unified look and feel across all views. Standardize on consistent border radii and background treatments.
