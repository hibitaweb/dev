
#モジュールのインポート
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

"""
options = Options()
options.add_argument('--headless')
"""

url_1 = 'https://www.netflix.com/browse/genre/'
dset = {}

driver = webdriver.Chrome("/usr/local/bin/chromedriver")
driver.get('https://www.netflix.com/jp/')
login = driver.find_element_by_css_selector('#appMountPoint > div > div > div > div > div > div.our-story-header-wrapper > div > a')
login.click()
driver.find_element_by_name('userLoginId').send_keys('h19980326@gmail.com')
driver.find_element_by_name('password').send_keys('Sato0326')
driver.find_element_by_css_selector('#appMountPoint > div > div.login-body > div > div > div.hybrid-login-form-main > form > button').click()
time.sleep(1)
driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[1]/div/a/div/div").click()
time.sleep(1)

print("ログインが完了しました")

for i in range(15):
    tag = i
    url = url_1 + str(tag)

    driver.get(url)
    print('進行中('+str(tag)+')')

    html = driver.page_source.encode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    result = soup.find(class_='aro-genre-details')
    genreTitle = None

    try:
        genreTitle = result.get_text()
    except AttributeError:
        genreTitle ='エラー'

    if genreTitle == 'あなたにオススメ':
        genreTitle = '該当なし'

    dset[tag] = str(genreTitle)

driver.close()
driver.quit()

import pprint
pprint.pprint(dset)

import csv
body = list(dset.items())
header = ["tag","title"]
with open('/Users/satohibiki/python/sample.csv', 'w') as f:
    writer = csv.writer(f)  # writerオブジェクトを作成
    writer.writerow(header) # ヘッダーを書き込む
    writer.writerows(body)  # 内容を書き込む
