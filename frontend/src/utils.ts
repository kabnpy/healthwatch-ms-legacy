import { AxiosError } from "axios"
import type { ApiError } from "./client"

function extractErrorMessage(err: ApiError): string {
  if (err instanceof AxiosError) {
    return err.message
  }

  const errDetail = (err.body as any)?.detail
  if (Array.isArray(errDetail) && errDetail.length > 0) {
    return errDetail[0].msg
  }
  return errDetail || "Something went wrong."
}

export const handleError = function (
  this: (msg: string) => void,
  err: ApiError,
) {
  const errorMessage = extractErrorMessage(err)
  this(errorMessage)
}

export const getInitials = (name: string): string => {
  return name
    .split(" ")
    .slice(0, 2)
    .map((word) => word[0])
    .join("")
    .toUpperCase()
}

export const slugify = (text: string): string => {
  return text
    .toString()
    .toLowerCase()
    .trim()
    .replace(/\s+/g, "_") // Replace spaces with _
    .replace(/[^\w-]+/g, "") // Remove all non-word chars
    .replace(/--+/g, "-") // Replace multiple - with single -
    .replace(/^-+/, "") // Trim - from start of text
    .replace(/-+$/, "") // Trim - from end of text
}

export const getPolicyDisplayName = (riskNote: any): string => {
  const policySnapshot = riskNote?.policy_snapshot || {}
  const riskDetails = policySnapshot?.risk_details || {}
  
  // Try to find Product/Class Name
  const className = 
    policySnapshot?.product?.class_of_insurance || 
    riskNote?.policy?.product?.class_of_insurance || 
    "Insurance Policy"

  if (className.toLowerCase().includes("motor private")) {
    // Look for registration number in VEHICLE DETAILS
    const vehicleDetails = riskDetails["VEHICLE DETAILS"] || {}
    const regNo = vehicleDetails["reg_no"] || vehicleDetails["Reg No"] || ""
    
    if (regNo) {
      return `${className} - ${regNo}`
    }
  }

  // Fallback to description if available
  const description = policySnapshot?.description || riskNote?.policy?.description
  if (description) {
    return `${className} - ${description}`
  }

  return className
}
