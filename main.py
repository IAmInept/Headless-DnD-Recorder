import time
import requests
from dotenv import load_dotenv
import subprocess
import asyncio
from pyvirtualdisplay import Display
from playwright.async_api import async_playwright
from nextcloud import NextCloud

class HeadlessServer:
    def __init__(self):
        ## nextcloud login
        self.NEXTCLOUD_URL = "http://{}:80".format(load_dotenv('NEXTCLOUD_HOSTNAME'))
        self.NEXTCLOUD_USERNAME = load_dotenv('NEXTCLOUD_ADMIN_USER')
        self.NEXTCLOUD_PASSWORD = load_dotenv('NEXTCLOUD_ADMIN_PASSWORD')
        self.nextcloud = NextCloud(self.NEXTCLOUD_URL, self.NEXTCLOUD_USERNAME, self.NEXTCLOUD_PASSWORD, json_output=True)
        self.display: Display = None
        self.ffmpeg = None
        self.browser = None
        self.shutdown = asyncio.Event()
        self.apiassert = True

    def initBuffer(self):
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
        

    async def initBrowser(self):
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
            await self.shutdown.wait()

    async def stopRecording(self):
        self.shutdown.set()
        self.ffmpeg.terminate()
        await asyncio.to_thread(self.ffmpeg.wait)
        await self.browser.close()
        self.display.stop()
        self.nextcloud

    def isRecording(self):
        if (self.apiassert):
            return self.apiassert
        else:
            return False
