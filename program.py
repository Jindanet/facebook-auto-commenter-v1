from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import os
import time
import pyautogui
import random
from datetime import datetime, timedelta
import schedule
import requests
import logging
import pyperclip
import sys

pyautogui.FAILSAFE = False

# Set up logging
logging.basicConfig(level=logging.INFO, filename='facebook_posting.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global counter for posted links
posted_links_count = 0
total_posts = 0

# Function to perform the posting
def post_to_facebook(url):
    global posted_links_count, total_posts
    logging.info(f"Starting to post to Facebook for URL: {url}")
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
    try:
        driver.get(url)
        time.sleep(0.5)
        driver.refresh()
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
       
        time.sleep(5)

        # Click to press comment text
        # use test.py to get X and Y
        pyautogui.click(x=561, y=1018)

        time.sleep(5)
        hearts = [
            "❤", "💛", "💚", "💙", "💜",  # สีหัวใจเดิม
            "🔥", "✨", "🚀", "👍", "👏",  # เดิม
            "⭐", "🌟", "💥", "🎉", "✌️",  # เพิ่มดาว, ระเบิด, งานฉลอง, สันติภาพ
            "💪", "👀", "🎯", "⚡", "🌈"   # เพิ่มพลัง, ตา, เป้า, ฟ้าผ่า, รุ้ง
        ]
        msg_post = [
            "message", "message2", "message3"
        ]
        random_heart = random.choice(hearts)
        random_msg_msg = random.choice(msg_post)
        current_comment_time = datetime.now()
        time_comment = current_comment_time.strftime('%H:%M')

        pyperclip.copy(random_msg_msg + " " + time_comment + " " + random_heart)
        pyautogui.hotkey('ctrl', 'v')

        time.sleep(5)
        # Click to post comment
        # use test.py to get X and Y
        pyautogui.click(x=860, y=1020)
        
        posted_links_count += 1
        time.sleep(10)
        logging.info(f"Successfully commented on the post for URL: {url}")
        logging.info(f"Posted links count: {posted_links_count}")

    except Exception as e:
        webhook_url = "https://discord.com/api/webhooks/example/example"
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data = {
            "content": f"Error Post V2 => {url} at {current_time} Exception => {e}"
        }
        
        try:
            response = requests.post(webhook_url, json=data)
            response.raise_for_status()  # Ensure that the request was successful
        except requests.exceptions.RequestException as req_e:
            logging.error(f"An error occurred while sending the error notification to Discord: {req_e}")
        
        logging.error(f"An error occurred while posting to Facebook for URL: {url} - {e}")
    
    finally:
        driver.quit()

    # Send webhook to Discord
    send_discord_webhook(url, posted_links_count)

    # Check if all posts are done and reset the counter (เหมือน V2 เดิม แต่ไม่ส่งผลต่อการ exit)
    if posted_links_count == total_posts:
        logging.info("Complete comment all postlink Resetting posted_links_count.")
        posted_links_count = 0

# Function to send a webhook to Discord
def send_discord_webhook(url, count):
    webhook_url = "https://discord.com/api/webhooks/example/example"
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data = {
        "content": f"POST V2 => {url} ({count}) at {current_time}"
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        logging.info(f"Successfully sent webhook for {url} at {current_time}")
    else:
        logging.error(f"Failed to send webhook for {url} at {current_time}, status code: {response.status_code}")

# Define URLs from file
with open('postlink.txt', 'r') as file:
    lines = file.readlines()

urls = [line.strip() for line in lines]

posting_times = ["01:29", "02:29", "03:29", "04:29"]


total_posts = len(urls)

def start_now():
    for url in urls:
        # โพสต์ทันที
        post_to_facebook(url=url)
        logging.info(f"Posted immediately for URL: {url}")

        # ตั้งเวลาโพสต์ในอนาคตตาม posting_times
        for post_time in posting_times:
            schedule.every().day.at(post_time).do(post_to_facebook, url=url)
            logging.info(f"Scheduled post for URL: {url} at {post_time}")

    end_time = datetime.now() + timedelta(days=1)  # รัน 1 วันแล้วออก
    while datetime.now() < end_time:
        schedule.run_pending()
        time.sleep(1)

    logging.info("Completed one day of posting. Exiting program for restart.")
    schedule.clear()
    sys.exit(1)


def schedule_posts():
    for url in urls:
        for post_time in posting_times:
            schedule.every().day.at(post_time).do(post_to_facebook, url=url)
            logging.info(f"Scheduled post for URL: {url} at {post_time}")

    end_time = datetime.now() + timedelta(days=1)  # รัน 1 วันแล้วออก
    while datetime.now() < end_time:
        schedule.run_pending()
        time.sleep(1)

    logging.info("Completed one day of posting. Exiting program for restart.")
    schedule.clear()
    sys.exit(1)

# Start scheduling posts
print("Starting to schedule posts")
logging.info("Starting to schedule posts")
# start_now()
schedule_posts()
