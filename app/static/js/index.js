////Header Nav-Stick ////////////////////
(function(){
    window.addEventListener("scroll",function(){
        const nav = document.querySelector(".header__nav")
        nav.classList.toggle("inactive",window.scrollY > 0)
    })

})();

//// Boton Menu //////////////
(function(){
    const btnMenu = document.querySelector(".header__navicon");
    const boxMenu = document.querySelector(".header__navLinks");
    const btnStateMenu = document.querySelector(".header__navicon");


    btnMenu.addEventListener("click",()=>{
        boxMenu.classList.toggle("activeMenu")
    })
    btnStateMenu.addEventListener("click",()=>{
        const closeMenu = document.querySelectorAll(".header__navicon .icon");

        if(closeMenu[0].classList.contains("icon--active")){
            closeMenu[0].classList.remove("icon--active");
            closeMenu[1].classList.add("icon--active")
        }else{
            closeMenu[1].classList.remove("icon--active");
            closeMenu[0].classList.add("icon--active")
        }
    })
    
})();