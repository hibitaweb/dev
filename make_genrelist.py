
#モジュールのインポート
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time

url_1 = 'https://www.netflix.com/browse/genre/'
dset = {}
#データ保管用辞書の宣言

#webドライバの設定
options = Options()
options.add_argument('--headless') #ヘッドレスモードで表示なし
driver = webdriver.Chrome("/usr/local/bin/chromedriver",options=options)
driver.get('https://www.netflix.com/jp/')

#ログイン画面に移動
login = driver.find_element_by_css_selector('#appMountPoint > div > div > div > div > div > div.our-story-header-wrapper > div > a')
login.click()

#メールアドレスとパスワードを入力
driver.find_element_by_name('userLoginId').send_keys('h19980326@gmail.com')
driver.find_element_by_name('password').send_keys('Sato0326')

#ログイン
driver.find_element_by_css_selector('#appMountPoint > div > div.login-body > div > div > div.hybrid-login-form-main > form > button').click()
time.sleep(1)
print("ログインが完了しました")

driver.find_element_by_xpath("/html/body/div[1]/div/div/div[1]/div[1]/div[2]/div/div/ul/li[1]/div/a/div/div").click()
time.sleep(1)


#urlのクローリング
for i in range(99999):
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

#以下出力モジュール
import csv

body = list(dset.items())
header = ["tag","title"]

with open('/Users/satohibiki/python/genreList.csv', 'w',encoding='utf_8_sig') as f:
    #文字化け防止エンコード付与
    writer = csv.writer(f)  # writerオブジェクトを作成
    writer.writerow(header) # ヘッダーを書き込む
    writer.writerows(body)  # 内容を書き込む
