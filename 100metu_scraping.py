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
    CREATE TABLE IF NOT EXISTS metu(
        Title_100metu text,
        Price_100metu decimal,
        Manufacturer text,
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

for i in range(0, 23): #22 pages in url
    url = f'https://www.100metu.lt/prekiu-katalogas/5/nereceptiniai-vaistai?page={i}&cat=240&manufacturers=&atc_descriptions=&registrations=&atcs=&min_price=0&max_price=44&sort=atitle&reimbursed='
    driver.get(url)

    last_height = driver.execute_script("return document.body.scrollHeight")  # for scrolling in window
    while True:
        driver.execute_script("window.scrollBy(0, 300);")
        time.sleep(4)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup)

    title = soup.find_all('span', class_='h1 ng-binding')
    price = soup.find_all('span', class_='price ng-binding')[1:]
    manufacturer = soup.find_all('span', class_='manufacturer ng-binding')
    brand = soup.find_all('span', class_='h1 ng-binding')


    for tit, pri, man, bra in zip(title, price, manufacturer, brand):
        tit_text = tit.get_text().strip()
        pri_text = pri.get_text().replace('€', '').strip()
        man_text = man.get_text().replace('Gamintojas: ', '').strip()
        bra_text = bra.get_text().strip().split(' ')[0]


        data.append({'Title_100metu': tit_text, 'Price_100metu': pri_text, 'Manufacturer': man_text, 'Brand': bra_text})

###########SQLdb table
        insert_query = '''
                            INSERT INTO metu(Title_100metu, Price_100metu, Manufacturer, Brand)values(%s, %s, %s, %s)
                            '''
        cursor.execute(insert_query, (tit_text, pri_text, man_text, bra_text))
        connection.commit()

driver.quit()
df = pd.DataFrame(data)
# print(df)
df.to_csv("100metu.csv", index=False)