export interface CalculationInput {
  sumInsured: number
  rate: number
  hasPVT: boolean
  hasExcessProtector: boolean
  hasPassengerLiability?: boolean
}

export interface CalculationResult {
  breakdown: {
    basic: number
    extensions: Array<{ name: string; amount: number }>
    levies: {
      trainingLevy: number
      phcf: number
      stampDuty: number
    }
    total: number
  }
}

export function calculatePremium(input: CalculationInput): CalculationResult {
  const basic = input.sumInsured * (input.rate / 100)

  // Extensions
  const extensions: Array<{ name: string; amount: number }> = []
  if (input.hasPVT) {
    extensions.push({ name: "PVT", amount: basic * 0.0025 })
  }
  if (input.hasExcessProtector) {
    extensions.push({ name: "Excess Protector", amount: basic * 0.0025 })
  }
  if (input.hasPassengerLiability) {
    // Standard flat fee for passenger liability in this context or percentage
    // Let's use 500 KES as a flat fee for MVP
    extensions.push({ name: "Passenger Liability", amount: 500 })
  }

  const extensionsTotal = extensions.reduce((acc, curr) => acc + curr.amount, 0)

  // Levies (Standard Kenyan Insurance Taxes)
  const trainingLevy = basic * 0.002 // 0.2%
  const phcf = basic * 0.0025 // 0.25%
  const stampDuty = 40 // Fixed

  const total = basic + extensionsTotal + trainingLevy + phcf + stampDuty

  return {
    breakdown: {
      basic,
      extensions,
      levies: { trainingLevy, phcf, stampDuty },
      total,
    },
  }
}
