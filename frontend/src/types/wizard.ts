export interface WizardState {
  product_id: string // The selected product (e.g. Motor Private)

  // Step 1: The Asset
  asset: {
    identifier: string // "KCA 123B" or "Plot No 4"
    description: string // "Toyota Harrier" or "Residential House"
    details: Record<string, any> // { chassis: "...", engine: "..." }
  }

  // Step 2: The Money & Coverage
  financials: {
    sum_insured: number // The base for all math
    rate: number // e.g. 4.5%
    startDate: string // ISO Date string
    duration: number // Months (usually 12)
  }

  // Step 2b: The Toggles (Extensions)
  extensions: {
    pvt: boolean // Political Violence
    excessProtector: boolean
    passengerLiability: boolean
  }

  // Step 2c: The Promises (Custom Benefits)
  benefitOverrides: {
    towingLimit?: number
    windscreenLimit?: number
    radioLimit?: number
  }
}

export type WizardMode = "NEW" | "RENEWAL" | "ENDORSEMENT"
