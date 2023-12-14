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

for i in range(1, 13): #puslapiu skaicius, 13 psl

    url = f"https://www.eurovaistine.lt/vaistai-nereceptiniai?page={i}"
    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 200);")
        time.sleep(4)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # response = requests.get(url)
    # print(response)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    #print(soup)

    title = soup.find_all('div', class_='title')
    price = soup.find_all('div', class_='productPrice text-end')
    brand = soup.find_all('div', class_='brand')
    category = soup.find_all('div', class_='productMedicineDescription')
    kiekis = soup.find_all(title = soup.find_all('div', class_='title'))
    #status = soup.find_all('div', class_='soldOut')


    for pav, kai, br, cat  in zip(title, price, brand, category):

        pav_text = pav.get_text().strip()
        kai_text = kai.get_text().replace('€', '').strip()
        br_text = br.get_text().split(' ')[0].strip()
        cat_text = cat.get_text().strip()


        data.append({'Title': pav_text, 'Brand': br_text, 'Category': cat_text, 'Price (EUR)': kai_text})
        # print(data)



df = pd.DataFrame(data)
# print(df)

df.to_csv("euro.csv", index=False)