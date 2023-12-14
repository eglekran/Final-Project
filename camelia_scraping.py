from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
import psycopg2

# connection to sqldb
db_host = 'localhost'
db_name = 'vaistines'
db_user = 'postgres'
db_password = 'Reggaere'
connection = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_password)
cursor = connection.cursor()

create_table_query = '''
    CREATE TABLE IF NOT EXISTS camelia(
        Title_camelia text,
        Price_camelia text,
        Brand text
    )
'''
cursor.execute(create_table_query)
print('lentele sukurta')

webdriver_path = "C:/Users/rkran/OneDrive/Desktop/chromedriver-win64/chromedriver.exe"
service = Service(webdriver_path)
service.start()
driver = webdriver.Chrome(service=service)
data = []  # create empty list

for i in range(0, 14): #13 pages in url
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

        data.append({'Title_camelia': tit_text, 'Price_camelia': pri_text, 'Brand': bra_text})

        ###########SQLdb table
        insert_query = '''
                                    INSERT INTO camelia(Title_camelia, Price_camelia, Brand)values(%s, %s, %s)
                                    '''
        cursor.execute(insert_query, (tit_text, pri_text, bra_text))
        connection.commit()

driver.quit()
df = pd.DataFrame(data)
# print(df)
df.to_csv("camelia.csv", index=False)
#statusas