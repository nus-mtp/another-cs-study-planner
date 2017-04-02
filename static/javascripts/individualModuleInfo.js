window.onload = function () {
    studentYearBarChart = new CanvasJS.Chart("module-view-student-year-bar-chart",
    {
		animationEnabled: true,
		axisY: {
			title: "Number of Students",
			titleFontColor: "#161616",
			labelFontColor: "#161616",
			lineColor: "#161616"
		},
		axisX: {
			title: "Year of Study",
			titleFontColor: "#161616",
			labelFontColor: "#161616",
			lineColor: "#161616"
		},
		legend: {
			verticalAlign: "bottom",
			horizontalAlign: "center"
		},
		theme: "theme1",
		data: [{
					type: "column",
					dataPoints: year_of_study_bar_values
			  }]
	});

	studentYearBarChart.render();

	studentYearPieChart = new CanvasJS.Chart("module-view-student-year-pie-chart",
    {
		animationEnabled: true,
		legend: {
			verticalAlign: "center",
			horizontalAlign: "left"
		},
		data: [{
					type: "pie",
					indexLabelFontFamily: "Garamond",       
					indexLabelFontSize: 20,
					indexLabelFontWeight: "bold",
					startAngle:0,
					indexLabelFontColor: "#161616",       
					indexLabelLineColor: "#161616", 
					indexLabelPlacement: "outside",

					toolTipContent: "{name}:  {y} (#percent%)",
					showInLegend: false,
					indexLabel: "{name}:  {y} (#percent%)",
					dataPoints: year_of_study_pie_values
			  }]
	});

    focusAreaBarChart = new CanvasJS.Chart("module-view-focus-area-bar-chart",
    {
		animationEnabled: true,
		axisY: {
			title: "Number of Students",
			titleFontColor: "#161616",
			labelFontColor: "#161616",
			lineColor: "#161616"
		},
		axisX: {
			title: "Focus Area",
			titleFontColor: "#161616",
			labelFontColor: "#161616",
			lineColor: "#161616"
		},
		legend: {
			verticalAlign: "bottom",
			horizontalAlign: "center"
		},
		theme: "theme1",
		data: [{
					type: "column",
					dataPoints: focus_area_bar_values
			  }]
	});

	focusAreaBarChart.render();

	focusAreaPieChart = new CanvasJS.Chart("module-view-focus-area-pie-chart",
    {
		animationEnabled: true,
		legend: {
			verticalAlign: "center",
			horizontalAlign: "left"
		},
		data: [{
					type: "pie",
					indexLabelFontFamily: "Garamond",       
					indexLabelFontSize: 20,
					indexLabelFontWeight: "bold",
					startAngle:0,
					indexLabelFontColor: "#161616",       
					indexLabelLineColor: "#161616", 
					indexLabelPlacement: "outside",

					toolTipContent: "{name}: {y} (#percent%)",
					showInLegend: false,
					indexLabel: "{name}:  {y} (#percent%)", 
					dataPoints: focus_area_pie_values
			  }]
	});

	// Get the modal
	var modal = document.getElementById('myModal');
	// Get the button that opens the modal
	var edit_specific_info_btn = document.getElementById("edit-specific-info");
	var overlapping_mods_btn = document.getElementById("view-overlapping-with-module");
	var students_taking_btn = document.getElementById("view-students-planning-to-take-module");

	// When the user clicks the button, open the modal 
	edit_specific_info_btn.onclick = function() {
	  modal.style.display = "block";
	  document.getElementById("edit-specific-info-modal").style.display = "block";
	  document.getElementById("overlapping-mods-modal").style.display = "none";
	  document.getElementById("students-taking-modal").style.display = "none";
	}
	overlapping_mods_btn.onclick = function() {
	  modal.style.display = "block";
	  document.getElementById("edit-specific-info-modal").style.display = "none";
	  document.getElementById("overlapping-mods-modal").style.display = "block";
	  document.getElementById("students-taking-modal").style.display = "none";
	}
	students_taking_btn.onclick = function() {
	  modal.style.display = "block";
	  document.getElementById("edit-specific-info-modal").style.display = "none";
	  document.getElementById("overlapping-mods-modal").style.display = "none";
	  document.getElementById("students-taking-modal").style.display = "block";
	}

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
	  if (event.target == modal) {
	      modal.style.display = "none";
	  }
	}
}

// When the user clicks on <span> (x), close the modal
function closeModal() {
    document.getElementById('myModal').style.display = "none";
}

function showStudentYearBarChart() {
	document.getElementById('module-view-student-year-bar-chart').style.display = "block";
	document.getElementById('module-view-student-year-pie-chart').style.display = "none";
	document.getElementById('module-view-student-year-bar-chart-button').classList.add("active");
	document.getElementById('module-view-student-year-pie-chart-button').classList.remove("active");
	studentYearBarChart.render();
}

function showStudentYearPieChart() {
	document.getElementById('module-view-student-year-pie-chart').style.display = "block";
	document.getElementById('module-view-student-year-bar-chart').style.display = "none";
	document.getElementById('module-view-student-year-pie-chart-button').classList.add("active");
	document.getElementById('module-view-student-year-bar-chart-button').classList.remove("active");
	studentYearPieChart.render();
}

function showFocusAreaBarChart() {
	document.getElementById('module-view-focus-area-bar-chart').style.display = "block";
	document.getElementById('module-view-focus-area-pie-chart').style.display = "none";
	document.getElementById('module-view-focus-area-bar-chart-button').classList.add("active");
	document.getElementById('module-view-focus-area-pie-chart-button').classList.remove("active");
	focusAreaBarChart.render();
}

function showFocusAreaPieChart() {
	document.getElementById('module-view-focus-area-pie-chart').style.display = "block";
	document.getElementById('module-view-focus-area-bar-chart').style.display = "none";
	document.getElementById('module-view-focus-area-pie-chart-button').classList.add("active");
	document.getElementById('module-view-focus-area-bar-chart-button').classList.remove("active");
	focusAreaPieChart.render();
}