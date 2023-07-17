import json  # https://docs.python.org/3/library/json.html
import urllib.request  # https://docs.python.org/3/library/urllib.request.html
import csv  # https://docs.python.org/zh-tw/3/library/csv.html
import collections  # https://docs.python.org/3/library/collections.html

url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"

# 讀取網址的JSON檔案內容
with urllib.request.urlopen(url) as response:
    # 將內容讀取成字串符號，中文的部分用utf-8編碼，儲存在變數data中
    data = response.read().decode('utf-8')

# 分析JSON格式，轉換成python字典格式(null換成None)
parsed_data = json.loads(data)  # 只能分析字串格式(看文件)

""" # 確定能找出所需要的資料
# 景點名稱
stitle = parsed_data['result']['results'][0]['stitle']
print(stitle)
# 區域 資料需整理
address = parsed_data['result']['results'][0]['address']
print(address)
# 經度
longitude = parsed_data['result']['results'][0]['longitude']
print(longitude)
# 緯度
latitude = parsed_data['result']['results'][0]['latitude']
print(latitude)
# 第一張圖檔網址 資料需整理
file = parsed_data['result']['results'][0]['file']
print(file)
# 捷運站名稱
MRT = parsed_data['result']['results'][0]['MRT']
print(MRT) """

""" # 確定可以撈出全部資料
results = parsed_data['result']['results']
for result in results:
    stitle = result['stitle']
    address = result['address']
    longitude = result['longitude']
    latitude = result['latitude']
    file = result['file']
    MRT = result['MRT']

    print("景點名稱：", stitle)
    print("區域：", address)
    print("經度：", longitude)
    print("緯度：", latitude)
    print("第一張圖檔網址：", file)
    print("捷運名稱：", MRT) """

""" # 找出特定區域名稱
results = parsed_data['result']['results']
n = 0
for result in results:
    address = result['address']
    # print(address)
    district = address.split('  ')[1][:3]  # 依照空白去分割，取index 1，前三個字
    if district in ["中正區", "萬華區", "中山區", "大同區", "大安區", "松山區", "信義區", "士林區", "文山區", "北投區", "內湖區", "南港區"]:
        print(district)
        n += 1
print(n)  # 正確要有58筆 """

""" # 找出特定圖檔網址
results = parsed_data['result']['results']
n = 0
for result in results:
    file = result["file"]
    image_links = file.lower().split('.jpg') #都轉成小寫，因為最後一筆資料.jpg是大寫
    first_image_url = image_links[0] + '.jpg'
    print(first_image_url)
    n += 1
print(n) """

# 把資料全部統整起來
ans = []
results = parsed_data['result']['results']
for result in results:
    stitle = result['stitle']

    address = result['address']
    district = address.split('  ')[1][:3]
    if district not in ["中正區", "萬華區", "中山區", "大同區", "大安區", "松山區", "信義區", "士林區", "文山區", "北投區", "內湖區", "南港區"]:
        continue  # 若不是這些區域的，直接跳過這個循環，繼續下一個循環

    longitude = result['longitude']
    latitude = result['latitude']

    file = result["file"]
    image_links = file.lower().split('.jpg')
    first_image_url = image_links[0] + '.jpg'

    MRT = result['MRT']

    information = {
        'stitle': stitle,
        'district': district,
        'longitude': longitude,
        'latitude': latitude,
        'first_image_url': first_image_url,
        'MRT': MRT
    }

    ans.append(information)
# print(ans)  # 確定資料正確

# 新增CSV檔案
attraction = "attraction.csv"
# 寫入attraction.csv
with open(attraction, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for item in ans:
        writer.writerow([item["stitle"], item["district"],
                        item["longitude"], item["latitude"], item["first_image_url"]])


# 新增CSV檔案
mrt = "mrt.csv"

# 建立一個預設值為"空列表"的"字典"
mrt_dict = collections.defaultdict(list)
""" z = {"x": "X值", "y": "Y值"}
xx = z["x"]  # X值
yy = z["y"]  # Y值
print(mrt_dict[xx])  # 找不到名為"x值"的鍵，所以顯示是空值
mrt_dict[xx].append(yy)  # 因為找不到"鍵"，所以會自動用"x值"建立"鍵"，"值"的部分會為列表，再將"Y值"加入到列表中
print(mrt_dict) """

for item in ans:
    stitle = item['stitle']
    MRT = item['MRT']
    # 若mrt_dict中的"鍵"為空值，會自動建立MRT對應的鍵，而"值"就會默認為"列表"，再將stitle加入到這個列表中
    mrt_dict[MRT].append(stitle)

# 寫入mrt.csv
with open(mrt, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    for MRT, stitles in mrt_dict.items():
        # 如果MRT為None就改為附近沒有捷運站
        if MRT is None:
            MRT = "附近沒有捷運站"
        writer.writerow([MRT] + stitles)  # [建立一個列表]+列表連接起來
