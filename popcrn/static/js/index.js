$(document).ready(function() {
  var btn = document.getElementById("btnSearch");
  btn.addEventListener("click", function() {
    var val = btn.value;
    console.log(val);
    if (val == null || val.trim() == "") {
      alert("Enter a valid query into the search box!");
    } else {
      console.log("Post request!");
      $.post("http://localhost:6543/?topic=" + val, {"text":text}, function(data) {
				console.log(data);
                mapcreate(data);
			});

    }
  });
});
