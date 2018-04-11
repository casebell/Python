
import pymysql
from bs4 import BeautifulSoup
from selenium import webdriver

conn = pymysql.connect(host='--', user='--', password='--', db='--', charset='utf8', autocommit=True)
cursor = conn.cursor()
sql = "select mnf_no, domestic from mnf order by mnf_no"
cursor.execute(sql)
mnfNoList = cursor.fetchall()
driver = webdriver.Chrome('chromedriver')
driver.implicitly_wait(1)

i = 1

for mnfNo in mnfNoList:

    print("제조사 : " + str(mnfNo[0]) + "수입,국산(Y,N) : ", mnfNo[1])

    cursor = conn.cursor()

    sql = "insert into type_car (type_car_no, type_car_group_no, mnf_no, val, img) values(%s, %s, %s, %s, %s) on duplicate key update val = %s"

    optList = ['OS', 'DC', 'RC', 'OC']  # 시판종류

    for opt in optList:

        driver.get('https://auto.naver.com/company/main.nhn?mnfcoNo=' + str(mnfNo[0]) + '&modelType=' + opt + '&order=0&importYn=' + str(mnfNo[1]) + '&page=100')
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        # 1. 페이징 끝 인덱스 추출
        page = soup.select(
            '#content > div.paginate2 > strong'
        )[0].text
        print("페이징 번호 : " + page)

        # 페이징 번호만큼 반복
        for index in range(int(page)):
            driver.get(
                'https://auto.naver.com/company/main.nhn?mnfcoNo=' + str(mnfNo[0]) + '&modelType=' + opt + '&order=0&importYn=' + str(mnfNo[1]) + '&page=' + str(index+1)
            )
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 2. 리스트 추출
            listTypeImg = soup.select(
                '#modelListArea > ul > li > div > div > span > a > img'
            )  # 자동차타입명, 이미지 추출
            listTypeCarGroup = soup.select(
                '#modelListArea > ul > li > div > ul > li.info > a > span'
            )  # 자동차크기 종류 추출
            listModelTypeCar = soup.select(
                '#modelListArea > ul > li > div > ul > li.info > a'
            )  # 자동차 no 추출


            #type_car_group_no = int()  # 1. 소형 2. 준중형 3. 대형 4. 스포츠카

            range(len(listTypeImg))

            # 리스트 전부 반복
            for target in range(len(listTypeImg)):
                if listTypeCarGroup[target].text == '경형':
                    type_car_group_no = 1
                elif listTypeCarGroup[target].text == '준중형':
                    type_car_group_no = 2
                elif listTypeCarGroup[target].text == '중형':
                    type_car_group_no = 3
                elif listTypeCarGroup[target].text == '대형':
                    type_car_group_no = 4
                else:
                    type_car_group_no = 5
                print("-" * 50)
                print(listTypeImg[target].get('alt'))
                print(listTypeImg[target].get('src'))
                print(listTypeCarGroup[target].text)
                print(type_car_group_no)
                print(listModelTypeCar[target].get('onclick').split(',')[2].strip("'"))
                print("-" * 50)
                # #  insert 문 실행
                cursor.execute(sql, (str(i), type_car_group_no, str(mnfNo[0]), listTypeImg[target].get('alt'), listTypeImg[target].get('src'), listTypeImg[target].get('alt')))

                # 자동차 no속 의 세부등급 리스트
                driver.get(
                    'https://auto.naver.com/car/main.nhn?yearsId='+ listModelTypeCar[target].get('onclick').split(',')[2].strip("'") +'&importYn=' + str(mnfNo[1])
                )
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')

                detailList = soup.select(
                    '#carLineupArea > table > tbody > tr'
                )

                for detail in range(len(detailList)):
                    data = soup.select('#carLineupArea > table > tbody > tr > td')
                    cursor.execute(
                        "insert into model_type_car (type_car_no, val, displacement, max_output, fuel_eff, `release`) values (%s, %s, %s, %s, %s, %s)",
                        (str(i),
                         soup.select('#carLineupArea > table > tbody > tr > td > a')[detail].text,
                         data[1 + (5 * detail)].text,
                         data[2 + (5 * detail)].text,
                         data[3 + (5 * detail)].text.strip('\n'),
                         data[4 + (5 * detail)].text.strip('\n')
                         )
                    )
                    print(soup.select('#carLineupArea > table > tbody > tr > td > a')[detail].text)
                    print("="*10)
                    print(soup.select('#carLineupArea > table > tbody > tr > td')[1 + (5 * detail)].text)
                    print(soup.select('#carLineupArea > table > tbody > tr > td')[2 + (5 * detail)].text)
                    print(soup.select('#carLineupArea > table > tbody > tr > td')[3 + (5 * detail)].text.strip('\n'))
                    print(soup.select('#carLineupArea > table > tbody > tr > td')[4 + (5 * detail)].text.strip('\n'))
                i += 1
conn.commit()
conn.close()







