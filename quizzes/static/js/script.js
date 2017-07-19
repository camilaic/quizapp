//remove form from the html
function removeForm() {
    document.querySelector('.quiz_form').remove();
}

//display div and the score
function displayScore(data, numberQuestions) {
    var json_parse = JSON.parse(data);
    var get_user_score = json_parse["score_correct"];

    var getDiv = document.querySelector('.overall_score');
    getDiv.style.display = 'block';

    var pluralizeWord = function () {
        if(numberQuestions > 1) {
            return 'Overall Score: ' + get_user_score + ' of ' + numberQuestions + ' questions';
            // return `Overall Score: ${text[1]} of ${numberQuestions} questions`;
        }
        else {
            return 'Overall Score: ' + get_user_score + ' of ' + numberQuestions + ' question';
        }
    };

    getDiv.innerHTML = pluralizeWord();
}

//displaying the results
function displayAnswers(data, list_questions) {
    var color_paragraph;

    //parsing the data to a JSON
    var json_parse = JSON.parse(data);
    //getting correct choices
    var get_correct_choices = json_parse["correct_choice"];
    //getting user_answers
    var get_user_answers = json_parse["user_answers"];

    //looping through the list_questions to get the question
    for (var i = 0; i < list_questions.length; i++) {
        var question = list_questions[i];

        //getting the correct_answer and user_answer for each question
        var correct_answer = get_correct_choices[question];
        var user_answer = get_user_answers[question];

        // if the user answer is correct, the color is green, otherwise it will be red
        if (user_answer === correct_answer) {
            color_paragraph = "green"
        } else {
            color_paragraph = "red"
        }

        getElement(question, 'black', "question_paragraph");
        getElement('Correct Answer: '  + correct_answer, 'black', "result");
        getElement('User Answer: ' + user_answer, color_paragraph, "result");
    }
}

//getting the div to display the results
function getElement(textToDisplay, colorToChange, addClassName) {
    //displaying the div
    var getDiv = document.querySelector('.div_result');
    getDiv.style.display = "block";

    //creating a paragraph element
    var myContent = document.createElement("p");
    //adding class name to be able to use in the css file
    myContent.className = addClassName;

    //setting the color if the user answer is correct or not
    myContent.style.color = colorToChange;

    //appending the text to display the results
    myContent.appendChild(document.createTextNode(textToDisplay));
    getDiv.appendChild(myContent);
}
