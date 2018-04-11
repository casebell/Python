
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome('chromedriver')
driver.implicitly_wait(3)

conn = pymysql.connect(host='--', user='--', password='--', db='--', charset='utf8')

cursor = conn.cursor()

sql = "insert into mnf (mnf_no, val, domestic, img) values (%s, %s, %s, %s) on duplicate key update mnf_no = %s"

driver.get('https://auto.naver.com/car/mainList.nhn')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

listM = soup.select(
    '#_vendor_select_layer > div > div.maker_group > div > ul > li > a > img'
)

listNo = soup.select(
    '#_vendor_select_layer > div > div.maker_group > div > ul > li > a'
)

for index in range(len(listM)):
    mnfNo = listNo[index].get('onclick').split(',')[2][1:len(listNo[index].get('onclick').split(',')[2])-1]
    print(listM[index].get('alt'), listM[index].get('data-src'))
    print(mnfNo)
    print(listNo[index].get('href')[len(listNo[index].get('href'))-1])

    # sql = "insert into mnf (mnf_no, val, import, img) values (%s, %s, %s, %s)"

    cursor.execute(sql, (
        mnfNo,
        listM[index].get('alt'),
        listNo[index].get('href')[len(listNo[index].get('href')) - 1],
        listM[index].get('data-src'),
        mnfNo
        )
    )

conn.commit()
conn.close()



