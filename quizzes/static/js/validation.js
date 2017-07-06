// console.log('validation page');

var quizForm = document.querySelector('.quiz_form');

function removeClass(element, className) {
    if (element.classList.contains(className)) {
               element.classList.remove(className);
            }
}

quizForm.addEventListener('submit', function (event) {
    event.preventDefault();
    var formValid = true;

    // get all the questions
    var questionContainers = document.querySelectorAll('.question');

    // loop over the questions to the answers
    for (var i = 0; i < questionContainers.length; i++) {
        var questionContainer = questionContainers[i];
        var answers = questionContainer.querySelectorAll('.answer');
        var currentQuestionAnswered = false;

        // loop over answers to check if checked is true or false
        for (var j = 0; j < answers.length; j++ ) {
            var answerSelected = answers[j].checked;

            if (answerSelected) {
                currentQuestionAnswered = true;
            }
        }

        if (!currentQuestionAnswered) {
            formValid = false;

            questionContainer.classList.add('invalid_question');

        } else {
            removeClass(questionContainer, 'invalid_question');

        }
    }
    // console.log(formValid);
    if (formValid) {
        quizForm.submit();
    }
});

