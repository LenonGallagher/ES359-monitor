import json
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

# =========================
# 設定
# =========================

LISTINGS_FILE = "data/listings.json"

headers = {
    "User-Agent": "Mozilla/5.0"
}

# =========================
# 讀取已記錄網址
# =========================

if os.path.exists(LISTINGS_FILE):
    with open(LISTINGS_FILE, "r", encoding="utf-8") as f:
        known_urls = set(json.load(f))
else:
    known_urls = set()

# =========================
# 讀取關鍵字
# =========================

with open("watchlist.json", "r", encoding="utf-8") as f:
    keywords = json.load(f)

print("=" * 60)
print("ES359 Monitor V0.03")
print("=" * 60)

new_urls = []

# =========================
# 搜尋
# =========================

for keyword in keywords:

    print()
    print(f"🔍 搜尋：{keyword}")
    print("-" * 60)

    search_url = f"https://html.duckduckgo.com/html/?q={quote(keyword)}"

    try:

        response = requests.get(
            search_url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(response.text, "html.parser")

        results = soup.select(".result")

        if not results:
            print("沒有找到結果")
            continue

        for result in results[:3]:

            title_tag = result.select_one(".result__title")
            link_tag = result.select_one(".result__url")

            if not title_tag:
                continue

            title = title_tag.get_text(" ", strip=True)

            if link_tag:
                url = link_tag.get_text(" ", strip=True)
            else:
                url = "無網址"

            if url not in known_urls:

                print("🆕 新發現！")
                print(f"標題：{title}")
                print(f"網址：{url}")
                print()

                known_urls.add(url)
                new_urls.append(url)

            else:

                print("已記錄，略過")

    except Exception as e:

        print("錯誤：", e)

# =========================
# 儲存資料庫
# =========================

with open(LISTINGS_FILE, "w", encoding="utf-8") as f:
    json.dump(
        sorted(list(known_urls)),
        f,
        ensure_ascii=False,
        indent=4
    )

# =========================
# 結果
# =========================

print()
print("=" * 60)
print(f"新增網址數量：{len(new_urls)}")
print(f"資料庫總數量：{len(known_urls)}")
print("=" * 60)