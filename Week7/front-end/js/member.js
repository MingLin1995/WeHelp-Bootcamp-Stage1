// 在 member.html 頁面載入時，檢查 JWT token 是否有效
document.addEventListener("DOMContentLoaded", async () => {
  const token = localStorage.getItem("token");

  if (!token) {
    // 如果沒有 token，轉跳到登入頁面
    window.location.href = "login.html";
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/member/verify_token", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (response.status === 200) {
      // token 有效，繼續顯示會員頁面內容
      const memberData = await response.json();
      // 顯示歡迎訊息或其他相關內容
    } else {
      // token 無效，轉跳到登入頁面
      window.location.href = "login.html";
    }
  } catch (error) {
    console.error("連接錯誤:", error);
  }
});

// 登出
document.getElementById("logoutButton").addEventListener("click", () => {
  // 清除 Local Storage 中的 token
  localStorage.removeItem("token");
  console.log("Logged out");
  // 重新導向到登入頁面
  window.location.href = "login.html";
});

//會員頁面，顯示會員姓名
document.addEventListener("DOMContentLoaded", async () => {
  // 讀取登入的帳號
  const username = sessionStorage.getItem("username");
  try {
    const response = await fetch("http://127.0.0.1:5000/member/get_name", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username }),
    });

    const data = await response.json();
    if (data.type === "success") {
      document.getElementById(
        "welcomeMessage"
      ).textContent = `${data["memberName"]}，歡迎登入系統`;
    } else {
      console.error("無法獲取會員姓名:", data.message);
    }
  } catch (error) {
    console.error("連接錯誤:", error);
  }
});

// 取得留言板內容
const getMessages = async () => {
  try {
    const response = await fetch("http://127.0.0.1:5000/message/get_content", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    if (data.type === "success") {
      const messagesData = data.messagesData;
      displayMessages(messagesData);
    } else {
      console.error("無法獲取留言板內容:", data.message);
    }
  } catch (error) {
    console.error("連接錯誤:", error);
  }
};
// 顯示留言板內容
const displayMessages = (messagesData) => {
  const messagesContainer = document.getElementById("messagesContainer");
  messagesContainer.innerHTML = ""; // 清空容器

  messagesData.forEach((message) => {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");
    messageElement.innerHTML = `
      <p><strong>${message.name}：${message.content}</strong></p>
    `;

    messagesContainer.appendChild(messageElement);
  });
};
// 在頁面載入完成後取得留言板內容
document.addEventListener("DOMContentLoaded", () => {
  getMessages();
});

// 留言功能
const createMessage = document.querySelector("form[name='createMessage']");
createMessage.addEventListener("submit", async (event) => {
  // 停止表單提交
  event.preventDefault();

  var content = document.getElementById("content").value;
  if (content == "") {
    alert("留言內容不能為空白");
    return; //若空白就跳出
  }

  const username = sessionStorage.getItem("username");
  try {
    const response = await fetch(
      "http://127.0.0.1:5000/message/create_message",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ username: username, content: content }),
      }
    );

    const data = await response.json();
    if (data.type === "success") {
      // 清空輸入框
      document.getElementById("content").value = "";
      // 更新留言板，這裡假設有一個函式 updateMessageBoard 用來更新留言板
      getMessages();
    } else {
      alert("留言發送失敗");
    }
  } catch (error) {
    console.error("連接錯誤:", error);
  }
});

/* ---------------------------------------------------------------- */

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

/* ----------------------------------------------------------------- */

/* 查詢會員帳號功能 */
// https://xhkpandaman.medium.com/%E9%9B%B6%E5%9F%BA%E7%A4%8E-%E7%B0%A1%E6%98%93javascript-8-api-%E5%AD%96%E5%AF%B6-fetch%E5%8F%8Aasync-await-574de2f16dd9
const queryButton = document.getElementById("queryButton");
const queryResult = document.getElementById("queryResult");

queryButton.addEventListener("click", async () => {
  const queryUsername = document.getElementById("queryUsername").value;
  //如果有輸入帳號
  if (queryUsername) {
    //傳送到後端查詢
    const response = await fetch(
      `http://127.0.0.1:5000/member/get_username?username=${queryUsername}`,
      {
        mothod: "GET",
      }
    );

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
  const username = sessionStorage.getItem("username");
  const newName = document.getElementById("newName").value;
  if (newName) {
    const response = await fetch("http://127.0.0.1:5000/member/update_name", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        // 在這裡加入 Token 到 headers
        //Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      //將JS物件轉換回JSON格式
      body: JSON.stringify({ username: username, newName: newName }),
    });

    const data = await response.json();
    //data.ok會對應後端回傳的true
    if (data.ok) {
      updateResult.innerHTML = "更新成功";

      /* 同步更新頁面資訊 */
      const welcomeMessageElement = document.getElementById("welcomeMessage");
      welcomeMessageElement.textContent = `${data["newName"]}，歡迎登入系統`;

      /* 同步更新留言板 */
      getMessages();
    } else {
      updateResult.innerHTML = "更新失敗";
    }
  } else {
    updateResult.innerHTML = "請輸入新的會員姓名";
  }
});
