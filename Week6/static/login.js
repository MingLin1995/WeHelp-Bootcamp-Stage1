function registerCheck() {
  var name = document.forms["registerForm"]["name"].value;
  var username = document.forms["registerForm"]["username"].value;
  var password = document.forms["registerForm"]["password"].value;
  if (name == "" || username == "" || password == "") {
    alert("註冊欄位不得為空白");
    return false;
  }
}

function loginCheck() {
  var username = document.forms["loginForm"]["username"].value;
  var password = document.forms["loginForm"]["password"].value;
  if (username === "" || password === "") {
    alert("帳號或密碼不得為空白");
    return false;
  }
}
