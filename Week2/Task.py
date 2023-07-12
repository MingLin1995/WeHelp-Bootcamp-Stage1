print("----------------------------Task1-------------------------------")


def find_and_print(messages):
    # write down your judgment rules in comments
    """ 
    18歲、大學生、法定年齡、投票，都是大於17歲的關鍵字
    """
    # your code here, based on your own rules
    for key, value in messages.items():
        # print(key, value) 確定可以將鍵、值個別取出
        if "18" in value or "college student" in value or "legal age" in value or "vote" in value:
            print(key)


find_and_print({
    "Bob": "My name is Bob. I'm 18 years old.",
    "Mary": "Hello, glad to meet you.",
    "Copper": "I'm a college student. Nice to meet you.",
    "Leslie": "I am of legal age in Taiwan.",
    "Vivian": "I will vote for Donald Trump next week",
    "Jenny": "Good morning."
})

print('----------------------------Task2-------------------------------')


def calculate_sum_of_bonus(data):
    # write down your bonus rules in comments
    """ 
        獎金總和上限為1萬台幣
        一、薪資、績效、職位的獎金比例分別為3:4:3 
        二、薪資：高於五萬、五萬，低於五萬，比例分別為2:3:5
        三、績效：高於平均、平均、低於平均，比例分別為5:3:2
        四、職位：工程師、CEO、業務，比例分別為4:2:4
    """
    # your code here, based on your own rules
    """ 薪資、績效、職位獎金比例為3:4:3 """
    salaryRatio = 0.3
    performanceRatio = 0.4
    positionRatio = 0.3
    """ 薪資獎金級距 """
    salaryRank1 = 0.5
    salaryRank2 = 0.3
    salaryRank3 = 0.2
    """ 績效獎金級距 """
    performanceRank1 = 0.5
    performanceRank2 = 0.3
    performanceRank3 = 0.2
    """ 職位獎金級距 """
    positionEngineer = 0.4
    positionCEO = 0.2
    positionSales = 0.4

    """ 計算薪資獎金 """
    def calculateSalaryBonus(salary):
        """ 可以觀察到資料有字串、有數字，但要判斷數字大小，所以全部轉換成數字型態 """
        """ 透過isinstance去檢查，若為字串型態就執行以下判斷"""
        if isinstance(salary, str):
            """ 透過isdigit檢查字串是否只包含數字符號 """
            if salary.isdigit():
                salary = int(salary)  # 字串只包含數字符號，所以會直接轉換成整數
            elif "USD" in salary:
                salary = int(salary.replace("USD", "")) * \
                    30  # 移除USD後轉為整數，且換成TWD
            else:
                salary = int(salary.replace(",", ""))  # 移除逗號後轉換為整數

        if salary > 50000:
            return totalBonus * salaryRank3 * salaryRatio
        elif salary == 50000:
            return totalBonus * salaryRank2 * salaryRatio
        else:
            return totalBonus * salaryRank1 * salaryRatio

    """ 計算績效獎金 """
    def calculatePerformanceBonus(performance):
        if performance == "above average":
            return totalBonus * performanceRank1 * performanceRatio
        elif performance == "average":
            return totalBonus * performanceRank2 * performanceRatio
        else:
            return totalBonus * performanceRank3 * performanceRatio

    """ 計算職位獎金 """
    def calculatePositionBonus(position):
        if position == "Engineer":
            return totalBonus * positionEngineer * positionRatio
        elif position == "CEO":
            return totalBonus * positionCEO * positionRatio
        else:
            return totalBonus * positionSales * positionRatio

    """ 資料是字典，值的部分是列表包字典 """
    employees = data["employees"]
    # print(employees) 確定可以將值出，值的資料型態是列表[字典{}]
    """ 透過while True無限循環，直到成功輸入有效獎金才會跳出 """
    while True:
        try:
            totalBonus = int(input("請輸入總獎金金額（最多會以一萬計算）："))
            totalBonus = min(totalBonus, 10000)
            break
        except ValueError:
            print("請輸入阿拉伯數字！")

    """ 計算每個人的獎金 """
    for employee in employees:
        # print(employee) 確定可以取出值，字典的部分
        """ 取出個別字典的值 """
        salary = employee["salary"]
        performance = employee["performance"]
        position = employee["role"]

        salaryBonus = calculateSalaryBonus(salary)
        performanceBonus = calculatePerformanceBonus(performance)
        positionBonus = calculatePositionBonus(position)

        individualBonus = salaryBonus + performanceBonus + positionBonus

        print(f'{employee["name"]}: 獎金為 {int(individualBonus)} 台幣')


calculate_sum_of_bonus({
    "employees": [
        {
            "name": "John",
            "salary": "1000USD",
            "performance": "above average",
            "role": "Engineer"
        },
        {
            "name": "Bob",
            "salary": 60000,
            "performance": "average",
            "role": "CEO"
        },
        {
            "name": "Jenny",
            "salary": "50,000",
            "performance": "below average",
            "role": "Sales"
        }
    ]
})  # call calculate_sum_of_bonus function

print('----------------------------Task3-------------------------------')


def func(*data):
    # your code here
    """ 用來儲存沒有重複第二個字元的人 """
    uniquePerson = []

    """ enumerate(要取出的列表、元組、字串,start=0(設定索引的起始值，預設為0)) """
    for i, name in enumerate(data):
        """ 取得第二個文字 """
        secondWord = name[1]
        """ 判斷是否獨一無二，是的話T，否的話F """
        unique = True

        for j, otherName in enumerate(data):
            """ 排除自己，且第二個字跟別人比較"""
            if i != j and secondWord == otherName[1]:
                unique = False

        """ 如果沒有重複，就把獨一無二的名子加入到列表uniquePerson """
        if unique:
            uniquePerson.append(name)

    """ 如果有獨一無二的人就依序印出來，如果沒有就沒有 """
    if len(uniquePerson) > 0:
        for uniqueName in uniquePerson:
            print(uniqueName)
    else:
        print("沒有人是獨一無二的")


func("彭⼤牆", "王明雅", "吳明")  # print 彭⼤牆
func("郭靜雅", "王立強", "林靜宜", "郭立恆", "林花花")  # print 林花 花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花")  # print 沒有

print('----------------------------Task4-------------------------------')


def get_number(index):
    # your code here
    """ 
    可以找到規律是0+4-1+4-1+4-1的循環 
    index為奇數時+4、偶數時-1 
    0/0=0 所以會被判斷到偶數裡面
    0=x-1 x=1 所以ans一開始設定為1
    """
    ans = 1
    for i in range(index+1):
        if i % 2 == 0:  # index為偶數時會-1
            ans -= 1
        else:
            ans += 4  # index為奇數時會+4
    print(ans)


get_number(1)  # print 4
get_number(5)  # print 10
get_number(10)  # print 15

print('----------------------------Task5-------------------------------')


def find_index_of_car(seats, status, number):
    # your code here
    """ 
    1.找出買票人數
    2.找出那些車廂的狀態是可以買票的
    3.找出可以坐的車廂的座位數(可以用狀態的index去對應車廂座位數)
    4.判斷車廂空位有沒有大於等於買票人數(有的話繼續往下判斷)
    5.找出所有符合買票人數的車廂(跟買票人數相減，取最小的)
    6.找出最適合的車廂(印出index)
    """
    # print(seats) #找出值
    # print(status[4]) #找出"值"的index
    statusOK = []  # 用來儲存狀態ok的車廂的index
    n = 0
    for statusIndividual in status:
        # print(statusIndividual) #個別狀態取出判斷
        if (statusIndividual == 1):
            # print(f'可以乘坐的車廂index為{n}')
            statusOK.append(n)
            n += 1
        else:
            n += 1
    # print(statusOK)

    seatsOK = []  # 用來儲存空位符合買票人數的車廂的index
    for remainingAmount in statusOK:
        # print(remainingAmount) #可以買票的車廂index
        # print(seats[remainingAmount]) #個別空位數
        if (seats[remainingAmount] >= number):  # 空位數大於買票人數
            # print("可以買票")
            seatsOK.append(remainingAmount)

    if not seatsOK:  # if not 用來檢查一個資料集合，如列表、字典，是否為空
        print("-1")
        return  # 用來結束函式

    bestSeat = []  # 所有符合條件的車廂的差異數(車廂空位數-買票人數)
    for seatDifference in seatsOK:
        # print(seats[seatDifference]-number[0])  # 車廂空位數-買票人數
        bestSeat.append(seats[seatDifference]-number)
    # print(bestSeat) #差異數
    # print(min(bestSeat)) #取差異樹的最小值(代表最符合條件)
    # print(bestSeat.index(min(bestSeat))) #透過差異數，找出index

    # seatsOK的index會跟bestSeat的index對應
    # 最佳解[可以買票且符合人數的車廂index]
    print(f'最佳解{seatsOK[bestSeat.index(min(bestSeat))]}')


find_index_of_car([3, 1, 5, 4, 2], [0, 1, 0, 1, 1], 2)  # print 4
find_index_of_car([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4)  # print -1
find_index_of_car([4, 6, 5, 8], [0, 1, 1, 1], 4)  # print 2
