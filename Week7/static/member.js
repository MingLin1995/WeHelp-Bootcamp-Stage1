/* 留言欄位檢查 */
function validateMessage() {
  var contentInput = document.getElementById("content");
  if (contentInput.value.trim() === "") {
    alert("留言內容不能為空白");
    return false;
  }
  return true;
}

/* 刪除確認，回傳該筆留言的index */
function confirmDelete(messageId) {
  if (confirm("確定要刪除這則留言嗎？")) {
    deleteMessage(messageId);
  }
}

/* 連接後端刪除功能*/
function deleteMessage(messageId) {
  const formData = new FormData();
  formData.append("message_id", messageId);
  fetch("/deleteMessage", {
    method: "POST",
    body: formData,
  }).then(() => {
    location.reload();
  });
}

/* 查詢會員資料功能 */
// https://xhkpandaman.medium.com/%E9%9B%B6%E5%9F%BA%E7%A4%8E-%E7%B0%A1%E6%98%93javascript-8-api-%E5%AD%96%E5%AF%B6-fetch%E5%8F%8Aasync-await-574de2f16dd9
const queryButton = document.getElementById("queryButton");
const queryResult = document.getElementById("queryResult");

queryButton.addEventListener("click", async () => {
  const queryUsername = document.getElementById("queryUsername").value;
  //如果有輸入帳號
  if (queryUsername) {
    //傳送到後端查詢
    const response = await fetch(`/api/member?username=${queryUsername}`);
    //後端回傳回來
    const data = await response.json();
    if (data.data) {
      queryResult.innerHTML = `${data["data"]["name"]}（${data["data"]["username"]}）`;
    } else {
      queryResult.innerHTML = "查無此會員或帳號輸入錯誤";
    }
    //如果沒輸入帳號
  } else {
    queryResult.innerHTML = "請輸入要查詢的會員帳號";
  }
});

/* 更新會員姓名功能 */
const updateButton = document.getElementById("updateButton");
const updateResult = document.getElementById("updateResult");

updateButton.addEventListener("click", async () => {
  const newName = document.getElementById("newName").value;
  if (newName) {
    const response = await fetch("/api/member", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      //將JS物件轉換回JSON格式
      body: JSON.stringify({ name: newName }),
    });
    /* const requestBody = JSON.stringify({ name: newName });
    console.log(requestBody); 確定格式正確*/

    const data = await response.json();
    //data.ok會對應後端回傳的true
    if (data.ok) {
      updateResult.innerHTML = "更新成功";

      /* 同步更新頁面資訊 */
      const welcomeMessageElement = document.getElementById("welcomeMessage");
      welcomeMessageElement.textContent = `${newName}，歡迎登入系統`;

      //登入後，把session刪除，更新姓名就會失敗
    } else {
      updateResult.innerHTML = "更新失敗";
    }
  } else {
    updateResult.innerHTML = "請輸入新的會員姓名";
  }
});
