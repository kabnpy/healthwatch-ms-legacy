export interface CalculationInput {
  sumInsured: number
  rate: number
  hasPVT: boolean
  hasExcessProtector: boolean
  hasPassengerLiability?: boolean
  hasOMRescuePlus?: boolean
  isMotorPrivate?: boolean
}

export interface CalculationResult {
  breakdown: {
    basic: number
    extensions: Array<{ name: string; amount: number; included?: boolean }>
    levies: {
      trainingLevy: number
      phcf: number
      stampDuty: number
    }
    total: number
  }
}

/**
 * Local fallback calculation logic for real-time UI previews.
 * MUST be kept in sync with backend/app/services/rating.py
 */
export function calculatePremium(input: CalculationInput): CalculationResult {
  const value = input.sumInsured || 0
  let basic = 0
  
  // 1. Basic Premium (Motor Private: 3.25%, min 15,000)
  if (input.isMotorPrivate) {
    basic = Math.max(15000, value * 0.0325)
  } else {
    basic = value * (input.rate / 100)
  }

  // 2. Pre-Levy Extensions (Benefits)
  const extensions: Array<{
    name: string
    amount: number
    included?: boolean
  }> = []

  let netPremium = basic

  if (input.hasPVT) {
    const amt = value * 0.0025
    extensions.push({
      name: "PVT",
      amount: amt,
    })
    netPremium += amt
  }

  if (input.hasExcessProtector) {
    const amt = value * 0.0025
    extensions.push({ 
      name: "Excess Protector", 
      amount: amt 
    })
    netPremium += amt
  }

  // 3. Levies (calculated on Net Premium)
  const trainingLevy = netPremium * 0.002 // 0.2%
  const phcf = netPremium * 0.0025 // 0.25%
  const stampDuty = 40 // Fixed
  const totalLevies = trainingLevy + phcf + stampDuty

  // 4. Post-Levy Benefits (e.g., OM Rescue Plus)
  let postLevyTotal = 0
  if (input.hasOMRescuePlus) {
    const amt = 1000
    extensions.push({ name: "OM Rescue Plus", amount: amt })
    postLevyTotal += amt
  }

  const total = netPremium + totalLevies + postLevyTotal

  return {
    breakdown: {
      basic,
      extensions,
      levies: { trainingLevy, phcf, stampDuty },
      total,
    },
  }
}
