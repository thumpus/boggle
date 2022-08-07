score = 0;
timeLeft = 60;
guessedWords = [];
$(document).ready(function(){
$("form").on("submit", function(event){
    event.preventDefault()
    $guess = $('#guess');
    checkWord($guess.val().toLowerCase())
    $guess.val('')
});

async function checkWord(word) {
    let response = await axios.get("/check", {params: {word}})
    console.log(response.data.result)
    if (response.data.result == "ok"){
        if (guessedWords.includes(word)){
            $('h2').text('Already guessed!')
        } else {
            $('h2').text('Valid word!')
            guessedWords.push(word)
            score = score + word.length
            $('h4').text(score)
        }
    } else if (response.data.result== "not-word"){
        $('h2').text('Invalid word!')
    } else if (response.data.result == "not-on-board"){
        $('h2').text("That word isn't on the board!")
    }
}
})

timer = setInterval(function() {
    if (timeLeft > 0){
        timeLeft--;
        $('h1').text(timeLeft)
    } else if (timeLeft === 0) {
        $('h1').text("GAME OVER!")
        $('h2').text('')
        $("form").remove()
        $("body").append(`<form action = "game">
        <input type = "submit" value = "New Game">
        </form>`)
        submitScores()
        clearInterval(timer)
    }
}, 1000)

async function submitScores(){
    let response = await axios.post("/submitscore", {params: {score}});
    highScore = response.data.highscore
    timesPlayed = response.data.timesplayed
    $("body").append(`<h5>
        High Score: ${highScore} 
        Times Played: ${timesPlayed}
        </h5>`)
}