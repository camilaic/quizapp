var quizForm = document.querySelector('.quiz_form');

// remove the red box around the question that was not answered
function removeClass(element, className) {
    // check if the class contains the class name and if there is a match, remove it
    if (element.classList.contains(className)) {
        element.classList.remove(className);
    }
}

// add a listener to the form
quizForm.addEventListener('submit', function (event) {
    // not allow the default action - submit - to happen
    event.preventDefault();
    var formValid = true;

    // select all the questions
    var questionContainers = document.querySelectorAll('.question');

    // loop over the questions to get the answers
    for (var i = 0; i < questionContainers.length; i++) {
        var questionContainer = questionContainers[i];
        var answers = questionContainer.querySelectorAll('.answer');
        var currentQuestionAnswered = false;

        // loop over answers to check if checked is true or false
        for (var j = 0; j < answers.length; j++) {
            var answerSelected = answers[j].checked;

            // if checked is true, then modify currentQuestionAnswered to true
            if (answerSelected) {
                currentQuestionAnswered = true;
                // when the answerSelected is found, break the looping
                break;
            }
        }

        // if currentQuestionAnswered is not true then formValid is false
        if (!currentQuestionAnswered) {
            formValid = false;

            //adding a class
            questionContainer.classList.add('invalid_question');

        //remove the class by calling the function removeClass
        } else {
            removeClass(questionContainer, 'invalid_question');
        }
    }

    // if the form is valid, then submit the user's answers
    if (formValid) {
        quizForm.submit();
    }
});
