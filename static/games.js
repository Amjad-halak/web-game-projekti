"use strict"

function setupDifficultyButtons (){
const diffButtons = document.querySelectorAll(`.diff-btn`)


for (const btn of diffButtons){
    btn.addEventListener("click" , function (){
        console.log(btn.dataset.diff)
        const group = btn.parentElement
        const groupButtons = group.querySelectorAll(".diff-btn")
    for(const button of groupButtons){
        button.classList.remove("active")
}
    btn.classList.add("active")
        
    });
}
} 
setupDifficultyButtons();

function setupstartButton (){
    const startButton = document.querySelectorAll(".start-btn")
    for (const btn of startButton){
        btn.addEventListener("click" , function (){
            const card = btn.closest(".game-card")
            const activeDiffBtn = card.querySelector(".diff-btn.active")
            const difficulty = activeDiffBtn.dataset.diff
            console.log(card.dataset.game , difficulty)
    localStorage.setItem("selectedGame", card.dataset.game);
        localStorage.setItem("selectedDifficulty", difficulty);
             window.location.href = "amjadGame.html";
        })
    }
}
setupstartButton();