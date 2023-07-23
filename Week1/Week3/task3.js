/* https://ithelp.ithome.com.tw/articles/10248113 */
async function getData() {
  const response = await fetch(
    "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
  );
  const data = await response.json();
  const results = data.result.results;

  /* //取出景點資料
  for (let i = 0; i < results.length; i++) {
    const stitle = results[i].stitle;
    console.log(stitle);
  } */

  /*  //取出網址資料
  for (let i = 0; i < results.length; i++) {
    const file = results[i].file;
    const image_links = file.toLowerCase().split(".jpg");
    const first_image_url = image_links[0] + ".jpg";
    console.log(first_image_url);
  } */

  /* 獲得所有P元素 */ /* 用來獲取文件中所有 <p> 標籤元素的集合 */
  const paragraphs = document.getElementsByTagName("p");
  /* 獲得圖片sunrise.jpg */
  const imageElements = document.querySelectorAll('img[src="sunrise.jpg"]');

  for (let i = 0; i < results.length; i++) {
    const stitle = results[i].stitle;
    /* 替換掉原本內容 */
    paragraphs[i].textContent = stitle;

    const file = results[i].file;
    const image_links = file.toLowerCase().split(".jpg");
    const first_image_url = image_links[0] + ".jpg";
    /* setAttribute(屬性名稱,要設定的值) */
    imageElements[i].setAttribute("src", first_image_url);
  }
}

getData();

/* ----------------------顯示更多按鈕------------------------------------ */
document.addEventListener("DOMContentLoaded", function () {
  /* class選擇器 */
  const contentContainer = document.querySelector(".content-main");
  /* ID選擇器 */
  const showMoreButton = document.getElementById("showMoreButton");

  /* 每次顯示的 main 元素數量 */
  let numMainElementsToShow = 12;
  /* 目前已顯示的 main 元素數量 */
  let currentMainElements = 15;

  /* 新增固定數量的 main 元素並更新內容 */
  async function addMoreMainElementsAndUpdateContent() {
    const response = await fetch(
      "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
    );
    const data = await response.json();
    const results = data.result.results;

    /* 取得 main 元素的範本 */
    const mainTemplate = document.querySelector(".main");

    /* 新增12個main元素 */
    for (
      let i = currentMainElements; //12
      i < currentMainElements + numMainElementsToShow; //12+15
      i++
    ) {
      if (i >= results.length) {
        /* 若已經沒有剩餘的 main 元素就隱藏按鈕 */
        showMoreButton.style.display = "none";
        /* 如果超出總資料數，則停止新增 */
        break;
      } else {
        /* 這個元素範本複製一份，並且複製其所有的子元素和內容，不僅僅是複製元素本身。 */
        const newMain = mainTemplate.cloneNode(true);
        contentContainer.appendChild(newMain);

        /* 更新內容 */
        const stitle = results[i].stitle;
        /* 選擇第一個出現的 <p> 標籤元素 */
        newMain.querySelector("p").textContent = stitle;

        /* 更新圖片 */
        const file = results[i].file;
        const image_links = file.toLowerCase().split(".jpg");
        const first_image_url = image_links[0] + ".jpg";
        newMain.querySelector(".img1").setAttribute("src", first_image_url);
      }
    }

    currentMainElements += numMainElementsToShow;
  }

  /* 按下按鈕後執行的函式 */
  function showMoreContent() {
    /* console.log("成功觸發"); */
    addMoreMainElementsAndUpdateContent();
  }

  /* 監聽按鈕點擊事件 */
  showMoreButton.addEventListener("click", showMoreContent);
});
