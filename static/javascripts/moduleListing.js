// functions for filtering tables in module listing page
  
  
// toggle the filters on and off
function toggleFilters() {
	var elements = document.getElementsByClassName("filter")
	if (elements[0].hasAttribute("hidden")) {
		document.getElementById("chevron").className="glyphicon glyphicon-chevron-up"
		for(var i=0; i < elements.length; i++) {
			elements[i].removeAttribute("hidden");
		}
	} else {
		document.getElementById("chevron").className="glyphicon glyphicon-chevron-down"
		for(var i=0; i < elements.length; i++) {
			elements[i].setAttribute("hidden", true);
                            elements[i].value = "";
		}
	}
}
				
// stop table from sorting when input field clicked
$(document).ready(function(){
	$("input").click(function(event){
		event.stopPropagation();
	});
});