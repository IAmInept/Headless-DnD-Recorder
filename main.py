import os
import time
import subprocess
import threading
from pyvirtualdisplay import Display
from playwright.sync_api import Page, expect, sync_playwright

class HeadlessServer:
    def __init__(self):
        self.display: Display = None
        self.ffmpeg = None
        self.browser = None
        self.threading = None

    def startRecording(self):
        def record():
            with Display(visible=False, size=(1920, 1080), color_depth=24) as disp:
                self.display = disp
                if disp.is_alive():
                    print(f"Display has started on {disp.new_display_var}")
                    try:
                        ffmpeg = subprocess.Popen(["ffmpeg", "-probesize", "30M", "-f", "x11grab", "-framerate",  "60", "-i", f"{disp.new_display_var}", "-c:v", "ffv1", "-g", "1", f"./output/{time.strftime('%Y-%m-%d_%H-%M-%S')}.mkv"])
                        self.ffmpeg = ffmpeg
                    except Exception as e:
                        print(f"ffmpeg failed to start {e}")
            

                with sync_playwright() as p:
                    browser = p.chromium.launch(headless=False)
                    self.browser = browser
                    page = browser.new_page()
                    page.set_viewport_size({"width": 1920, "height": 1080})
                    page.goto("https://foundry.gianwallace.com/")
                    page.select_option("select[name='userid']", value="cmD8QxeWRQLEkt86")
                    page.get_by_role("button", name="Join").click()
                    page.wait_for_url("https://foundry.gianwallace.com/game")

                    while True:
                        time.sleep(1)



        self.threading = threading.Thread(target=record, daemon=True)
        self.threading.start()

    def StopRecording(self):
        self.ffmpeg
