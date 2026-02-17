/**
 * Utilities for handling the "Document-as-Data" blueprint format.
 */

export interface WizardField {
  path: string[] // Path to the value in the JSON object
  label: string
  type: string // text, number, date, boolean
}

/**
 * Recursively crawls a blueprint JSON to find <<placeholders>>.
 * Returns a flat list of fields for the minimal wizard.
 */
export function extractWizardFields(
  obj: any,
  path: string[] = [],
): WizardField[] {
  const fields: WizardField[] = []

  if (typeof obj !== "object" || obj === null) {
    if (typeof obj === "string" && obj.startsWith("<<") && obj.endsWith(">>")) {
      const type = obj.slice(2, -2)
      // The label is the last segment of the path
      const label = path[path.length - 1] || "Field"
      fields.push({ path, label, type })
    }
    return fields
  }

  if (Array.isArray(obj)) {
    // We typically don't expect placeholders inside lists in the blueprint,
    // but we could support it if needed. For now, skip.
    return fields
  }

  for (const [key, value] of Object.entries(obj)) {
    fields.push(...extractWizardFields(value, [...path, key]))
  }

  return fields
}

/**
 * Deeply merges user inputs from the wizard into the blueprint to create the final document data.
 */
export function injectWizardData(
  blueprint: any,
  inputs: any,
  fullPath: string[] = [],
): any {
  if (typeof blueprint !== "object" || blueprint === null) {
    return blueprint
  }

  if (Array.isArray(blueprint)) {
    return blueprint.map((item) => injectWizardData(item, inputs, fullPath))
  }

  const result: any = {}
  for (const [key, value] of Object.entries(blueprint)) {
    const currentPath = [...fullPath, key]
    const dotPath = currentPath.join(".")

    if (
      typeof value === "string" &&
      value.startsWith("<<") &&
      value.endsWith(">>")
    ) {
      // 1. Try to find the value by dot-notated full path (flat inputs)
      if (inputs && inputs[dotPath] !== undefined) {
        result[key] = inputs[dotPath]
      }
      // 2. Try to find it by nested key (if inputs were partially navigated)
      else if (
        inputs &&
        inputs[key] !== undefined &&
        typeof inputs[key] !== "object"
      ) {
        result[key] = inputs[key]
      } else {
        result[key] = "[ EMPTY ]"
      }
    } else if (typeof value === "object" && value !== null) {
      // Recurse, passing the same root inputs but extending the path
      // Also pass the sub-object if it exists for traditional nesting
      const nextInputs =
        inputs?.[key] && typeof inputs[key] === "object" ? inputs[key] : inputs

      result[key] = injectWizardData(value, nextInputs, currentPath)
    } else {
      result[key] = value
    }
  }
  return result
}
