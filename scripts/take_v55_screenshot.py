from playwright.sync_api import sync_playwright
import os
import time

def take_screenshot():
    with sync_playwright() as p:
        # We specify no executable_path to use the installed chromium
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Local server URL
        url = "http://localhost:8892/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/omega_workspace_v55.html"
        
        print(f"Navigating to {url}")
        page.on("console", lambda msg: print(f"BROWSER CONSOLE: {msg.text}"))
        page.goto(url)
        
        # Wait for some time for Golden Layout to settle
        print("Waiting for Golden Layout...")
        time.sleep(10)
        
        screenshot_path = "reports/v55_transparency_test.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot saved to {screenshot_path}")
        
        # Debugging: Print IDs of elements found
        elements = page.query_selector_all("*")
        ids = [el.get_attribute("id") for el in elements if el.get_attribute("id")]
        print(f"Found IDs: {ids}")
        
        browser.close()

if __name__ == "__main__":
    take_screenshot()
