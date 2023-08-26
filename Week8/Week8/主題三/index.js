/* 簡單請求，所以不會有CORS的問題 */
/* fetch(
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
)
  .then((response) => response.json())
  .then((data) => console.log(data));
 */

/* 簡單請求，所以不會有CORS的問題 */
async function response(url) {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "text/plain", // 使用 text/plain
      },
    });

    const data = await response.text(); // 使用 response.text() 方法
    console.log(data);
  } catch (error) {
    console.error("連接錯誤 :", error);
  }
}
response(
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
);

/* 非簡單請求 */
/* async function response(url) {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error("連接錯誤 :", error);
  }
}
response(
  "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
); */

// 伺服器沒有設置允許 http://localhost:8080 訪問的CORS 所以都會出現跨域問題
// 解決方法，請看app.py
/* async function response(url) {
  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error("連接錯誤 :", error);
  }
}
response("http://127.0.0.1:5000"); */
