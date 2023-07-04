function openNav() {
    document.getElementById("mySidepanel").style.width = "150px"; /* 點擊後，展開的寬度(就會顯示) */
    document.getElementsByClassName("closebtn")[0].style.display = "block"; /* [0]代表第一個元素 */

  }
  
  function closeNav() {
    document.getElementById("mySidepanel").style.width = "0"; /* 關閉後，寬度為0(就不會顯示) */
    document.getElementsByClassName("closebtn")[0].style.display = "none";
  }



  
  