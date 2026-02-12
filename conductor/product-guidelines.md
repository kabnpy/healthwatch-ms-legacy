# Product Guidelines: HealthWatch MS

## 1. Visual Identity & Design Principles
- **Aesthetic Core:** Prioritize **Visual Clarity**. Maintain a clean, minimalist "physical folder" metaphor using ample whitespace and simple UI elements.
- **Brand Palette:** Employ **Subtle Neutrals**. Use a soft palette of grays and off-whites to enhance the "physical paper" feel. Reserve professional accents (like corporate blue or green) for positive actions and system feedback.
- **Modernization:** While evolving the design, avoid clutter. Every UI addition should justify its presence by improving clarity or efficiency without sacrificing the minimalist foundation.

## 2. User Experience & Interaction
- **Workflow Management:** Use **Sequential Wizards** for complex, multi-step processes (e.g., Endorsements, New Business). Break down complex data entry into manageable, logical steps to reduce cognitive load.
- **State Feedback:** Implement **Contextual & Instructive** empty states. Use "Empty State" areas to guide the user toward the next logical action (e.g., "Create your first cover"). Use skeleton loaders to maintain layout stability and provide a smooth perceived performance.
- **Navigation:** Maintain the 3-column tabbed interface for deep-dive contexts, ensuring the user always feels grounded in their current task.

## 3. Prose & Communication
- **Tone:** **Direct & Clear**. Use simple, action-oriented language.
- **Terminology:** Balance accessibility with industry accuracy. Use precise insurance terms (Endorsement, Risk Note, Debit Note) where necessary for legal or professional clarity, but avoid unnecessary jargon in general navigation and instructions.
- **Guidance:** Microcopy should be helpful and concise, focusing on the "what" and "how" of the immediate task.

## 4. Technical Standards for UI
- **Type Safety:** All new UI components must be fully typed. Use Zod for schema validation and ensure tight integration with the auto-generated backend client.
- **Consistency:** Leverage the existing Shadcn/UI component library and Tailwind CSS v4 patterns to ensure a unified look and feel across all views.
