""" 
1.先試著找出標題、推文數量、發佈時間
2.找出第一頁每個標題、推文數量、發佈時間
3.合併標題、推文數量，透過標題的判斷，排除板規以及被刪除的文章，再找出推文數
4.透過篩選後的文章標題，找出超連結，進入後取出發佈時間
5.透過函式回傳功能，達到換頁的功能
"""
import bs4
import urllib.request as req


def get_data(url):
    # url = "https://www.ptt.cc/bbs/movie/index.html" 有定義函式，就不用這一段了
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

    """ # 尋找標題
    # 用find尋找div標籤，class="title"的資料
    titles = root.find("div", class_="title")
    print(titles)  # 會出現div標籤包起來的所有內容
    print(titles.a)  # 代表只取到a標籤
    print("文章標題：", titles.a.string)  # 代表只取到a標籤內的文字 """
    """ # 尋找每個文章標題，排除電影板板規以及被刪除的文章
    titles = root.find_all("div", class_="title")
    for title in titles:
        if title.a:  # 排除被刪除的文章(會沒有超連結)
            if "電影板板規" not in title.a.string:  # 排除電影板板規
                print("文章標題：", title.a.string)
            else:
                break """

    """ # 尋找推文數量
    like = root.find("div", class_="nrec")  # 不能直接抓span 因為class會變動
    print("推文數：", like.string) """
    """ # 尋找每個推文數量
    likes = root.find_all("div", class_="nrec")
    for like in likes:
        if like.string is None:  # 判斷是否為 None，若是則顯示 0，否則顯示推文數量
            print("推文數：", 0)
        else:
            print("推文數：", like.string) """

    """ # 尋找發布時間 #格式 Fri Jul 14 23:14:36 2023
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
    print("發佈時間：", published_time[3].string)  # 取第三個 """
    """ ----------------------------------------------------------------- """
    titles = root.find_all("div", class_="title")
    likes = root.find_all("div", class_="nrec")
    articles_data = []  # 用來保存"每頁"的資料
    for title, like in zip(titles, likes):
        if title.a:  # 排除被刪除的文章(會沒有超連結)
            if "電影板板規" not in title.a.string:  # 排除電影板板規
                article_data = {}  # 建立一個空的字典來保存每筆的資料
                article_data["文章標題"] = title.a.string  # 自動新增鍵，並且賦值
                # print("文章標題：", title.a.string)

                # 推文數
                if like.string is None:  # 判斷是否為 None，若是則顯示 0，否則顯示推文數量
                    article_data["推文數"] = 0
                    # print("推文數：", 0)
                else:
                    article_data["推文數"] = like.string
                    # print("推文數：", like.string)

                # 發佈時間
                # 直接透過篩選過的title去找href
                article_url = f"https://www.ptt.cc{title.a['href']}"
                article_request = req.Request(article_url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
                                                                    })
                with req.urlopen(article_request) as article_response:
                    article_data_html = article_response.read().decode("utf-8")

                article_soup = bs4.BeautifulSoup(
                    article_data_html, 'html.parser')
                published_time = article_soup.find_all(  # 不只有一個符合條件的標籤，所以要用ALL
                    'span', class_='article-meta-value')
                article_data["發佈時間"] = published_time[3].string
                # print("發佈時間：", published_time[3].string)  # 取第三個

                # 將"這筆"的三個資料加入到列表
                articles_data.append(article_data)
    # print(articles_data)

    # 抓取上一頁的連結
    # 找到內文是‹ 上頁的a標籤，用字串去找才不會找到其他選項連結
    nextLink = root.find("a", string="‹ 上頁")
    return nextLink["href"], articles_data  # 回傳下一頁的連結和這一頁的所有文章資料


""" # 主程序:抓取一個頁面的標題
pageURL = "https://www.ptt.cc/bbs/movie/index9610.html"
pageURL = "https://www.ptt.cc"+get_data(pageURL)  # 呼叫函式，return的結果會回傳回來
# print(pageURL) #確定會印出上一頁的網址 """

# 儲存"三頁"的所有資訊
all_articles = []
# 抓取三頁
pageURL = "https://www.ptt.cc/bbs/movie/index.html"
count = 0
while count < 3:
    nextLink, articles_data = get_data(pageURL)  # 關鍵字：多重賦值用法，回傳兩個值用,隔開

    # 將每一頁的文章資料反向後再合併到 all_articles 列表中(PTT最新的文章是在最下面)
    # https://www.runoob.com/python3/python3-func-reversed.html
    # https://blog.csdn.net/qq_41800366/article/details/86367465 (append與extend差異)
    all_articles.extend(reversed(articles_data))

    pageURL = "https://www.ptt.cc"+nextLink
    # pageURL = "https://www.ptt.cc" + get_data(pageURL)

    count += 1
    # print("-------------------換頁成功------------------------")

# 將資料寫入txt檔案（依序印出）
with open("movie.txt", "w", encoding="utf-8") as file:
    for article in all_articles:
        file.write(article["文章標題"] + "," +
                   str(article["推文數"]) + "," + article["發佈時間"] + "\n")
