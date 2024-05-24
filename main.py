import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import re
from bs4 import BeautifulSoup
import requests
import csv
# Get the current working directory
current_directory = os.getcwd()

# Set the path to the Chrome driver executable
chrome_driver_path = os.path.join(current_directory, 'chromedriver')

# Chrome options
chrome_options = Options()
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)


def getImageLinks(brand : str , model : str ) :
    try :
        driver.get(f"https://cardekho.com/carmodels/{brand}/{model}")

        time.sleep(2)

        html = driver.page_source 
        soup = BeautifulSoup(html , 'html.parser') 
        ul_element = soup.find('ul', {'data-carousel': 'OverviewTop'})
        image_link = ul_element.find('img')["src"]
        # print(image_link)
        return image_link
    except Exception as e :
        print(f"No image found for the {brand} - {model}")




def download_images(image_url, brand, model):
    folder_path = os.path.join('images', brand, model)
    os.makedirs(folder_path, exist_ok=True)
    # for i, url in enumerate(image_urls, start=1):
    image_name = f"{model}.jpg"
    image_path = os.path.join(folder_path, image_name)
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {image_name} to {folder_path}")
    else:
        print(f"Failed to download {image_name}")



def readCSVFile(path):
    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            brand = row['Brand'].split(" ")[0].capitalize()
            model = row['Models'].replace(" ","-").capitalize()
            req_model = brand + "_" + model 
            print (brand , model )
            image_url = getImageLinks(brand , req_model)
            if image_url:
                download_images(image_url, brand, model)
            else:
                print(f"No images found for {brand} {model}")

readCSVFile("Vehicles.csv")
# getImageLinks("Maruti" , "Maruti_Wagon-R");
driver.quit()





