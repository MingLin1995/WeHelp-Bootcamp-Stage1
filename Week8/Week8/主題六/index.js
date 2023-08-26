/* 一般情況 */
function hello() {
  // 獲取輸入框的值
  const name = document.getElementById("Input").value;

  // 獲取顯示結果的元素
  const helloElement = document.getElementById("hello");

  // 更新元素的內容
  helloElement.innerHTML = name + "，Hello!";
}

/* 攻擊方法 */
//<img src=x onerror=alert("你被攻擊囉！")>

/* 解決方法 */
/* function hello() {
  // 獲取輸入框的值
  const name = document.getElementById("Input").value;

  // 獲取顯示結果的元素
  const helloElement = document.getElementById("hello");

  // 更新元素的內容（改為 innerText 純文字內容）
  helloElement.innerText = name + "，Hello!";
} */

/* function hello() {
  //DOM 型 
  // 獲取輸入框的值
  const name = document.getElementById("Input").value;
  // 獲取顯示結果的元素
  const helloElement = document.getElementById("hello");
  // 更新元素的內容
  helloElement.innerHTML = name + "，Hello!";

  // 反射型 
  // 將輸入的名稱附加到網址的查詢字串中
  const urlParams = new URLSearchParams(window.location.search);
  urlParams.set("name", name);

  // 將更新後的查詢字串設定回網址
  history.replaceState(null, "", "?" + urlParams.toString());
}

// 頁面載入時，從查詢字串中取得並顯示名稱
window.onload = function () {
  const urlParams = new URLSearchParams(window.location.search);
  const nameFromQuery = urlParams.get("name");
  if (nameFromQuery) {
    const helloElement = document.getElementById("hello");
    helloElement.innerHTML = nameFromQuery + "，Hello!";
  }
}; */
