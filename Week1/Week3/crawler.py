# 抓取PTT電影版的網頁原始碼(HTML)
import bs4
import urllib.request as req
url = "https://www.ptt.cc/bbs/movie/index.html"
request = req.Request(url, headers={
    # 建立一個Request物件，附加Request Headers的資訊(要讓伺服器認為是正常使用者)(增加表頭偽裝成瀏覽器)
    # Network→index.html→Headers→Request Headers
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
})
with req.urlopen(request) as response:
    data = response.read().decode("utf-8")
# print(data)  # 確定可以抓到HTML的網頁原始碼

# 用html.parser(固定的用法)讓BeautifulSoup協助解析HTML格式文件
root = bs4.BeautifulSoup(data, "html.parser")

# 尋找標題
# 用find尋找div標籤，class="title"的資料
titles = root.find("div", class_="title")
# print(titles)  # 會出現div標籤包起來的所有內容
# print(titles.a)  # 代表只取到a標籤
print("文章標題：", titles.a.string)  # 代表只取到a標籤內的文字

# 尋找推文數量
like = root.find("div", class_="nrec")  # 不能直接抓span 因為class會變動
print("推文數：", like.string)

# 尋找發布時間 #格式 Fri Jul 14 23:14:36 2023
# 觀察網址變化 點下去前 https://www.ptt.cc/bbs/movie/index.html
# 觀察網址變化 點下去後 https://www.ptt.cc/bbs/movie/M.1689675300.A.439.html
link = root.find("div", "title").a["href"]  # ["href"] 取得超連結的URL
# print(link)  # /bbs/movie/M.1689675300.A.439.html
# 進入第一篇文章連結取得文章內容
article_url = f"https://www.ptt.cc{link}"  # 字串組合變數去達成換網頁的效果
# 重複抓網頁的步驟
article_request = req.Request(article_url, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
})
with req.urlopen(article_request) as article_response:
    article_data = article_response.read().decode("utf-8")

article_soup = bs4.BeautifulSoup(article_data, 'html.parser')
published_time = article_soup.find_all(  # 不只有一個符合條件的標籤，所以要用ALL
    'span', class_='article-meta-value')
print("發佈時間：", published_time[3].string)  # 取第三個
