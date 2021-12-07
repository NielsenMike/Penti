$(document).ready(function(){
  id = document.getElementById('question_id').value
  $("#check_answer0").click(function(){
    var value = document.getElementById("check_answer0").innerHTML;
    $.post('/check_answer', {question_id:parseInt(id), answer:value});
  });
  $("#check_answer1").click(function(){
    var value = document.getElementById("check_answer1").innerHTML;
    $.post('/check_answer', {question_id:parseInt(id), answer:value});
  });
  $("#check_answer2").click(function(){
    var value = document.getElementById("check_answer2").innerHTML;
    $.post('/check_answer', {question_id:parseInt(id), answer:value});
  });
  $("#check_answer3").click(function(){
    var value = document.getElementById("check_answer3").innerHTML;
    $.post('/check_answer', {question_id:parseInt(id), answer:value});
  });
});