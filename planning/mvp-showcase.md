# 🚀 MVP EXECUTION PROTOCOL (Branch: `feature/mvp-showcase`)

> **MISSION:** Build the "Client -> Policy -> Risk Note -> Print" workflow.
> **STRATEGY:** Use `uv` for local execution + `seed_mock_data` for data.
> **STATUS:** [ ] Not Started

---

## 🟢 STEP 1: BACKEND DATA INJECTION (Local w/ UV)
**Goal:** Inject mock data without entering the Docker container.
**Prerequisite:** Ensure your database is running: `docker compose up -d db`
**Action:**
1.  The `prestart.sh` script is generally used to inject data. this is done by the prestart docker service. You may reference, extend it, or create a new script.
2.  Use the script below for reference (It creates Jubilee, Motor Product, John Doe, Policy, and Risk Note)
    ```python
    # File: backend/app/seed_mock_data.py
    import logging
    import os
    from datetime import date, timedelta
    from sqlmodel import Session, select
    
    from app.db.engine import engine
    from app.models import Client, Policy, RiskNote, RiskItem, Insurer, Product
    
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    def create_mock_data():
        with Session(engine) as session:
            # 1. SETUP THE CATALOG
            insurer = session.exec(select(Insurer).where(Insurer.name == "Jubilee Insurance")).first()
            if not insurer:
                insurer = Insurer(name="Jubilee Insurance", email="claims@jubilee.com")
                session.add(insurer)
                session.commit()
                session.refresh(insurer)
    
            product = session.exec(select(Product).where(Product.name == "Motor Private - Gold")).first()
            if not product:
                product = Product(
                    insurer_id=insurer.id,
                    name="Motor Private - Gold",
                    class_of_insurance="Motor Private",
                    default_benefits={"towing": 50000, "windscreen": 50000, "excess": "2.5% of Value"},
                    default_commission_rate=12.5
                )
                session.add(product)
                session.commit()
                session.refresh(product)
    
            # 2. CREATE CLIENT
            client = session.exec(select(Client).where(Client.kra_pin == "A001234567Z")).first()
            if not client:
                client = Client(
                    name="John Doe", 
                    kra_pin="A001234567Z", 
                    phone="0712345678", 
                    physical_address="Westlands, Nairobi",
                    email="john@example.com"
                )
                session.add(client)
                session.commit()
                session.refresh(client)
    
            # 3. CREATE POLICY
            policy = session.exec(select(Policy).where(Policy.policy_number == "P/001/2026")).first()
            if not policy:
                policy = Policy(
                    policy_number="P/001/2026",
                    client_id=client.id,
                    product_id=product.id,
                    status="Active"
                )
                session.add(policy)
                session.commit()
                session.refresh(policy)
    
            # 4. CREATE RISK ITEM (The Car)
            item = session.exec(select(RiskItem).where(RiskItem.identifier == "KCA 123B")).first()
            if not item:
                item = RiskItem(
                    policy_id=policy.id,
                    identifier="KCA 123B",
                    description="Toyota Harrier",
                    sum_insured=2500000.0,
                    details={"make": "Toyota", "chassis": "JMZ..."},
                    benefits=product.default_benefits
                )
                session.add(item)
                session.commit()
    
            # 5. CREATE RISK NOTE (The Financials)
            rn = session.exec(select(RiskNote).where(RiskNote.risk_note_number == "RN/001/26")).first()
            if not rn:
                rn = RiskNote(
                    risk_note_number="RN/001/26",
                    policy_id=policy.id,
                    transaction_type="New Business",
                    start_date=date.today(),
                    end_date=date.today() + timedelta(days=365),
                    basic_premium=100000.0,
                    gross_premium=100300.0,
                    commission_amount=12500.0,
                    special_clauses=["Including Political Violence", "Windscreen up to 50k"]
                )
                session.add(rn)
                session.commit()
                
            logger.info("✅ Mock Data Seeded Successfully")
    
    if __name__ == "__main__":
        create_mock_data()
    ```
---

## 🟢 STEP 2: GENERATE THE TYPESCRIPT CLIENT
**Goal:** Let the machine write the API code.
**Action:**
1.  Refer to the generate client script in `./scripts/generate-client.sh`.
2.  Run the generator from the backend directory using `uv`:
    ```bash
    cd backend
    uv run python -c "import app.main; import json; print(json.dumps(app.main.app.openapi()))" > ../openapi.json
    ```
3.  Copy the generated `openapi.json` file to the frontend directory: `mv ../openapi.json ../frontend/openapi.json`.
4.  Run the generator from the frontend directory:
    ```bash
    cd ../frontend
    npm run generate-client
    ```
5.  **Verify:** Check `frontend/src/client`. You MUST see the generated code.

---

## 🟢 STEP 3: CREATE THE "SMART HOOKS"
**Goal:** Wrap the generated client in React Query.
**Constraint:** Do NOT write `axios` or `fetch` calls. Import from `../../client`.

### Task 3.1: `frontend/src/hooks/useInsurance.ts`
**Agent Instruction:** Create a consolidated hook file.
```typescript
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { 
  ClientsService, 
  PoliciesService, 
  RiskNotesService,
  RiskNoteCreate 
} from "../../client"; // The Generated Code

// 1. CLIENTS
export const useClients = () => {
  return useQuery({
    queryKey: ["clients"],
    queryFn: () => ClientsService.readClients({ skip: 0, limit: 100 }),
  });
};

export const useClient = (id: string) => {
  return useQuery({
    queryKey: ["clients", id],
    queryFn: () => ClientsService.readClient({ clientId: id }),
    enabled: !!id,
  });
};

// 2. POLICIES
export const useClientPolicies = (clientId: string) => {
  return useQuery({
    queryKey: ["policies", clientId],
    // Assumption: Backend has a filter or we fetch all and filter client-side for MVP
    queryFn: () => PoliciesService.readPolicies({ skip: 0, limit: 100 }), 
    select: (data) => data.filter(p => p.client_id === clientId)
  });
};

// 3. RISK NOTES (The Money)
export const useCreateRiskNote = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (data: RiskNoteCreate) => RiskNotesService.createRiskNote({ requestBody: data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["risk-notes"] });
      queryClient.invalidateQueries({ queryKey: ["policies"] });
    },
  });
};
```

## 🟢 STEP 4: BUILD THE VIEWS (The "Happy Path")

### Task 4.1: The Client Hub (routes/_layout/clients.$clientId.tsx)
**Layout**:
- Header: Client Name (from useClient).
- Body: A <Tabs> component (Shadcn).
- Tab "Policies":
  * Render a Table of policies using useClientPolicies.
  * Add a button: "Add Risk Note".
  * Interaction: Clicking "Add Risk Note" opens the RiskNoteForm (Task 4.2).

### Task 4.2: The Calculator Component (components/insurance/RiskNoteForm.tsx)
**Logic**:
- Input: Sum Insured.
- Effect: useEffect calculates Gross Premium = Sum * 0.04 + Levies.
- Submit: Calls useCreateRiskNote with the calculated values.

### Task 4.3: The Print View (routes/print/risk-notes.$id.tsx)
**Style**:
- Plain White Background.
- CSS: @media print { .sidebar { display: none } }.
- Content: A grid layout mimicking the "Risk Note - sample.docx".
