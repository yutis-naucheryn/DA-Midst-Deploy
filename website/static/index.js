function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/space";
    });
}

function editNote(event) {
  //retrieves the note id from the button's data attribute
  const noteId = event.target.dataset.id;

  //navigates to the edit-note route, passing the note id as a parameter in the URL.
  window.location.href = "/space/edit-note/" + noteId;
  
}  

function updateNote(noteId){
  var updatedNote = document.getElementById("note").value;
  fetch("/update-note", {
    method: "POST",
    //passing both noteId and updatedNote to Python
    body: JSON.stringify({ noteId: noteId, note: updatedNote }),
    headers: {
      'Content-Type':'application/json'
    }
  }).then((_res) => {
    window.location.href = "/all-journal";
  });
}

function printNote(){
  print('All journals') //can print as pdf if put print here
}

function chat(){

  //navigates to the edit-note route, passing the note id as a parameter in the URL.
  window.location.href = "/home/chat";
  
}  

function dass21(){

  //navigates to the edit-note route, passing the note id as a parameter in the URL.
  window.location.href = "/moodtrack/dass-21";
  
}  

function dass21_result(){

  //navigates to the edit-note route, passing the note id as a parameter in the URL.
  window.location.href = "/moodtrack/dass-21/result";
  
}  

function personal_space(){

  //navigates to the edit-note route, passing the note id as a parameter in the URL.
  window.location.href = "/space";
  
}  

function all_journal(){

  window.location.href = "/all-journal";
}

function tic_tac_toe(){

  window.location.href = "/game/tic-tac-toe";
}

// Retrieve the color from localStorage on page load
window.addEventListener("DOMContentLoaded", function() {
  var storedColor = localStorage.getItem("backgroundColor");
  if (storedColor) {
    document.body.style.backgroundColor = storedColor;
  }
});

function changeColor_green() {
  var color = "#C7EDCC"; // set new background color

  // Store the color in localStorage
  localStorage.setItem("backgroundColor", color);

  // Change the background color
  document.body.style.backgroundColor = color;
}

function changeColor_yellow() {
  var color = "#FAF9DE"; // set new background color

  // Store the color in localStorage
  localStorage.setItem("backgroundColor", color);

  // Change the background color
  document.body.style.backgroundColor = color;
}

function changeColor_orange() {
  var color = "#FFF2E2"; // set new background color

  // Store the color in localStorage
  localStorage.setItem("backgroundColor", color);

  // Change the background color
  document.body.style.backgroundColor = color;
}

function changeColor_red() {
  var color = "#FDE6E0"; // set new background color

  // Store the color in localStorage
  localStorage.setItem("backgroundColor", color);

  // Change the background color
  document.body.style.backgroundColor = color;
}

function changeColor_blue() {
  var color = "#DCE2F1"; // set new background color

  // Store the color in localStorage
  localStorage.setItem("backgroundColor", color);

  // Change the background color
  document.body.style.backgroundColor = color;
}

function changeColor_purple() {
  var color = "#E9EBFE"; // set new background color

  // Store the color in localStorage
  localStorage.setItem("backgroundColor", color);

  // Change the background color
  document.body.style.backgroundColor = color;
}

function changeColor_grey() {
  var color = "#EAEAEF"; // set new background color

  // Store the color in localStorage
  localStorage.setItem("backgroundColor", color);

  // Change the background color
  document.body.style.backgroundColor = color;
}

function changeColor_greenLight() {
  var color = "#FAF9DE"; // set new background color

  // Store the color in localStorage
  localStorage.setItem("backgroundColor", color);

  // Change the background color
  document.body.style.backgroundColor = color;
}

function changeColor_white() {
  var color = "#FFFFFF"; // set new background color

  // Store the color in localStorage
  localStorage.setItem("backgroundColor", color);

  // Change the background color
  document.body.style.backgroundColor = color;
}