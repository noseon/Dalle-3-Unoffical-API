from undetected_chromedriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import logging
import requests
import os
import json
                
options = ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--headless")
driver = Chrome(options=options)

def load_UBing(index):
    with open(os.path.join(os.getcwd(), "binng.json"), "r", encoding="utf-8") as file:
        data = json.load(file)
        if isinstance(data, list) and index < len(data):
            return data[index]['value']
        return None

def get_time():
    return datetime.datetime.now().strftime("[%d/%m/%Y %H:%M:%S]")

def download_images(urls, save_folder):
    print(urls)
    try:
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        for index, url in enumerate(urls):
            response = requests.get(url)
            response.raise_for_status()
            filename = os.path.join(save_folder, f"({index + 1}).png")
            with open(filename, 'wb') as file:
                file.write(response.content)

            logging.info(f'{get_time()} Image downloaded successfully and saved to "{filename}"')

    except requests.exceptions.RequestException as e:
        logging.critical(f"Image download failed: {str(e)}")

def open_website(query):
    cookie = {"name": "_U",
              "value": load_UBing(9)}

    driver.get(f'https://www.bing.com/images/create?q={query}')
    logging.info(f"{get_time()} Bing İmage Creator (Dalle-3) Opened")

    driver.add_cookie(cookie)
    driver.refresh()  
      
    page_source = driver.page_source
    data = driver.page_source
    print(data)
    
    download_images(get_urls(), "Temp")

    logging.info(f"{get_time()} Cookie values added ")    
    
    #return True

def get_urls():
    try:
        urls = list(set([element.get_attribute("src") for element in WebDriverWait(driver, 600).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "mimg")))]))

        urls = [url.split('?')[0] for url in urls]
        print(urls)
        return urls
    except Exception as e:
        logging.critical(
            f"Error while extracting image urls. Maybe something is wrong about your prompt. (You can check you prompt manually) \n{e}")
