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
    CREATE TABLE IF NOT EXISTS euro(
        Title_euro text,
        Brand text,
        Category text,
        Price_euro text
    )
'''

cursor.execute(create_table_query)
print('lentele sukurta')

webdriver_path = "C:/Users/rkran/OneDrive/Desktop/chromedriver-win64/chromedriver.exe"
service = Service(webdriver_path)
service.start()
driver = webdriver.Chrome(service=service)
data = [] # create empty list

for i in range(1, 13): #12 pages in url

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


    for pav, kai, br, cat  in zip(title, price, brand, category):

        pav_text = pav.get_text().strip()
        kai_text = kai.get_text().replace('€', '').strip()
        br_text = br.get_text().split(' ')[0].strip()
        cat_text = cat.get_text().strip()


        data.append({'Title_euro': pav_text, 'Brand': br_text, 'Category': cat_text, 'Price_euro': kai_text})
        # print(data)
        ###########SQLdb table
        insert_query = '''
                                            INSERT INTO euro(Title_euro, Brand, Category, Price_euro)values(
                                            %s, %s, %s, %s)
                                            '''
        cursor.execute(insert_query, (pav_text, br_text, cat_text, kai_text))
        connection.commit()



df = pd.DataFrame(data)
# print(df)

df.to_csv("euro.csv", index=False)