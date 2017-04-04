$(document).ready(function() {
    //Load the list of modules into the inputs of the search specific modules form
    $("input.prior-to-form-module-A").typeahead({
        minLength: 1,
        source: moduleSource,
        updater: function(selectedModule) {
            var selectedModuleCode = selectedModule.split(" ")[0];
			setTimeout(function() {
			    $("input.prior-to-form-module-A").val(selectedModuleCode);
			}, 200);
        }
    })
    $("input.prior-to-form-module-B").typeahead({
        minLength: 1,
        source: moduleSource,
        updater: function(selectedModule) {
            var selectedModuleCode = selectedModule.split(" ")[0];
			setTimeout(function() {
			    $("input.prior-to-form-module-B").val(selectedModuleCode);
			}, 200);
        }
    })

	// Get the modal
	var modal = document.getElementById('myModal');
	// Get the button that opens the modal
	var btn = document.getElementById('openModal');
	// Get the cross icon that closes the modal
	var cross = document.getElementsByClassName("closeModal")[0];

	// When the user clicks the button, open the modal 
	btn.onclick = function() {
	    modal.style.display = "block";
	}
	// When the user clicks on <span> (x), close the modal
	cross.onclick = function() {
	    modal.style.display = "none";
	}
	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	    if (event.target == modal) {
	        modal.style.display = "none";
	    }
	}
})