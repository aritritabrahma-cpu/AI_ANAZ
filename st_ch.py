from playwright.sync_api import sync_playwright
import os

SAVE_PATH = r"C:\Users\Admin\OneDrive\Desktop\AI_ANAZ\my_project\auth.json"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    context = browser.new_context()
    page = context.new_page()

    page.goto("https://staging.guardrail.in")

    input("✅ Login to Guardrail completely, then press ENTER here...")

    print("Saving storage state...")

    context.storage_state(path=SAVE_PATH)

    print("Saved!")
    print("Exists:", os.path.exists(SAVE_PATH))

    browser.close()