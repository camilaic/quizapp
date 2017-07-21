var quizForm = document.querySelector('.quiz_form');
var number_questions;
var list_questions = [];

//remove the red box around the question that was not answered
function removeClass(element, className) {
    //check if the class contains the class name and if there is a match, remove it
    if (element.classList.contains(className)) {
        element.classList.remove(className);
    }
}

//check if the question already exists in the list
function addToList(item) {
    //getting the question_text from the node
    var questions_text = item[0].innerText;

    //if the question does not exist, add to the list_question
    //better indexOf() === -1, instead indexOf() < 0
    if (list_questions.indexOf(questions_text) === -1) {
        list_questions.push(questions_text);
    }
}
// add a listener to the form
quizForm.addEventListener('submit', function (event) {
    //not allow the default action - submit - to happen
    event.preventDefault();
    var formValid = true;

    //select all the questions
    var questionContainers = document.querySelectorAll('.question');
    number_questions = questionContainers.length;

    //loop over the questions to get the answers
    for (var i = 0; i < questionContainers.length; i++) {
        var questionContainer = questionContainers[i];

        //getting the questions
        var questionNode= questionContainer.querySelectorAll('.question_name');
        addToList(questionNode);

        //getting the answers
        var answers = questionContainer.querySelectorAll('.answer');
        var currentQuestionAnswered = false;

        //loop over answers to check if checked is true or false
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

            //if a div does nor contains the class name invalid_question, then add the class name
            if(!questionContainer.classList.contains('invalid_question')) {
                questionContainer.classList.add('invalid_question');
                console.log(questionContainer);
            }

        //remove the class by calling the function removeClass
        } else {
            removeClass(questionContainer, 'invalid_question');
        }
    }

    //get the elements from the form
    var form_elements = event.target.elements;
    var user_choices = [];
    //get the keys from the form that starts with question
    var question_keys = Object.keys(form_elements).filter(function(key) {
        return key.startsWith('question')
    });

    //looping and saving the user answer into the user_choices list
    //user_answer must match the user_answer field from serializer = UserAnswerSerializer
    question_keys.forEach(function(question_key) {
        user_choices.push({user_answer: form_elements[question_key].value});
    });

    //getting the cookie from csrf_token
    var csrf_token = Cookies.get('csrftoken');

    // if the form is valid, then submit the user's answers
    if (formValid) {
        fetch('/api/user_answers/', {
            headers: {
                'X-CSRFToken': csrf_token,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            //credentials displays the username
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
            displayScore(data, number_questions);
            displayAnswers(data, list_questions);
        });
    }
});


