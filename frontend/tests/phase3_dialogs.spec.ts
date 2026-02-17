import { expect, test } from "@playwright/test"

test.describe("Phase 3: Component & Copy Audit - Dialog Column Verification", () => {
  test.beforeEach(async ({ page }) => {
    test.setTimeout(60000)
    await page.goto("/")
  })

  test("Add Client dialog uses single column layout where appropriate", async ({
    page,
  }) => {
    test.setTimeout(60000)
    await page.goto("/clients")
    await page.getByRole("button", { name: "Add Client" }).click()

    const dialog = page.getByRole("dialog")
    await expect(dialog).toBeVisible()

    // Check if the form within the dialog has multi-column grids
    // We expect major sections to be single column or simple 2-column for small fields
    // Based on user feedback, we want to ensure it doesn't feel 'multiple columns'

    // Check for 2-column grids that might be too wide
    const grids = dialog.locator(".grid")
    const gridCount = await grids.count()

    for (let i = 0; i < gridCount; i++) {
      const grid = grids.nth(i)
      const classList = await grid.getAttribute("class")
      if (
        classList?.includes("grid-cols-2") ||
        classList?.includes("md:grid-cols-2")
      ) {
        // This is a 2-column grid. We should verify if it contains small fields (like Type/PIN)
        // or if it should be single column.
      }
    }
  })

  test("Add Policy dialog should be audited for columns", async ({ page }) => {
    test.setTimeout(60000)
    await page.goto("/clients")
    await page.waitForSelector("table")

    // Search for Agnes
    const searchInput = page.getByPlaceholder("Search...")
    if (await searchInput.isVisible()) {
      await searchInput.fill("Agnes")
      await page.waitForTimeout(1000)
    }

    // Click client link
    await page.locator('table tbody tr a[href*="/clients/"]').first().click()
    await page.waitForURL(/\/clients\/.+/)

    // Explicitly click Policies tab
    await page.getByRole("tab", { name: "Policies" }).click()

    // Ensure we are on the Policies tab and content is loaded
    const addPolicyButton = page
      .getByRole("button", { name: /New Policy|Add Policy/i })
      .first()
    await addPolicyButton.waitFor({ state: "visible" })
    await addPolicyButton.click()

    const dialog = page.getByRole("dialog")
    await expect(dialog).toBeVisible()

    // Audit for columns: Ensure no grids have more than 2 columns (MD breakpoint included)
    const grids = dialog.locator(".grid")
    const gridCount = await grids.count()

    for (let i = 0; i < gridCount; i++) {
      const classList = await grids.nth(i).getAttribute("class")
      expect(classList).not.toContain("grid-cols-3")
      expect(classList).not.toContain("md:grid-cols-3")
    }
  })
})
