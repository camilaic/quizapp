var quizForm = document.querySelector('.quiz_form');
var number_questions;
var list_questions = [];

// remove the red box around the question that was not answered
function removeClass(element, className) {
    // check if the class contains the class name and if there is a match, remove it
    if (element.classList.contains(className)) {
        element.classList.remove(className);
    }
}

function saveQuestions(element) {

}

// add a listener to the form
quizForm.addEventListener('submit', function (event) {
    // not allow the default action - submit - to happen
    event.preventDefault();
    var formValid = true;

    // select all the questions
    var questionContainers = document.querySelectorAll('.question');
    number_questions = questionContainers.length;

    // loop over the questions to get the answers
    for (var i = 0; i < questionContainers.length; i++) {
        var questionContainer = questionContainers[i];

        var questions = questionContainer.querySelectorAll('.question_name');
        // list_questions.push(questionContainer.querySelectorAll('.question_name'));

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

    //get the elements from the form
    var form_elements = event.target.elements;
    var user_choices = [];
    // get the keys from the form that starts with question
    var question_keys = Object.keys(form_elements).filter(function(key) {return key.startsWith('question')});
    //looping and saving the user answer into the user_choices list
    //user_answer must match the user_answer field from serializer = UserAnswerSerializer
    question_keys.forEach(function(question_key) {
        user_choices.push({user_answer: form_elements[question_key].value});

    });

    //getting the cookie from csrf_token
    var csrf_token = Cookies.get('csrftoken');

    // if the form is valid, then submit the user's answers
    if (formValid) {
        fetch('/api/results/', {
            headers: {
                'X-CSRFToken': csrf_token,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            // credentials displays the username
            credentials: 'include',
            method: 'POST',
            // send the user_choices list as json
            body: JSON.stringify(user_choices)
        }).then(function(response) {
            if(response.ok) {
                removeForm();
            }
            return response.text()
        }).then(function(data) {
            addScore(data, number_questions);
            displayAnswers(data, list_questions);
        });
    }
});


