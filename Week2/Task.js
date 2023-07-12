console.log("----------------------------Task1-------------------------------");
function findAndPrint(messages) {
  // write down your judgment rules in comments
  /* 18歲、大學生、法定年齡、投票，都是大於17歲的關鍵字 */
  // your code here, based on your own rules
  for (var key in messages) {
    /* console.log(key); 確定可以找到key*/
    /* console.log(messages[key]); 確定可以找到value*/
    var value = messages[key];
    if (
      value.includes("18") ||
      value.includes("college student") ||
      value.includes("legal age") ||
      value.includes("vote")
    ) {
      console.log(key);
    }
  }
}

findAndPrint({
  Bob: "My name is Bob. I'm 18 years old.",
  Mary: "Hello, glad to meet you.",
  Copper: "I'm a college student. Nice to meet you.",
  Leslie: "I am of legal age in Taiwan.",
  Vivian: "I will vote for Donald Trump next week",
  Jenny: "Good morning.",
});

console.log("----------------------------Task2-------------------------------");
function calculateSumOfBonus(data) {
  // write down your bonus rule in comments
  /* 
    獎金總和上限為1萬台幣
    一、薪資、績效、職位的獎金比例分別為3:4:3 3000 4000 3000
    二、薪資：高於五萬、五萬，低於五萬，比例分別為2:3:5 600 900 1500
    三、績效：高於平均、平均、低於平均，比例分別為5:3:2 
    四、職位：工程師、CEO、業務，比例分別為4:2:4 
  */
  // your code here, based on your own rules
  /* 薪資、績效、職位獎金比例為3:4:3 */
  const salaryRatio = 0.3;
  const performanceRatio = 0.4;
  const positionRatio = 0.3;
  /* 薪資獎金級距 */
  const salaryRank1 = 0.5;
  const salaryRank2 = 0.3;
  const salaryRank3 = 0.2;
  /* 績效獎金級距 */
  const performanceRank1 = 0.5;
  const performanceRank2 = 0.3;
  const performanceRank3 = 0.2;
  /* 職位獎金級距 */
  const positionEngineer = 0.4;
  const positionCEO = 0.2;
  const positionSales = 0.4;

  /* 計算薪資獎金 */
  function calculateSalaryBonus(salary) {
    if (typeof salary == "string") {
      /* !isNaN可以判斷是否有效，如果int轉換以後是NaN代表有混雜其他字符，就會回傳False */
      if (!isNaN(salary)) {
      } else if (salary.includes("USD")) {
        salary = parseInt(salary.replace("USD", "")) * 30;
      } else {
        salary = parseInt(salary.replace(",", ""));
      }
    }

    if (salary > 50000) {
      return Math.floor(totalBonus * 0.2 * salaryRatio);
    } else if (salary == 50000) {
      return Math.floor(totalBonus * 0.3 * salaryRatio);
    } else {
      return Math.floor(totalBonus * 0.5 * salaryRatio);
    }
  }

  /* 計算績效獎金 */
  function calculatePerformanceBonus(performance) {
    if (performance == "above average") {
      return Math.floor(totalBonus * 0.5 * performanceRatio);
    } else if (performance == "average") {
      return Math.floor(totalBonus * 0.3 * performanceRatio);
    } else {
      return Math.floor(totalBonus * 0.2 * performanceRatio);
    }
  }

  /* 計算職位獎金 */
  function calculatePositionBonus(position) {
    if (position == "Engineer") {
      return Math.floor(totalBonus * 0.4 * positionRatio);
    } else if (position == "CEO") {
      return Math.floor(totalBonus * 0.2 * positionRatio);
    } else {
      return Math.floor(totalBonus * 0.4 * positionRatio);
    }
  }

  const employees = data["employees"];

  let totalBonus = null;
  /* 判斷若沒輸入值(空值)，就會一直循環 */
  while (totalBonus == null) {
    const input = prompt("請輸入總獎金金額（最多會以一萬計算）：");
    /* 正規表示式：/[^\d]/g 數字以外的任何字符 g檢查完全部的值才會停止 */
    const inputWithoutPunctuation = input.replace(/[^\d]/g, "");
    /* 判斷整個字串是否為數字符號:^代表字串的開頭；/d代表數字型符號；$代表字串結尾 */
    const isValidNumber = /^\d+$/.test(inputWithoutPunctuation);

    if (isValidNumber) {
      /* 字串轉為數字型態 */
      totalBonus = parseInt(inputWithoutPunctuation);
      /* 若輸入的值大於一萬，以一萬計算 */
      if (totalBonus > 10000) {
        totalBonus = 10000;
      }
    } else {
      alert("請輸入阿拉伯數字！");
    }
  }

  /* 計算每個人的獎金 */
  for (const employee of employees) {
    const salary = employee["salary"];
    const performance = employee["performance"];
    const position = employee["role"];

    const salaryBonus = calculateSalaryBonus(salary);
    const performanceBonus = calculatePerformanceBonus(performance);
    const positionBonus = calculatePositionBonus(position);

    const individualBonus = salaryBonus + performanceBonus + positionBonus;

    console.log(`${employee["name"]}: 獎金為 ${individualBonus} 台幣`);
  }
}

calculateSumOfBonus({
  employees: [
    {
      name: "John",
      salary: "1000USD",
      performance: "above average",
      role: "Engineer",
    },
    {
      name: "Bob",
      salary: 60000,
      performance: "average",
      role: "CEO",
    },
    {
      name: "Jenny",
      salary: "50,000",
      performance: "below average",
      role: "Sales",
    },
  ],
}); // call calculateSumOfBonus function

console.log("----------------------------Task3-------------------------------");
function func(...data) {
  // your code here
  /* 用來儲存沒有重複第二個字元的人 */
  let uniquePerson = [];

  /* 用迴圈找出人名 */
  for (let i = 0; i < data.length; i++) {
    let name = data[i];
    let secondWord = name[1];
    let unique = true;

    for (let j = 0; j < data.length; j++) {
      let otherName = data[j];
      /* 用迴圈找出其他人名並且比較第二個字 */
      if (i !== j && secondWord == otherName[1]) {
        unique = false;
      }
    }

    /* 如果沒有重複，就把獨一無二的名子加入到列表uniquePerson */
    if (unique) {
      uniquePerson.push(name);
    }
  }

  /* 如果有獨一無二的人就依序印出來，如果沒有就沒有  */
  if (uniquePerson.length > 0) {
    for (let uniqueName of uniquePerson) {
      console.log(uniqueName);
    }
  } else {
    console.log("沒有人是獨一無二的");
  }
}

func("彭⼤牆", "王明雅", "吳明"); // print 彭⼤牆
func("郭靜雅", "王立強", "林靜宜", "郭立恆", "林花花"); // print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花"); // print 沒有

console.log("----------------------------Task4-------------------------------");
function getNumber(index) {
  // your code here
  /* 
    可以找到規律是0+4-1+4-1+4-1的循環 
    index為奇數時+4、偶數時-1 
    0/0=0 所以會被判斷到偶數裡面
    0=x-1 x=1 所以ans一開始設定為1 
  */
  let ans = 1;
  for (let i = 0; i < index + 1; i++) {
    if (i % 2 == 0) {
      ans -= 1;
    } else {
      ans += 4;
    }
  }
  console.log(ans);
}

getNumber(1); // print 4
getNumber(5); // print 10
getNumber(10); // print 15

console.log("----------------------------Task5-------------------------------");
function findIndexOfCar(seats, status, number) {
  // your code here
  /*
  1.找出買票人數
  2.找出那些車廂的狀態是可以買票的
  3.找出可以坐的車廂的座位數(可以用狀態的index去對應車廂座位數)
  4.判斷車廂空位有沒有大於等於買票人數(有的話繼續往下判斷)
  5.找出所有符合買票人數的車廂(跟買票人數相減，取最小的)
  6.找出最適合的車廂(印出index)
  */

  let statusOK = [];
  let n = 0;
  for (statusIndividual of status) {
    if (statusIndividual == 1) {
      statusOK.push(n);
      n += 1;
    } else {
      n += 1;
    }
  }

  let seatsOK = [];
  for (remainingAmount of statusOK) {
    if (seats[remainingAmount] >= number) {
      seatsOK.push(remainingAmount);
    }
  }

  if (seatsOK.length == 0) {
    console.log("-1");
    return;
  }

  let bestSeat = [];
  for (seatDifference in seatsOK) {
    bestSeat.push(seats[seatsOK[seatDifference]] - number);
  }

  console.log(`最佳解${seatsOK[bestSeat.indexOf(Math.min(...bestSeat))]}`);
}

findIndexOfCar([3, 1, 5, 4, 2], [0, 1, 0, 1, 1], 2); // print 4
findIndexOfCar([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4); // print -1
findIndexOfCar([4, 6, 5, 8], [0, 1, 1, 1], 4); // print 2
