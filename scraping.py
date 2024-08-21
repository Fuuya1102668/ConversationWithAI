from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import urllib.request
import os
import json

# 印刷用の設定----------------------------------------------
appState = {
    "recentDestinations": [
        {
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }
    ],
    "selectedDestinationId": "Save as PDF",
    "version": 2
}

profile = {'printing.print_preview_sticky_settings.appState': json.dumps(appState),
           'savefile.default_directory': '/home/fuya/AI/ConversationWithAI/rag_source/'} # ここでデフォルトの保存先を設定
#           'savefile.default_directory': '~/'} # ここでデフォルトの保存先を設定

options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', profile)
options.add_argument('--kiosk-printing')  #　印刷用のプロンプトが表示された時、自動的に印刷ボタンが押される
#options.add_argument('--headless')#ヘッドレスモード，オンにしてもよい
driver = webdriver.Chrome(options=options)  # webdriverを設定

#URLにアクセスして，PDFとして保存する---------------------------
url_list = ["https://www.kanazawa-it.ac.jp/index.html"]#PDF化したいURLリスト
for i in range(len(url_list)):
    url = url_list[i]# 対象となるURL
    driver.get(url)#アクセス
    time.sleep(1)
    driver.execute_script('window.print();')  # javascriptを実行して印刷用のプロンプトを表示
    time.sleep(9)#ここを長くしないと，巨大なpdfは印刷されないことになってしまう
    
print("書き込みが完了しました")

