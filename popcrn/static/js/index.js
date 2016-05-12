$(document).ready(function() {
  var btn = document.getElementById("btnSearch");
  btn.addEventListener("click", function() {
    var val = btn.value;
    console.log(val);
    if (val == null || val.trim() == "") {
      alert("Enter a valid query into the search box!");
    } else {
      console.log("Post request!");
      $.get("http://localhost:6543/raw_topic/?topic=" + val, function(response) {
        console.log("got a response");
        console.log(response);
      });
    }
  });
});
