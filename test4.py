import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import datetime, json
from dateutil.tz import tzutc
from urllib.parse import urlparse, parse_qs, parse_qsl, urlencode, urlunparse
import qrcode

URL='https://www.e-future.co.kr/audio/info.do?bookkey=1031&cd_num=1'
driver = webdriver.Chrome(ChromeDriverManager().install())

parts = urlparse(URL)

#parse_qs의 결과를 dictionary로 캐스팅
qs = dict(parse_qsl(parts.query))

# 필요한 3-8뽑기 루프
for i in range(3,9):
    # i = 3
    qs['cd_num'] = i
    print(qs)
    parts = parts._replace(query=urlencode(qs))
    new_url = urlunparse(parts)
    print('new_url: ',new_url)
    driver.get(new_url)
    driver.implicitly_wait(4) #로딩까지 4초기다리기
    #li를 감싼 div
    firstList = driver.find_element(By.ID,'book_list')
    # div내에서 li리스트 검색
    titleList = firstList.find_elements(By.TAG_NAME,'li')

    # 치환
    special_char = '\/:*?"<>|' #타이틀에 들어가면 안되는것.
    #li는 여러개 이므로 for로 루프
    for li in titleList:
        aTag = li.find_element(By.TAG_NAME,'a')
        href = aTag.get_attribute('href')
        # print('타이틀: ',aTag.text)
        # print('링크: ',href)

        img = qrcode.make(href)
        fName = aTag.text.replace("\n","")
        for c in special_char:
            if c in fName:
                print(fName.find(c), c)
                fName = fName.replace(c, ' ')

        # print('fName::: ',fName)
        img.save("C:/Users/strin/Desktop/pyProject/ashley/qrImg/    "+fName+".png")
        driver.implicitly_wait(3)
        print(type(img))
        print(img.size)
        driver.implicitly_wait(3)

