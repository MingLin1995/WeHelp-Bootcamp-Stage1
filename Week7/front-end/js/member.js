/* ---------------------------Token檢查--------------------------- */
//載入member頁面檢查Token
window.onload = function () {
  checkToken();
  getName();
  getMessages();
};

// 檢查 JWT token 是否有效
async function checkToken() {
  // 讀取登入的帳號
  const username = sessionStorage.getItem("username");
  //取得後端傳過來的token
  const token = localStorage.getItem("token");

  // 如果token為空值或是不存在，轉跳到登入頁面
  if (!token) {
    window.location.href = "login.html";
    return;
  }

  try {
    const response = await fetch("http://127.0.0.1:5000/member/verify_token", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        username: username,
      },
    });

    const data = await response.json();
    if (data["type"] == "success") {
    } else {
      // token 無效，轉跳到登入頁面
      window.location.href = "login.html";
    }
  } catch (error) {
    console.error("連接錯誤:", error);
  }
}

//會員頁面，顯示會員姓名
async function getName() {
  const username = sessionStorage.getItem("username");
  try {
    const response = await fetch(
      `http://127.0.0.1:5000/member/get_name?username=${username}`,
      {
        method: "GET",
      }
    );

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
}

// 登出
document.getElementById("logoutButton").addEventListener("click", () => {
  // 清除 Local Storage 中的 token
  localStorage.removeItem("token");
  // 重新導向到登入頁面
  window.location.href = "login.html";
});

/* ------------------查詢帳號、更新姓名功能------------------- */
/* 查詢會員帳號功能 */
// https://xhkpandaman.medium.com/%E9%9B%B6%E5%9F%BA%E7%A4%8E-%E7%B0%A1%E6%98%93javascript-8-api-%E5%AD%96%E5%AF%B6-fetch%E5%8F%8Aasync-await-574de2f16dd9
async function submitQuery() {
  const queryResult = document.getElementById("queryResult");
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
    console.log(data);
    if (data["type"] == "success") {
      queryResult.innerHTML = `${data["message"]["name"]}（${data["message"]["username"]}）`;
    } else {
      queryResult.innerHTML = "查無此會員或帳號輸入錯誤";
    }
    //如果沒輸入帳號
  } else {
    queryResult.innerHTML = "請輸入要查詢的會員帳號";
  }
}

/* 更新會員姓名功能 */
async function submitUpdate() {
  const updateResult = document.getElementById("updateResult");
  const username = sessionStorage.getItem("username");
  const newName = document.getElementById("newName").value;
  if (newName) {
    const response = await fetch("http://127.0.0.1:5000/member/update_name", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ username: username, newName: newName }),
    });

    const data = await response.json();
    //data.ok會對應後端回傳的true
    if (data["type"] == "success") {
      updateResult.innerHTML = "更新成功";

      /* 同步更新頁面資訊 */
      getName();

      /* 同步更新留言板 */
      getMessages();
    } else {
      updateResult.innerHTML = "更新失敗";
    }
  } else {
    updateResult.innerHTML = "請輸入新的會員姓名";
  }
}

/* ---------------------------留言板功能--------------------------- */
// 取得留言板內容
async function getMessages() {
  try {
    const response = await fetch("http://127.0.0.1:5000/message/get_content", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
    });
    const data = await response.json();
    if (data["type"] == "success") {
      const messagesData = data["messagesData"];
      //顯示留言板內容
      displayMessages(messagesData);
    }
  } catch (error) {
    console.error("連接錯誤:", error);
  }
}

// 顯示留言板內容
const displayMessages = (messagesData) => {
  const messagesContainer = document.getElementById("messagesContainer");
  messagesContainer.innerHTML = ""; // 清空容器

  messagesData.forEach((message) => {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message");

    // 判斷是否顯示刪除按鈕
    const username = sessionStorage.getItem("username");
    const showDeleteButton = message["username"] == username;

    // 顯示留言內容
    /*
    showDeleteButton 為布林值，判斷是否登入者的留言
    ? 代表分隔符號 
    若為T 執行　：　左邊的程式碼(建立按鈕)
    若為F 執行　：　右邊的程式碼
    */
    messageElement.innerHTML = `
  <p>${message["name"]}：${message["content"]} ${
      showDeleteButton
        ? '<button class="deleteButton" onclick="deleteMessage(' +
          message["id"] +
          ')">刪除</button>'
        : ""
    }</p>
`;

    messagesContainer.appendChild(messageElement);
  });
};

// 留言功能
async function submitMessage() {
  const content = document.getElementById("content").value;
  if (content == "") {
    alert("留言內容不能為空白");
    return;
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
    if (data["type"] == "success") {
      // 清空輸入框
      document.getElementById("content").value = "";
      // 更新留言板
      getMessages();
    } else {
      alert("留言發送失敗");
    }
  } catch (error) {
    console.error("連接錯誤:", error);
  }
}

// 刪除留言功能
async function deleteMessage(messageId) {
  try {
    const token = localStorage.getItem("token");
    const response = await fetch(
      `http://127.0.0.1:5000/message/delete/${messageId}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    const data = await response.json();
    if (data["type"] == "success") {
      // 刪除成功後，更新留言板內容
      getMessages();
    } else {
      console.error(data["message"]);
    }
  } catch (error) {
    console.error("連接錯誤:", error);
  }
}