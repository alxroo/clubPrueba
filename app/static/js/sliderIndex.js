//// Slider ///////////////////////////
(function(){
    const imgs = document.querySelectorAll(".hero__img")
    const btnleft = document.querySelector(".hero__btn--left");
    const btnRight = document.querySelector(".hero__btn--right");

    let cont = 0;

    function opacity(){
        imgs.forEach((img)=>{
            img.classList.remove("active")
        })
    }

    
    function Next(){
        cont++;
        opacity();
        if(cont >= imgs.length){
            cont=0;
        }
        imgs[cont].classList.add("active");
    }
    function Prev(){
        cont--;
        opacity();
        if(cont<0){
            cont=imgs.length-1;
        }
        imgs[cont].classList.add("active");
    }

    imgs[0].classList.add("active");
    btnRight.addEventListener("click",()=>{
        Next();
    })
    btnleft.addEventListener("click",()=>{
        Prev();
    })
    
    setInterval(()=>{
        Next();
    },4000);


})();