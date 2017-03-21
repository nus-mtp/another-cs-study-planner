window.onload = function () {
    studentYearBarChart = new CanvasJS.Chart("enrollment-student-year-bar-chart",
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

	studentYearPieChart = new CanvasJS.Chart("enrollment-student-year-pie-chart",
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

    focusAreaBarChart = new CanvasJS.Chart("enrollment-focus-area-bar-chart",
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

	focusAreaPieChart = new CanvasJS.Chart("enrollment-focus-area-pie-chart",
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
}

function showStudentYearBarChart() {
	document.getElementById('enrollment-student-year-bar-chart').style.display = "block";
	document.getElementById('enrollment-student-year-pie-chart').style.display = "none";
	document.getElementById('enrollment-student-year-bar-chart-button').classList.add("active");
	document.getElementById('enrollment-student-year-pie-chart-button').classList.remove("active");
	studentYearBarChart.render();
}

function showStudentYearPieChart() {
	document.getElementById('enrollment-student-year-pie-chart').style.display = "block";
	document.getElementById('enrollment-student-year-bar-chart').style.display = "none";
	document.getElementById('enrollment-student-year-pie-chart-button').classList.add("active");
	document.getElementById('enrollment-student-year-bar-chart-button').classList.remove("active");
	studentYearPieChart.render();
}

function showFocusAreaBarChart() {
	document.getElementById('enrollment-focus-area-bar-chart').style.display = "block";
	document.getElementById('enrollment-focus-area-pie-chart').style.display = "none";
	document.getElementById('enrollment-focus-area-bar-chart-button').classList.add("active");
	document.getElementById('enrollment-focus-area-pie-chart-button').classList.remove("active");
	focusAreaBarChart.render();
}

function showFocusAreaPieChart() {
	document.getElementById('enrollment-focus-area-pie-chart').style.display = "block";
	document.getElementById('enrollment-focus-area-bar-chart').style.display = "none";
	document.getElementById('enrollment-focus-area-pie-chart-button').classList.add("active");
	document.getElementById('enrollment-focus-area-bar-chart-button').classList.remove("active");
	focusAreaPieChart.render();
}