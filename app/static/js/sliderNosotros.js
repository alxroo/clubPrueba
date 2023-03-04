////////Slider Training //////////////////////
(function(){
    const cards = document.querySelectorAll(".training__card");
    let cont=0;
    let ascDes=true;

    cards.forEach(card =>{
        card.addEventListener('click',()=>{
            removeClassActive();
            card.classList.add("active");
        })
    })

    function removeClassActive(){
        cards.forEach(card =>{
            card.classList.remove("active")
        })
    }
    function runCards(){
        removeClassActive();

        if(ascDes == true){
            cont++;
            if(cont == cards.length-1){
                ascDes = false;
            }
        }else{
            cont--;
            if(cont == 0){
                ascDes = true;
            }  
        }
        cards[cont].classList.add("active");
    }

    setInterval(()=>{
        runCards();
    },4000);

})();