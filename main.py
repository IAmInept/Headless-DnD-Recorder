import time
import subprocess
import asyncio
from pyvirtualdisplay import Display
from playwright.sync_api import Page, expect, sync_playwright
from playwright.async_api import async_playwright


class HeadlessServer:
    def __init__(self):
        self.display: Display = None
        self.ffmpeg = None
        self.browser = None
        self.shutdown = asyncio.Event()

    async def startRecording(self):
        self.display = Display(visible=False, size=(1920, 1080), color_depth=24)
        self.display.start() 
        if self.display.is_alive():
            print(f"Display has started on {self.display.new_display_var}")
            try:
                ffmpeg = subprocess.Popen(["ffmpeg", "-probesize", "30M", "-f", "x11grab", "-framerate",  "60", "-i", 
                                           f"{self.display.new_display_var}", "-c:v", "hevc", f"./output/{time.strftime('%Y-%m-%d_%H-%M-%S')}.mkv"])
                self.ffmpeg = ffmpeg
            except Exception as e:
                print(f"ffmpeg failed to start {e}")
                return
        
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                self.browser = browser
                page = await browser.new_page()
                await page.set_viewport_size({"width": 1920, "height": 1080})
                await page.goto("https://foundry.gianwallace.com/")
                await page.select_option("select[name='userid']", value="cmD8QxeWRQLEkt86")
                await page.get_by_role("button", name="Join").click()
                await page.wait_for_url("https://foundry.gianwallace.com/game")
                await page.wait_for_load_state()
                await page.get_by_label("Close Window").click()
                await self.shutdown.wait()
    
    async def stopRecording(self):
        self.shutdown.set()
        self.ffmpeg.terminate()
        await asyncio.to_thread(self.ffmpeg.wait)
        await self.browser.close()
        self.display.stop()
