import bs4
import urllib.request as req
# https://www.learncodewithmike.com/2020/11/multithreading-with-python-web-scraping.html
import threading
import time

start_time = time.time()  # 開始時間


def get_data(url):

    request = req.Request(url, headers={

        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = bs4.BeautifulSoup(data, "html.parser")

    titles = root.find_all("div", class_="title")
    likes = root.find_all("div", class_="nrec")
    articles_data = []
    for title, like in zip(titles, likes):
        if title.a:
            if "電影板板規" not in title.a.string:
                article_data = {}
                article_data["文章標題"] = title.a.string

                if like.string is None:
                    article_data["推文數"] = 0
                else:
                    article_data["推文數"] = like.string

                article_url = f"https://www.ptt.cc{title.a['href']}"
                article_request = req.Request(article_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
                                                                    })
                with req.urlopen(article_request) as article_response:
                    article_data_html = article_response.read().decode("utf-8")

                article_soup = bs4.BeautifulSoup(
                    article_data_html, 'html.parser')
                published_time = article_soup.find_all(
                    'span', class_='article-meta-value')
                article_data["發佈時間"] = published_time[3].string

                articles_data.append(article_data)

    return articles_data


def get_URL(url):  # 把取得網址的程式碼拉出來，另外設定一個函式
    request = req.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    root = bs4.BeautifulSoup(data, "html.parser")
    nextLink = root.find("a", string="‹ 上頁")
    return nextLink["href"]


pageURL = "https://www.ptt.cc/bbs/movie/index.html"
""" 
page2URL = "https://www.ptt.cc" + get_URL(pageURL)
page3URL = "https://www.ptt.cc" + get_URL(page2URL) 
"""
# 建立所有網址的清單
pageURLs = [pageURL]
# 透過迴圈取得 pageURL 的下一頁，直到取得三頁為止
while len(pageURLs) < 3:
    nextLink = get_URL(pageURLs[-1])
    pageURLs.append("https://www.ptt.cc" + nextLink)

all_articles = []


def fetch_data_and_save(url):  # 儲存文章資料函式
    articles_data = get_data(url)
    all_articles.extend(reversed(articles_data))


""" 
# 建立三個執行緒
# target 要執行的目標函式 args 關鍵字參數
thread1 = threading.Thread(target=fetch_data_and_save, args=(pageURL,))
thread2 = threading.Thread(target=fetch_data_and_save, args=(page2URL,))
thread3 = threading.Thread(target=fetch_data_and_save, args=(page3URL,))

# 啟動三個執行緒，開始各自執行
thread1.start()
thread2.start()
thread3.start()

# 等待所有三個執行緒完成任務，然後才會繼續執行下一步
thread1.join()
thread2.join()
thread3.join() 
"""

# 建立並啟動執行緒
threads = []
for url in pageURLs:
    thread = threading.Thread(target=fetch_data_and_save, args=(url,))
    thread.start()
    threads.append(thread)

# 等待所有執行緒完成，才會繼續執行寫入的步驟
for thread in threads:
    thread.join()

with open("movie_thread.txt", "w", encoding="utf-8") as file:
    for article in all_articles:
        file.write(article["文章標題"] + "," +
                   str(article["推文數"]) + "," + article["發佈時間"] + "\n")

end_time = time.time()
print(f"花了{end_time - start_time} 秒爬取資料")
