import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import re


webdriver_path = "C:/Users/rkran/OneDrive/Desktop/chromedriver-win64/chromedriver.exe"
service = Service(webdriver_path)
service.start()
driver = webdriver.Chrome(service=service)

data = []
for i in range(1, 2): #puslapiu skaicius, 29 psl

    url = f"https://vaistai.lt/nereceptiniai-vaistai?page={i}"
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
    for i in soup.find_all('td', attrs={'class': 'vp_list_title'}):
        data.append({"URL": i.a['href']})
        #print(i.a['href'])


#######################################################################################################################

df = pd.DataFrame(data)
#print(df)
df.to_csv("vlinks.csv", index=False)
info = []

for url in df['URL']:
    driver.get(url)
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find_all('table')

    if table:
        title = soup.find('td', class_='vp_item_title')
        tit_text = title.get_text().strip()
        #print(tit_text)

        usage = soup.find('td', class_='vp_item_gamintojas')
        usa_text = usage.get_text().replace('Vartojimas :', '').replace('Gamintojas :', 'N/A').strip()
        #print(usa_text)

        manufacturer = soup.find('td', class_='vp_item_gamintojasinfo')
        man_text = manufacturer.get_text().replace('Gamintojas :', '').strip()
        #print(man_text)


        pharmacy = [a.find('img').get('alt') for a in soup.find_all("td", {"class": "vp_item_pirkinternetu"}) if
                a.find('img')]

        price = soup.select('table.vp_item_kurpirkti')
        print(price)
        #pri_text = [price.get_text().strip().replace('PIRKTI','').replace('€', '').replace(
        #    ',', '.').replace('\xa0 \xa0', ',').replace('\xa0', '').strip()]
        #print(pri_text)



        info_data = {
            'Title': tit_text,
            'Usage': usa_text,
            'Manufacturer': man_text,
            'Pharmacy': pharmacy,
        }

        info.append(info_data)
        #print(info)

df1 = pd.DataFrame(info)
#print(df1)
df1.to_csv("vaistai.csv", index=False)



driver.quit()