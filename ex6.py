import requests
from bs4 import BeautifulSoup

url = 'https://www.musashino-u.ac.jp'
res = requests.get(url)

print(f"ステータスコード : {res.status_code}")
print(f"ステータスメッセージ : {res.reason}")

# HTMLのソースコードをBeautifulSoupオブジェクトに変換する処理
# html_soup = BeautifulSoup(res.text, 'html.parser')
html_soup = BeautifulSoup(res.content, 'html.parser')
print(f"html_soupの型 : {type(html_soup)}")
