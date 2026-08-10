import random
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog
from playwright.sync_api import sync_playwright

URL = "https://erp.code-graphers.co/"
EMAIL = ""
PASSWORD = r""  #place your password in the r""


def set_timesheet_times(page):
    today_str = datetime.now().strftime("%d-%m-%Y")

    from_time = (
        f"{today_str} 12:{random.randint(0, 20):02d}:{random.randint(0, 59):02d}"
    )
    to_time = (
        f"{today_str} 21:{random.randint(10, 45):02d}:{random.randint(0, 59):02d}"
    )

    page.click('input[data-fieldname="from_time"]')
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.keyboard.type(from_time, delay=30)
    page.keyboard.press("Tab")

    page.click('input[data-fieldname="to_time"]')
    page.keyboard.press("Control+A")
    page.keyboard.press("Backspace")
    page.keyboard.type(to_time, delay=30)
    page.keyboard.press("Tab")

    page.evaluate("document.activeElement.blur()")

def get_description_via_popup():
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    description = simpledialog.askstring(
        title="Timesheet Entry", prompt="Enter timesheet description:"
    )

    root.destroy()
    return description or ""



def run_automation():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,  slow_mo=500)
        context = browser.new_context()
        page = context.new_page()

        print(f"Navigating to {URL}...")
        page.goto(URL, wait_until="networkidle")

        print("Filling in login credentials...")
        page.fill("#login_email", EMAIL)
        page.fill("#login_password", PASSWORD)

        print("Clicking Continue...")
        page.click(".btn-login")

        page.wait_for_load_state("networkidle")

        print("Login attempt completed.")

        page.click('a[data-id="Projects"]')

        page.click('a[href="/desk/timesheet"]')

        page.click('button[data-label="Add Timesheet"]')

        page.click(".btn-open-row")

        page.fill('input[data-fieldname="activity_type"]', "Development")
        page.click('div[role="option"] p[title="Development"]')

        page.fill('input[data-fieldname="expected_hours"]', "8")

        set_timesheet_times(page)

        description_text = get_description_via_popup()

        page.fill(
            'textarea[data-fieldname="description"], input[data-fieldname="description"]',
            description_text,
        )

        page.click('input[data-fieldname="project"]')
        page.locator(
            'ul[role="listbox"]:not([hidden]) div[role="option"]'
        ).first.click()

        page.wait_for_timeout(300)

        page.click('input[data-fieldname="task"]')
        page.locator(
            'ul[role="listbox"]:not([hidden]) div[role="option"]'
        ).first.click()

        page.keyboard.press("Escape")

        page.click('button[data-label="Save"]')

        page.click('button[data-label="Submit"]')

        # page.click("button.btn-modal-primary:has-text('Yes')")

        print("submitted and done successfully")

        page.wait_for_timeout(300000)
        browser.close()


if __name__ == "__main__":
    run_automation()