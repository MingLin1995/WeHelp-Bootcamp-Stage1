//https://shunnien.github.io/2017/07/03/Get-Query-String-Parameters-with-JavaScript/

// 取得要求字串
const urlParams = new URLSearchParams(window.location.search);
//取出要求字串中的message參數，並且解碼字串符號
const errorMessage = decodeURIComponent(urlParams.get("message"));

// 顯示在錯誤頁面上
const errorMessageElement = document.getElementById("errorMessage");
errorMessageElement.textContent = errorMessage;
