# Medallion: Bronze | Mutation: 0% | HIVE: V
import asyncio
from playwright.async_api import async_playwright
import os

async def run_audit():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await p.new_page()
        
        # URL for the demo
        url = "http://localhost:8888/hfo_hot_obsidian/bronze/2_areas/mission_thread_omega/piano_genie_official/index.html"
        print(f"Navigating to {url}")
        
        # Listen for console messages
        page.on("console", lambda msg: print(f"BROWSER_LOG: {msg.text}"))
        
        try:
            await page.goto(url, timeout=60000)
            
            # Wait for "Play" button to become enabled (means genie.initialize finished)
            print("Waiting for Genie initialization...")
            play_btn = page.locator("#playBtn")
            await play_btn.wait_for(state="visible", timeout=30000)
            
            # Wait for button to NOT be loading
            await page.wait_for_function('!document.getElementById("playBtn").classList.contains("loading")', timeout=30000)
            print("Genie initialized!")
            
            # Take a snapshot of the splash screen
            await page.screenshot(path="genie_v53_splash.png")
            print("Splash screenshot saved.")
            
            # Click Play
            await play_btn.click()
            print("Clicked Play.")
            
            # Wait for the loaded screen
            await page.locator(".loaded").wait_for(state="visible", timeout=5000)
            
            # Wait a bit for the canvas to draw
            await asyncio.sleep(2)
            
            # Take a snapshot of the main screen (should show keys and piano)
            await page.screenshot(path="reports/FORENSIC_GENIE_V53_AUDIT.png")
            print("Main screen screenshot saved to reports/FORENSIC_GENIE_V53_AUDIT.png")
            
        except Exception as e:
            print(f"Audit failed: {e}")
            # Try to take error screenshot
            await page.screenshot(path="reports/ERROR_GENIE_V53_AUDIT.png")
            
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_audit())
