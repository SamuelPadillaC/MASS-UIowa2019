console.log('index.js loaded.');

// search button
var button = document.getElementById("search");
// keyword input
var keyword = document.getElementById("keyword_input");


// button click event listener
button.addEventListener("click", function() {
  // error handling
  if (!keyword.value) {
    return alert('Please add a keyword value');
  }

  document.location.href = "/map?keyword=" + keyword.value;
});
