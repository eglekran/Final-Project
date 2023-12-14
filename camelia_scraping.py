import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re

webdriver_path = "C:/Users/skais/OneDrive/Stalinis kompiuteris/chromedriver-win64/chromedriver.exe"
service = Service(webdriver_path)
service.start()
driver = webdriver.Chrome(service=service)
data = []
for i in range(0, 14): #14
    url = f'https://camelia.lt/2292-nereceptiniai-vaistai/?page={i}'
    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(4)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup)

    title = soup.find_all('h5', class_='product-name')
    price = soup.find_all('div', class_='first-prices d-flex flex-wrap align-items-center')
    brand = soup.find_all('h5', class_='product-name')


    for tit, pri, bra in zip(title, price, brand):
        tit_text = tit.get_text().strip()
        pri_text = pri.get_text().replace('€', '').strip()
        bra_text = bra.get_text().split(' ')[0].strip()

        data.append({'Title': tit_text, 'Price (EUR)': pri_text, 'Brand': bra_text})

driver.quit()
df = pd.DataFrame(data)
# print(df)
df.to_csv("camelia.csv", index=False)
#statusas