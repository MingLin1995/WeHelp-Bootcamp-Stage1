/* ---------------------------註冊--------------------------- */
async function submitRegisterForm() {
  const name = document.getElementById("registerName").value;
  const username = document.getElementById("registerUsername").value;
  const password = document.getElementById("registerPassword").value;

  //判斷是否為空白欄位
  if (name == "" || username == "" || password == "") {
    alert("註冊欄位不得為空白");
    return; //若空白就跳出，不執行下面程式碼
  }

  //將要重送到後端的值，用物件（字典）打包起來
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
      //跳出回傳值，"註冊成功"通知
      alert(data["message"]);
      //導向到login.html
      window.location.href = "login.html";
    } else {
      // 註冊失敗，轉跳到錯誤頁面，並帶上錯誤訊息
      window.location.href = `error.html?message=${data["message"]}`;
    }
  } catch (error) {
    console.error("連接錯誤:", error);
  }
}

/* ---------------------------登入--------------------------- */
async function submitLogin() {
  const username = document.getElementById("loginUsername").value;
  const password = document.getElementById("loginPassword").value;

  if (username == "" || password == "") {
    alert("帳號或密碼不得為空白");
    return;
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
      localStorage.setItem("token", data["token"]);

      //登入成功，轉跳會員頁面
      window.location.href = "member.html";
    } else {
      // 登入失敗，轉跳到錯誤頁面，並帶上錯誤訊息
      window.location.href = `error.html?message=${data["message"]}`;
    }
  } catch (error) {
    console.error("連接錯誤:", error);
  }
}
