import requests
from bs4 import BeautifulSoup
import os
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service


# set up Selenium options to run headless
options = Options()
options.add_argument('--headless')
service = Service('C:/Users/sidds/Downloads/msedgedriver.exe')
driver = webdriver.Edge(service=service, options=options)
url = input('url?: ')
response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')

save_dir = 'pics'

if not os.path.exists(save_dir):
    os.makedirs(save_dir)

for img in img_tags:
    img_url = img.attrs.get("src")
    if not img_url:
        continue

    if not img_url.startswith("http"):
        img_url = "https:" + img_url

    try:
        driver.get(img_url)
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, "img")))
        file_ext = os.path.splitext(img_url)[1]
        screenshot = os.path.join(save_dir, os.path.basename(img_url) + file_ext)
        driver.save_screenshot(screenshot)
        with Image.open(screenshot) as img_file:
            width, height = img_file.size
            if width >= 1000 and height >= 1000:
                print(f"Downloaded {img_url}")
            else:
                os.remove(screenshot)
                print(f"Deleted {img_url}")
    except Exception as e:
        print(f"Error saving {img_url} - {e}")

driver.save_screenshot(screenshot)
time.sleep(1)  # add a delay of 1 second
with Image.open(screenshot) as img_file:
    driver.quit()
