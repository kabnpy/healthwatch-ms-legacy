import type { 
  PolicyPublic, 
  RiskNotePublic, 
  ProductPublic, 
  ClientPublic,
  InsurerPublic 
} from "@/client"
import React from "react"

/**
 * Enhanced versions of the auto-generated types with better metadata and relationships
 */

export interface EnhancedProduct extends ProductPublic {
  insurer?: InsurerPublic
}

export interface EnhancedPolicy extends PolicyPublic {
  product?: EnhancedProduct
  client?: ClientPublic
}

export interface EnhancedRiskNote extends RiskNotePublic {
  policy?: EnhancedPolicy
}

/**
 * Types for the Document Rendering Engine
 */

export type RiskNoteContentValue = 
  | string 
  | number 
  | boolean 
  | null 
  | undefined
  | React.ReactNode
  | RiskNoteContentValue[]
  | { [key: string]: RiskNoteContentValue }

export interface RiskNoteSection {
  name: string
  content: RiskNoteContentValue
}

/**
 * Wizard State Types
 */

export interface WizardFinancials {
  sumInsured: number
  rate: number
  startDate: string
  duration: number
}

export interface WizardExtensions {
  pvt: boolean
  excessProtector: boolean
  passengerLiability: boolean
  omRescuePlus: boolean
}

export interface WizardState {
  product_id: string
  details: Record<string, any>
  financials: WizardFinancials
  extensions: WizardExtensions
}
