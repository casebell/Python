from selenium import webdriver
from bs4 import BeautifulSoup


driver = webdriver.Chrome('chromedriver')
driver.implicitly_wait(3)
driver.get('https://auto.naver.com/company/main.nhn?mnfcoNo=16&importYn=N&page=1')


html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
listV = soup.select(
    '#modelListArea > ul > li > div'
)

for var in listV:
    print(var)

# driver = webdriver.PhantomJS('phantomjs-2.1.1-windows/bin/phantomjs')


