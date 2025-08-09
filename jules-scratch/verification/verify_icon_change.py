from playwright.sync_api import sync_playwright, Page, expect
import os

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    # Listen for console messages
    page.on("console", lambda msg: print(f"CONSOLE: [{msg.type}] {msg.text}"))

    # Get the absolute path to the admin.html file
    page.goto('http://localhost:8000/admin.html')

    # 1. Login
    page.get_by_placeholder("Password").fill("thinkplusbd_admin_2024")
    page.get_by_role("button", name="Login").click()

    # Wait for the dashboard to load by checking for the "Order Management" heading
    expect(page.get_by_role("heading", name="Order Management")).to_be_visible()

    # Wait for the categories to load
    expect(page.locator('#categories-tbody tr').first).to_be_visible()

    # 2. Get the initial icon of the first category
    first_row = page.locator('#categories-tbody tr').first
    initial_icon_element = first_row.locator('td[data-field="icon"] i')
    initial_icon_class = initial_icon_element.get_attribute('class')

    # 3. Click "Change Icon" on the first category
    change_icon_button = first_row.get_by_role("button", name="Change Icon")
    change_icon_button.click()

    # 4. Verify the icon has changed
    expect(initial_icon_element).not_to_have_class(initial_icon_class)

    # 5. Verify the button text is now "Save Icon"
    save_icon_button = first_row.get_by_role("button", name="Save Icon")
    expect(save_icon_button).to_be_visible()

    # 6. Take a screenshot after changing the icon
    page.screenshot(path="jules-scratch/verification/01_icon_changed.png")

    # 7. Get the new icon class
    new_icon_class = initial_icon_element.get_attribute('class')

    # 8. Click "Save Icon"
    # We need to handle the alert that pops up after saving
    page.on("dialog", lambda dialog: dialog.accept())
    save_icon_button.click()

    # 9. Wait for the table to re-render and verify the new icon is saved
    # We expect the icon element to have the new class after the table reloads
    expect(initial_icon_element).to_have_class(new_icon_class)

    # 10. Verify the button is back to "Change Icon"
    expect(first_row.get_by_role("button", name="Change Icon")).to_be_visible()

    # 11. Take a final screenshot
    page.screenshot(path="jules-scratch/verification/02_icon_saved.png")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)
