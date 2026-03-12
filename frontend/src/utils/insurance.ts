import type { PolicyPublic } from "@/client"

/**
 * Derives a display name for a policy based on its product and latest snapshot.
 */
export function getPolicyDisplayName(policy: PolicyPublic): string {
  if (!policy.product) {
    return policy.policy_number
  }

  const baseName = policy.product.class_of_insurance || policy.product.name
  const snapshot = (policy.active_note?.cover_snapshot as any) || {}

  // Look for common identification keys in the snapshot
  function findIdValue(obj: any): string | null {
    if (!obj || typeof obj !== "object") return null

    const priorityKeys = [
      "registration_number",
      "reg_no",
      "serial_number",
      "id_number",
      "name",
    ]
    for (const k of priorityKeys) {
      if (obj[k] && typeof obj[k] === "string") return obj[k]
    }

    for (const v of Object.values(obj)) {
      const res = findIdValue(v)
      if (res) return res
    }
    return null
  }

  const idVal = findIdValue(snapshot)
  if (idVal) {
    return `${baseName} - ${idVal}`
  }

  return baseName
}

/**
 * Fetches a file with authentication headers and triggers a browser download.
 */
export async function downloadAuthenticatedFile(
  url: string,
  filename: string,
): Promise<void> {
  const token = localStorage.getItem("access_token")
  try {
    const response = await fetch(url, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })

    if (!response.ok) {
      throw new Error(`Failed to download file: ${response.statusText}`)
    }

    const blob = await response.blob()
    const objectUrl = URL.createObjectURL(blob)

    const link = document.createElement("a")
    link.href = objectUrl
    link.download = filename
    document.body.appendChild(link)
    link.click()

    // Cleanup
    document.body.removeChild(link)
    URL.revokeObjectURL(objectUrl)
  } catch (error) {
    console.error("Error downloading file:", error)
    throw error
  }
}
