export interface WizardState {
  // Step 1: The Asset
  asset: {
    identifier: string;       // "KCA 123B"
    makeModel: string;        // "Toyota Harrier"
    details: Record<string, any>; // { chassis: "...", engine: "..." }
  };

  // Step 2: The Money & Coverage
  financials: {
    sumInsured: number;       // The base for all math
    rate: number;             // e.g. 4.5%
    startDate: string;        // ISO Date string
    duration: number;         // Months (usually 12)
  };

  // Step 2b: The Toggles (Extensions)
  extensions: {
    pvt: boolean;             // Political Violence
    excessProtector: boolean;
    passengerLiability: boolean;
  };

  // Step 2c: The Promises (Custom Benefits)
  benefitOverrides: {
    towingLimit?: number;
    windscreenLimit?: number;
    radioLimit?: number;
  };
}

export type WizardMode = "NEW" | "RENEWAL" | "ENDORSEMENT";
