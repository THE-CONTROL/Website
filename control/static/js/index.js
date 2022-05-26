const alertBtns = document.querySelectorAll(".alertBtn")
const sideBtn = document.getElementById("sideBtn")
const sideBar = document.querySelector(".sideBar")

alertBtns.forEach((alertBtn) => {
   alertBtn.addEventListener("click", (e) => {
       const flash = e.currentTarget.parentElement
       flash.style.display = "none" 
   }) 
});

sideBtn.addEventListener("click", () => {
    if (sideBar.style.display == "block") {
        sideBar.style.display = "none"
    }
    else {
        sideBar.style.display = "block"
    }
})
