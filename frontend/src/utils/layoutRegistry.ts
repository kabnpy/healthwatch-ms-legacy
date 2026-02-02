export type LayoutType = "table-row" | "list-item" | "grid-row"

export interface SectionConfig {
  layout: LayoutType
  showLabelInList?: boolean
}

/**
 * Determines the layout for a given section.
 * This keeps presentation logic in the frontend.
 */
export const getSectionLayout = (
  sectionName: string,
  fieldsCount: number,
): SectionConfig => {
  const normalizedName = sectionName.toUpperCase()

  // 1. Grid Row Sections (Horizontal)
  if (
    normalizedName.includes("VEHICLE DETAILS") ||
    normalizedName.includes("LOCATION")
  ) {
    return { layout: "grid-row" }
  }

  // 2. List Item Sections (Vertical List)
  if (
    normalizedName.includes("BENEFITS") ||
    normalizedName.includes("CLAUSES") ||
    normalizedName.includes("EXCESS") ||
    normalizedName.includes("EXCLUDED") ||
    normalizedName.includes("INTEREST")
  ) {
    // If it's a clause or excluded risk, we often don't want the "Included: " label
    const isClauseOrExclusion =
      normalizedName.includes("CLAUSES") || normalizedName.includes("EXCLUDED")

    return {
      layout: "list-item",
      showLabelInList: !isClauseOrExclusion,
    }
  }

  // 3. Fallback: If a section has many items, default to list for readability
  if (fieldsCount > 5) {
    return { layout: "list-item" }
  }

  // 4. Default: Standard Table Row
  return { layout: "table-row" }
}
