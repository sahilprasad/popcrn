$(document).ready(function() {
  var btn = document.getElementById("btnSearch");
  var search = document.getElementById("txtSearch");
  btn.addEventListener("click", function() {
    var val = search.value;
    console.log(val);
    if (val == null || val.trim() == "") {
      alert("Enter a valid query into the search box!");
    } else {
      console.log("Post request!");
      $.post("http://localhost:6543/?topic=" + val, function(data) {
				console.log(data);
                mapcreate(data);
			});

    }
  });
});
