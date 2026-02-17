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

const MOTOR_PRIVATE_TIERS = [
  { max: 1500000, rate: 5.0, min: 60000 },
  { max: 2500000, rate: 4.0, min: 75000 },
  { max: 3000000, rate: 3.5, min: 100000 },
  { max: 5000000, rate: 3.25, min: 0 },
  { max: Infinity, rate: 3.0, min: 0 },
]

export function calculatePremium(input: CalculationInput): CalculationResult {
  let basic = 0
  let rate = input.rate

  if (input.isMotorPrivate) {
    const tier =
      MOTOR_PRIVATE_TIERS.find((t) => input.sumInsured < t.max) ||
      MOTOR_PRIVATE_TIERS[MOTOR_PRIVATE_TIERS.length - 1]
    rate = tier.rate
    basic = Math.max(input.sumInsured * (rate / 100), tier.min)
  } else {
    basic = input.sumInsured * (rate / 100)
  }

  // Extensions (Benefits)
  const extensions: Array<{
    name: string
    amount: number
    included?: boolean
  }> = []

  // High-End Logic: Sum Insured >= 3M (All Inclusive)
  const isHighEnd = input.isMotorPrivate && input.sumInsured >= 3000000

  if (input.hasPVT) {
    if (isHighEnd) {
      extensions.push({
        name: "Political Violence & Terrorism",
        amount: 0,
        included: true,
      })
    } else {
      extensions.push({
        name: "Political Violence & Terrorism",
        amount: input.sumInsured * 0.0025,
      })
    }
  }

  if (input.hasExcessProtector) {
    if (isHighEnd) {
      extensions.push({ name: "Excess Protector", amount: 0, included: true })
    } else {
      extensions.push({
        name: "Excess Protector",
        amount: input.sumInsured * 0.0025,
      })
    }
  }

  if (input.hasPassengerLiability) {
    extensions.push({ name: "Passenger Liability", amount: 500 })
  }

  if (input.hasOMRescuePlus) {
    extensions.push({ name: "OM Rescue Plus", amount: 1000 })
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
