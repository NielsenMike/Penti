$(document).ready(function(){
  var answered = false
  $("#check_answer0").click(function(){
    if(!answered) {
      postData("check_answer0_card", "check_answer0_text", "question_id")
      answered = true
    }
  });
  $("#check_answer1").click(function(){
    if(!answered) {
      postData("check_answer1_card", "check_answer1_text", "question_id")
      answered = true
    }
  });
  $("#check_answer2").click(function(){
    if(!answered) {
      postData("check_answer2_card", "check_answer2_text", "question_id")
      answered = true
    }
  });
  $("#check_answer3").click(function(){
    if(!answered) {
      postData("check_answer3_card", "check_answer3_text", "question_id")
      answered = true
    }
  });

  function postData(answer_card , answer_text, question_id){
    var id = document.getElementById(question_id).value
    var value = document.getElementById(answer_text).innerHTML;
    $.post('/check_answer', {question_id: parseInt(id), answer:value})
    .done(function( data ) {
        evaluateAnswer(data, answer_card)
    });
  }

  function evaluateAnswer(data, answer_card) {
    const jdata = JSON.parse(data);
    var element = document.getElementById(answer_card);
    if (jdata.correct){
      element.classList.add("text-white");
      element.classList.add("bg-success");
      element.classList.add("mb-3");
    }
    else{
      element.classList.add("text-white");
      element.classList.add("bg-danger");
      element.classList.add("mb-3");
    }
    setTimeout(function(){ window.location.reload(1);}, 5000);
  }
});