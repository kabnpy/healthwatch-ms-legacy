# Development Roadmap

## 🚩 Phase 1: The "Happy Path" MVP (Deadline: Showcase)
**Goal:** Demonstrate the "Perfect Day" scenario (New Business -> Print).
**Status:** In Progress.

- [ ] **Backend Core:** - [ ] Implement Models (Client, Policy, RiskNote, RiskItem).
  - [ ] Implement `TransactionType` Enum and `valid_from` fields (Foundation for Phase 2).
  - [ ] Create `seed_mock_data.py` script.
- [ ] **Frontend Foundation:**
  - [ ] Setup `features.ts` (Disable Endorsements/Claims).
  - [ ] Generate OpenAPI Client.
  - [ ] Create `useInsurance` hooks (React Query).
- [ ] **Views (Papermark Style):**
  - [ ] **Client Hub:** Grid of `InsuranceCard` components.
  - [ ] **Dashboard:** Tabbed view (Overview/History/Docs).
  - [ ] **Calculator:** "New Business" Modal (Auto-calc Premiums).
- [ ] **Output:**
  - [ ] **Print View:** CSS `@media print` layout for Risk Notes.

## 🚩 Phase 2: The "Time Traveler" (Post-MVP)
**Goal:** Handle the complexity of changing reality (Endorsements).
**Prerequisite:** Feature Flag `ENDORSEMENTS = true`.

- [ ] **Backend:** Implement `RiskItem` versioning logic (Expire old -> Create new).
- [ ] **Frontend:** Build "Endorsement Wizard" (Date Picker -> Delta View).
- [ ] **Math:** Implement Pro-Rata Premium calculation algorithms.
- [ ] **UI:** Enable "History" tab in Dashboard to show previous versions.

## 🚩 Phase 3: The "Financier" (Invoicing)
**Goal:** Handle Money In / Money Out.
**Prerequisite:** Feature Flag `PAYMENTS = true`.

- [ ] **Backend:** Create `Receipt` and `Allocation` models.
- [ ] **Frontend:** Build "Debit Note" Print View (Invoice styling of Risk Note).
- [ ] **Feature:** Payment splitting (One check paying for 3 policies).

## 🚩 Phase 4: The "Triager" (Claims)
**Goal:** Lifecycle management of losses.
**Prerequisite:** Feature Flag `CLAIMS = true`.

- [ ] **Backend:** `Claim` and `ClaimEvent` models.
- [ ] **Frontend:** Claims Timeline View / Status Tracker.
