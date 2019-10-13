console.log('index.js loaded.');

var button = document.getElementById("search");
button.addEventListener("click", function() {
  document.location.href = "/map";
});
