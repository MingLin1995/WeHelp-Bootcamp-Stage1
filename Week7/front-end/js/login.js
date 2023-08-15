/* 註冊 */

const registerForm = document.querySelector("form[name='registerForm']");
registerForm.addEventListener("submit", async (event) => {
  // 停止表單提交
  event.preventDefault();

  var name = document.getElementById("registerName").value;
  var username = document.getElementById("registerUsername").value;
  var password = document.getElementById("registerPassword").value;

  if (name == "" || username == "" || password == "") {
    alert("註冊欄位不得為空白");
    return; //若空白就跳出
  }

  const requestData = {
    name: name,
    username: username,
    password: password,
  };

  try {
    const response = await fetch("http://127.0.0.1:5000/member/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });

    const data = await response.json();
    if (data["type"] == "success") {
      //跳出註冊成功通知
      alert(data["message"]);
      window.location.href = "login.html";
    } else {
      // 註冊失敗，轉跳到錯誤頁面，並帶上錯誤訊息
      const errorMessage = encodeURIComponent(data["message"]);
      window.location.href = `error.html?message=${errorMessage}`;
    }
  } catch (error) {
    console.error("連接錯誤:", error);
  }
});

/* 登入 */

const loginForm = document.querySelector("form[name='loginForm']");
loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  var username = document.getElementById("loginUsername").value;
  console.log(username);
  var password = document.getElementById("loginPassword").value;
  console.log(password);

  if (username == "" || password == "") {
    alert("帳號或密碼不得為空白");
    return; //若空白就跳出
  }

  const requestData = {
    username: username,
    password: password,
  };

  try {
    const response = await fetch("http://127.0.0.1:5000/member/signin", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });

    const data = await response.json();
    if (data["type"] == "success") {
      // 儲存登入帳號到 Session Storage
      sessionStorage.setItem("username", data["username"]);

      // 將 token 儲存到 Local Storage
      localStorage.setItem("token", data.token);

      //登入成功，轉跳會員頁面
      window.location.href = "member.html";
    } else {
      // 登入失敗，轉跳到錯誤頁面，並帶上錯誤訊息
      const errorMessage = encodeURIComponent(data["message"]);
      window.location.href = `error.html?message=${errorMessage}`;
    }
  } catch (error) {
    console.error("连接错误:", error);
  }
});

/* 錯誤 */
