import { expect, test } from "@playwright/test"

test.describe("Phase 2: Professional Document Redesign", () => {
  test.beforeEach(async ({ page }) => {
    test.setTimeout(60000)
    await page.goto("/")
  })

  test("Risk Note template has professional elements", async ({ page }) => {
    test.setTimeout(60000)
    await page.goto("/clients")
    await page.waitForSelector("table")

    // Search for Agnes who we know has a policy in mock data
    const searchInput = page.getByPlaceholder("Search...")
    if (await searchInput.isVisible()) {
      await searchInput.fill("Agnes")
      await page.waitForTimeout(1000) // Wait for search to filter
    }

    const clientLink = page
      .locator('table tbody tr a[href*="/clients/"]')
      .first()
    await clientLink.click()
    await page.waitForURL(/\/clients\/.+/)

    // Check if there are any policies
    await page.waitForSelector("table")
    const policyLink = page
      .locator('table tbody tr a[href*="/policies/"]')
      .first()

    if (await policyLink.isVisible()) {
      await policyLink.click()
      await page.waitForURL(/\/policies\/.+/)

      // The Risk Note should be visible in the Overview tab
      await expect(
        page.getByRole("heading", { name: /Risk Note/i }),
      ).toBeVisible()

      // Check for letterhead/branding
      await expect(
        page.getByText("HealthWatch", { exact: false }).first(),
      ).toBeVisible()

      // Check for professional sections using robust locators from the template
      await expect(page.getByText("INSURED", { exact: true })).toBeVisible()
      await expect(page.getByText("CLASS", { exact: true })).toBeVisible()
      await expect(page.getByText("PERIOD", { exact: true })).toBeVisible()
    }
  })

  test("Document viewer opens and displays content", async ({ page }) => {
    test.setTimeout(60000)
    await page.goto("/clients")
    await page.waitForSelector("table")

    // Search for Agnes
    const searchInput = page.getByPlaceholder("Search...")
    if (await searchInput.isVisible()) {
      await searchInput.fill("Agnes")
      await page.waitForTimeout(1000)
    }

    const clientLink = page
      .locator('table tbody tr a[href*="/clients/"]')
      .first()
    await clientLink.click()
    await page.waitForURL(/\/clients\/.+/)

    // Check if there are any policies
    await page.waitForSelector("table")
    const policyLink = page
      .locator('table tbody tr a[href*="/policies/"]')
      .first()

    if (await policyLink.isVisible()) {
      await policyLink.click()
      await page.waitForURL(/\/policies\/.+/)

      // Go to History tab
      const historyTab = page.getByRole("tab", { name: "History" })
      await historyTab.click()

      // Wait for the history table to be loaded
      await page.waitForSelector("table")

      // Find and click the "View" button in the table
      const viewButton = page.getByRole("button", { name: "View" }).first()
      await viewButton.waitFor({ state: "visible" })
      await viewButton.click()

      // Check if modal opens
      const modal = page.getByRole("dialog")
      await expect(modal).toBeVisible()

      // Check if document title is rendered inside modal
      const modalTitle = modal.locator("h1")
      await expect(
        modalTitle.filter({ hasText: /Risk Note|Debit Note/i }).first(),
      ).toBeVisible()
    }
  })
})
