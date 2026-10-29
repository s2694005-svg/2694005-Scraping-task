import csv
import requests
import time
from bs4 import BeautifulSoup

url = "https://www.musashino-u.ac.jp/"

response = requests.get(url, timeout=15)
response.raise_for_status()

response.encoding = 'utf-8'

soup = BeautifulSoup(response.text, "html.parser")

title = soup.title.get_text(strip=True) if soup.title else "タイトルなし"

page_data = {
    "url": url,
    "title": title
}

print("URL:", page_data["url"])
print("タイトル", page_data["title"])

sitemap_url = "https://ef.musashino-u.ac.jp/sitemap/"

response = requests.get(sitemap_url, timeout=15)
response.raise_for_status()

sitemap_soup = BeautifulSoup(response.text, "html.parser")

sitemap_links = []

for link in sitemap_soup.find_all("a", href=True):
    page_url = requests.compat.urljoin(sitemap_url, link["href"])
    print(page_url)

    if "ef.musashino-u.ac.jp" in page_url:
        sitemap_links.append(page_url)

sitemap_links = list(dict.fromkeys(sitemap_links))

print("抽出したリンク数:", len(sitemap_links))

for page_url in sitemap_links[:10]:
    print(page_url)

page_data = {}
visited = set()

for page_url in sitemap_links:
    if page_url in visited:
        continue
    visited.add(page_url)
    try:
        time.sleep(2)

        response = requests.get(page_url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        if soup.title:
            title = soup.title.get_text(strip=True)
        else:
            title = "タイトルなし"

        page_data[page_url] = title

        print(page_url, ":", title)

    except requests.RequestException as e:
        print("取得できませんでした:", page_url, e)

print("タイトルを取得したページ数:", len(page_data))

with open("pages.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["URL", "title"])
    for url, title in page_data.items():
        writer.writerow([url, title])

print("CSVファイルを保存しました!")

print("辞書に保存されたページ数:", len(page_data))
print(page_data)