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

/* 連接後端 */
/* https://ithelp.ithome.com.tw/articles/10252941 */
/* https://developer.mozilla.org/zh-TW/docs/Web/API/Fetch_API/Using_Fetch */
/* https://pjchender.dev/webapis/webapis-form-formdata/*/
function deleteMessage(messageId) {
  /* FormData為字典型態 */
  const formData = new FormData();
  formData.append("message_id", messageId);

  fetch("/deleteMessage", {
    method: "POST",
    body: formData,
  }).then(() => {
    /* 刪除完成時，及時更新畫面 */
    location.reload();
  });
}
