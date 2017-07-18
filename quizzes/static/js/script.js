

// remove form from the html
function removeForm() {
    document.querySelector('.quiz_form').remove();
}

//display div and the score
function addScore(data, numberQuestions) {
    var json_parse = JSON.parse(data);
    var get_user_score = json_parse["score_correct"];

    var getDiv = document.querySelector('.overall_score');
    getDiv.style.display = 'inline';

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

function displayAnswers(data, list_questions) {
    var json_parse = JSON.parse(data);
    var get_user_answers = json_parse["user_answers"];
    var get_correct_choices = json_parse["correct_choice"];



    for (var i = 0; i < list_questions.length; i++) {
        var question = list_questions[i];
        console.log(question);
    }


    var getDiv = document.querySelector('.user_answer_result');
    getDiv.style.display = 'inline';
    getDiv.innerHTML = 'Hello testing';


    // var getParagraph = document.querySelector('.correct_choice_result');
    // getParagraph.style.display = 'inline';
    //
    // // // select all the questions
    // questionContainers = document.querySelectorAll('.question');
    // console.log(questionContainers);
    // // number_questions = questionContainers.length;
    //
    // // loop over the questions to get the answers
    // for (var i = 0; i < questionContainers.length; i++) {
    //     var questionContainer = questionContainers[i];
    //     var questions = questionContainer.querySelectorAll('.question_name');
    //     console.log("Questions: " + questions);
    //
    //     for (var j = 0; j < questions.length; j++) {
    //          var question = questions[j];
    //          console.log(question);
    //     }
    // }

}



