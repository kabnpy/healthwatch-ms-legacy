Context: We are upgrading the navigation architecture for our insurance agency management software. The application has deeply nested views (e.g., specific policies within client profiles), and users are losing context. We need to implement breadcrumbs in the main layout using Shadcn UI.

Technical Stack: React, Shadcn UI, File-based Routing (e.g., TanStack Router/React Router).

Task Checklist:

1. Component Installation

    [ ] Run the CLI command to add the Shadcn Breadcrumb component: npx shadcn@latest add breadcrumb.

    [ ] Ensure the component is installed in frontend/src/components/ui/breadcrumb.tsx.

2. Architecture & Refactor

    [ ] Extract Header: Create a new component frontend/src/components/layout/Header.tsx.

        Move the existing navbar/header code from frontend/src/routes/_layout.tsx into this new file.

        Import and render <Header /> inside _layout.tsx to maintain current functionality before adding new features.

    [ ] Route Definition (Crucial): Refactor the Client View tabs (Overview, Policies, Documents, Invoices) to be true nested routes rather than just simple state-switched tabs.

        Goal: The URL should reflect the tab, e.g., /clients/123/invoices.

        Reason: This allows the breadcrumb generator to map the URL segments directly to the UI.

3. Breadcrumb Implementation Logic

    [ ] Create a utility hook or function (e.g., useBreadcrumbs) that:

        Parses the current location path (e.g., /clients/123/policies).

        Splits the path into segments.

        Maps dynamic IDs (like 123) to readable names if possible (or keeps the ID as a fallback for now).

        Returns an array of objects: { label: string, href: string }.

    [ ] Admin Handling: Ensure the logic handles the /admin prefix gracefully (e.g., Home > Admin > User Management).

4. UI Integration

    [ ] Integrate the Breadcrumb component into frontend/src/components/layout/Header.tsx.

    [ ] Visual Style Guide:

        Use the "Separator" icon (chevron or slash) consistent with our existing iconography.

        Ensure the active page (last item) is distinct (bold or darker text) but not clickable.

        Maintain "High-Trust" aesthetics: Avoid clutter. Place the breadcrumbs strictly above the main page content or within the top header bar.

5. Verification

    [ ] Verify that navigating to a Client's "Invoice" tab generates: Home > Clients > [Client Name/ID] > Invoices.

    [ ] Verify that the back button works as expected with the new route-based tabs.
