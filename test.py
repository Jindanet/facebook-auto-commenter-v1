from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import os, time, json
import pyautogui
profile = 'C:\\Users\\ Your User \\AppData\\Local\\Google\\Chrome\\User Data\\Profile 29'
options = uc.ChromeOptions()
options.add_argument(f"--user-data-dir={profile}")
options.add_argument('--auto-open-devtools-for-tabs')
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--no-first-run")
options.add_argument("--no-default-browser-check")
options.add_argument("--disable-extensions")

driver = uc.Chrome(
    version_main=109,
    driver_executable_path="C:/ Your chromedriver path /chromedriver.exe",
    options=options
)
driver.maximize_window()
wait = WebDriverWait(driver, 10)

driver.get("https://m.facebook.com/groups/testgroup/permalink/0000000000000")
time.sleep(2)
driver.refresh()
try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x}, Y: {y}")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nDone.")
time.sleep(9999)
