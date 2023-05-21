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

function changeColor_green() {
  document.body.style.backgroundColor = "#C7EDCC"; // set new background color
}

function changeColor_yellow() {
  document.body.style.backgroundColor = "#FAF9DE"; // set new background color
}

function changeColor_orange() {
  document.body.style.backgroundColor = "#FFF2E2"; // set new background color
}

function changeColor_red() {
  document.body.style.backgroundColor = "#FDE6E0"; // set new background color
}

function changeColor_blue() {
  document.body.style.backgroundColor = "#DCE2F1"; // set new background color
}

function changeColor_purple() {
  document.body.style.backgroundColor = "#E9EBFE"; // set new background color
}

function changeColor_grey() {
  document.body.style.backgroundColor = "#EAEAEF"; // set new background color
}

function changeColor_greenLight() {
  document.body.style.backgroundColor = "#FAF9DE"; // set new background color
}

function changeColor_white() {
  document.body.style.backgroundColor = "#FFFFFF"; // set new background color
}