/* 傳統型 */
function changeColor1() {
  const button = document.querySelector(".button");
  /* 切換樣式 */
  button.classList.toggle("change_color");
}

/* BEM */
function changeColor2() {
  const button = document.querySelector(".content_main_button");
  /* 切換樣式 */
  button.classList.toggle("content_main_button--switch");
}
