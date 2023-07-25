function checkForm() {
  var agreementCheckbox = document.getElementById("agreement");
  if (agreementCheckbox.checked) {
    /* 已經勾選同意條款，返回 true，允許表單提交 */
    return true;
  } else {
    /* 沒有勾選同意條款，彈出警告視窗，並返回 false，阻止表單提交 */
    alert("請勾選同意條款");
    return false;
  }
}

function calculate() {
  /* 獲取使用者輸入的數字 */
  const number = document.getElementById("numberInput").value;
  /* 檢查是否為正整數 */
  if (isNaN(number) || Number(number) <= 0) {
    alert("請輸入正整數");
  } else {
    /* https://ithelp.ithome.com.tw/articles/10190062 */
    /* 重定向到square頁面，啟動路由 */
    window.location.href = "/square/" + number;
  }
}
