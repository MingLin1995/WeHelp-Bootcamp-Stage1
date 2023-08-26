/* ---------------------------註冊--------------------------- */
async function submitRegisterForm() {
  const name = document.getElementById("registerName").value;
  const username = document.getElementById("registerUsername").value;
  const password = document.getElementById("registerPassword").value;

  //判斷是否為空白欄位
  //使用 .trim() 方法刪除首、尾空白字符，然後進行比較(否則還是可以輸入空白)
  if (name.trim() == "" || username.trim() == "" || password.trim() == "") {
    alert("註冊欄位不得為空白");
    return; //若空白就跳出，不執行下面程式碼
  }

  // 驗證格式
  if (!isValidName(name)) {
    alert("姓名格式不正確，請輸入中文或英文，至少兩個字元");
    return;
  }

  if (!isValidUsername(username)) {
    alert("帳號格式不正確，請輸入英文或數字，至少六個字元");
    return;
  }

  if (!isValidPassword(password)) {
    alert(
      "密碼格式不正確，請輸入包含一個大寫英文、一個小寫英文以及數字，至少六個字元"
    );
    return;
  }
  //https://toolbox.tw/regexcode/ 正則表達產生器
  //https://regex101.com/ 驗證
  function isValidName(name) {
    // 姓名格式驗證，只能是中文、英文或空格，至少兩個字元
    const namePattern = /^[\u4e00-\u9fa5A-Za-z\s]{2,}$/;
    return namePattern.test(name);
  }

  function isValidUsername(username) {
    // 帳號格式驗證，只能是英文或數字，至少六個字元
    const usernamePattern = /^[A-Za-z0-9]{6,}$/;
    return usernamePattern.test(username);
  }

  function isValidPassword(password) {
    // 密碼格式驗證，包含一個大寫、一個小寫以及數字，至少六個字元
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$/;
    return passwordPattern.test(password);
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

  if (username.trim() == "" || password.trim() == "") {
    alert("登入欄位不得為空白");
    return;
  }

  if (!isValidUsername(username)) {
    alert("帳號格式不正確，請輸入英文或數字，至少六個字元");
    return;
  }

  if (!isValidPassword(password)) {
    alert(
      "密碼格式不正確，請輸入包含一個大寫英文、一個小寫英文以及數字，至少六個字元"
    );
    return;
  }

  function isValidUsername(username) {
    // 帳號格式驗證，只能是英文或數字，至少六個字元
    const usernamePattern = /^[A-Za-z0-9]{6,}$/;
    return usernamePattern.test(username);
  }

  function isValidPassword(password) {
    // 密碼格式驗證，包含一個大寫、一個小寫以及數字，至少六個字元
    const passwordPattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{6,}$/;
    return passwordPattern.test(password);
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
