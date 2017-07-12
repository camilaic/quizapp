function getCorrectChoice() {
    var correctChoice = document.querySelectorAll('.correct_choice');
    for (var i = 0; i < correctChoice.length; i++) {
        var choice = correctChoice[i].innerHTML;
        // var answers = choice.querySelectorAll('.answer');
        // console.log('choice: ', choice, i);
        var correctChoiceSubstring = choice.substring(16);
    }
      return correctChoiceSubstring;
}


function getUserAnswer(){
    var userAnswer = document.querySelectorAll('.user_answer');
    for (var j = 0; j < userAnswer.length; j++) {
        var answer = userAnswer[j].innerHTML;
        var userAnswerSubstring = answer.substring(13);
        // list_user_answers.push(userAnswerSubstring)
    }
    return userAnswerSubstring;
}

if (getCorrectChoice() === getUserAnswer()) {
    // document.querySelector('.user_answer').style.color = "green";
}

else if (getCorrectChoice() !== getUserAnswer()) {
    // document.querySelector('.user_answer').style.color = "red";
}


// init();

