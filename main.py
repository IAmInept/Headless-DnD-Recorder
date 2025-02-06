import os
import time
import subprocess
from pyvirtualdisplay import Display
from playwright.sync_api import Page, expect, sync_playwright



if __name__ == "__main__":
# start xvfb
    with Display(visible=False, size=(1920, 1080), color_depth=24) as disp:
        if disp.is_alive():
            print(f"Display has started on {os.environ.get("DISPLAY")}")
            try:
                ffmpeg = subprocess.Popen(["ffmpeg", "-probesize", "30M", "-f", "x11grab", "-framerate",  "60", "-i", f"{os.environ.get("DISPLAY")}", "-c:v", "ffv1", "-g", "1", f"{time.ctime()}.mkv"])
            except:
                raise Exception()
        else:
            print("Error!")
    

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            page.set_viewport_size({"width": 1920, "height": 1080})
            page.goto("https://foundry.gianwallace.com/")
            page.select_option("select[name='userid']", value="cmD8QxeWRQLEkt86")
            page.get_by_role("button", name="Join").click()
            page.wait_for_url("https://foundry.gianwallace.com/game")
            # browser.close()
            # ffmpeg.terminate()
            # ffmpeg.wait()
            # print("Recording Stopped")