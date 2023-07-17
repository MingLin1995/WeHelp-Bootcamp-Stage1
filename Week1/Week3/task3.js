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

  const paragraphs = document.getElementsByTagName("p"); //獲得所有P元素
  for (let i = 0; i < results.length; i++) {
    const stitle = results[i].stitle;
    if (paragraphs[i]) {
      paragraphs[i].textContent = stitle; // 更新對應的內容
    }
  }

  /*  //取出網址資料
  for (let i = 0; i < results.length; i++) {
    const file = results[i].file;
    const image_links = file.toLowerCase().split(".jpg");
    const first_image_url = image_links[0] + ".jpg";
    console.log(first_image_url);
  } */

  const imageElements = document.querySelectorAll('img[src="sunrise.jpg"]');

  for (let i = 0; i < results.length; i++) {
    const file = results[i].file;
    const image_links = file.toLowerCase().split(".jpg");
    const first_image_url = image_links[0] + ".jpg";

    if (imageElements[i]) {
      imageElements[i].setAttribute("src", first_image_url); // 替换图片链接
    }
  }
}

getData();
