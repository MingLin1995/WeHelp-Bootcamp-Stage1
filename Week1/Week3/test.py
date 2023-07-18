""" 
一直印出網頁上沒有顯示的內容

標題： [討論] 讓子彈飛 為什麼要帶銀子？
推文數： 1
發佈時間： Sat Sep  4 19:59:47 2021

"""

import bs4
import urllib.request as req
url = "https://www.ptt.cc/bbs/movie/index.html"
request = req.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
})
with req.urlopen(request) as response:
    data = response.read().decode("utf-8")

root = bs4.BeautifulSoup(data, "html.parser")


# 尋找所有文章標題與推文數量的元素
titles = root.find_all("div", class_="title")
likes = root.find_all("div", class_="nrec")

# 尋找第一頁所有文章的連結
links = []
for title in titles:
    if title.a:  # 確認是否有超連結
        links.append(title.a["href"])

# 顯示第一頁所有文章的標題與推文數量
for title, like, link in zip(titles, likes, links):
    # 判斷是否為被刪除的文章
    is_deleted = title.a is None and like.string is None
    # 判斷是否為電影板板規
    is_board_rule = "電影板板規" in title.text

    if not is_deleted and not is_board_rule:

        print("標題：", title.a.string)

        # 判斷是否為 None，若是則顯示 0，否則顯示推文數量
        print("推文數：", 0 if like.string is None else like.string)

        # 進入每篇文章連結取得發佈時間
        article_url = f"https://www.ptt.cc{link}"
        article_request = req.Request(article_url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        })

        with req.urlopen(article_request) as article_response:
            article_data = article_response.read().decode("utf-8")

        article_soup = bs4.BeautifulSoup(article_data, 'html.parser')
        published_time = article_soup.find_all(
            'span', class_='article-meta-value')
        print("發佈時間：", published_time[3].string)
