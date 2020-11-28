
import time
import csv
import sys
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

UserId = 'h19980326@gmail.com'
password = 'Sato19980326'

#当月からの位置
for i in range(5):
    month = input("今月分の場合0,遡る場合は遡る月数分,半角数字で入力")
    Er = input("入力："+str(month)+" 正しく半角英数字で入力されていますか？ Y/Nで返してください。Cで終了>>")
    if Er == "Y":
        break
    elif Er =="C":
        sys.exit()


#webドライバの設定
options = Options()
options.add_argument('--headless') #ヘッドレスモードで表示なし
driver = webdriver.Chrome("/usr/local/bin/chromedriver",options=options)

driver.implicitly_wait(15)
driver.set_window_size('1200', '1000')
#moneyforwardのメアドログインページへ遷移
driver.get('https://id.moneyforward.com/sign_in/email?client_id=2WND7CAYV1NsJDBzk13JRtjuk5g9Jtz-4gkAoVzuS_k&nonce=5e477f7b157d27962f77333743286ee8&redirect_uri=https%3A%2F%2Fmoneyforward.com%2Fauth%2Fmfid%2Fcallback&response_type=code&scope=openid+email+profile+address&select_account=true&state=63f16dc363f181e0134d840ecdda67f3')

#メールアドレスの入力とログインボタンの押下
driver.find_element_by_name('mfid_user[email]').send_keys( UserId )
login1 = driver.find_element_by_xpath('/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[3]')
login1.click()
time.sleep(1)

#パスワード入力とログインボタンの押下
driver.find_element_by_name('mfid_user[password]').send_keys( password )
login2 = driver.find_element_by_xpath('/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[3]')
login2.click()
print("ログインが完了しました")


#家計簿への遷移
url_kakebo = "https://moneyforward.com/cf"
driver.get(url_kakebo)
time.sleep(1)

#例外画面のスキップ操作
cur_url = driver.current_url
if 'account_selector' in cur_url :
    login3 = driver.find_element_by_xpath('/html/body/main/div/div/div/div/div[1]/section/form/div[2]/div/div[2]')
    login3.click()

#driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
#月の調整
counta = int(month) + 1

hei = driver.execute_script("return document.body.scrollHeight")
#hei = hei // 2
driver.execute_script("window.scrollTo(0,"+str(hei)+");")

time.sleep(1)
selector = '//*[@id="in_out"]/div[2]'
element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, selector)))
target = driver.find_element_by_xpath('//*[@id="in_out"]/div[2]')
actions = ActionChains(driver)
actions.move_to_element(target)
actions.perform()


time.sleep(1)
if month =="0" :
    driver.find_element_by_class_name("btn fc-button fc-button-today spec-fc-button-click-attached").click()
else:
    for i in range(counta):
        if i == 0:
            time.sleep(1)
            driver.find_element_by_xpath('//*[@id="in_out"]/div[2]/button[3]').click()
            time.sleep(1)
            continue
        driver.find_element_by_xpath('//*[@id="in_out"]/div[2]/button[1]').click()
        time.sleep(1)

#ファイルネームを日付に設定する
fname = driver.find_element_by_class_name('fc-header-title').text
fname2 = fname.replace('/','_')
fname3 = fname2.replace(' - ','-')

#家計簿テーブルデータの取得
table = driver.find_element_by_id("cf-detail-table")
trs = table.find_elements(By.TAG_NAME, "tr")

#header
list_header_line = []
ths = table.find_elements(By.TAG_NAME, 'th')
for i in range(0, len(ths)):
            list_header_line.append(ths[i].text)

#body
list_table = []
for i in range(1, len(trs)):
        tds = trs[i].find_elements(By.TAG_NAME, 'td')
        line = ""
        list_line = []
        for j in range(0, len(tds)):
            list_line.append(tds[j].text)
        list_table.append(list_line)

#出力
print("ファイル書き出し中")
with open('/Users/satohibiki/python/'+ fname3 +'.csv', "w", encoding='utf_8_sig') as f:
    writer = csv.writer(f)  # writerオブジェクトを作成
    writer.writerow(list_header_line) # ヘッダーを書き込む
    writer.writerows(list_table)  # 内容を書き込む


print('/Users/satohibiki/python/'+ fname3 +'.csv で作成完了しました')
driver.close()
driver.quit()
