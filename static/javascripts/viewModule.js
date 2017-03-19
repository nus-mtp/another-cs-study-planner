window.onload = function () {
    var chart = new CanvasJS.Chart("quota-demand-chart",
    {
      animationEnabled: true,

      axisY:{
         lineColor: "#161616",
         labelFontColor: "#161616",
         title: "Number of Students",
         titleFontColor: "#161616" 
      },

      axisX:{
         lineColor: "#161616",
         labelFontColor: "#161616",
         labelFontSize: 18
      },

      legend: {
        cursor:"pointer",
        fontColor: "#161616",
        fontSize: 14,
        itemclick : function(e) {
			if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
				if (e.dataSeries.name == "Sem 1 Quota" || e.dataSeries.name == "Sem 1 Demand") {
					chart.options.data[0].visible = false;
					chart.options.data[1].visible = false;
				} else {
					chart.options.data[2].visible = false;
					chart.options.data[3].visible = false;					
				}
			} else {
				if (e.dataSeries.name == "Sem 1 Quota" || e.dataSeries.name == "Sem 1 Demand") {
					chart.options.data[0].visible = true;
					chart.options.data[1].visible = true;
				} else {
					chart.options.data[2].visible = true;
					chart.options.data[3].visible = true;					
				}
			}
          chart.render();
        }
      },

      data: [
      {        
        type: "bar",
        showInLegend: true,
        name: "Sem 1 Quota",
        color: "#BC141D",
        indexLabelFontColor: "#161616", 
        dataPoints: sem_1_quota
      },

      {        
        type: "bar",
        showInLegend: true,
        name: "Sem 1 Demand",
        color: "#ED31C4", 
        indexLabelFontColor: "#161616",      
        dataPoints: sem_1_demand
      },

      {        
        type: "bar",
        showInLegend: true,
        name: "Sem 2 Quota",
        color: "#366EC9",
        indexLabelFontColor: "#161616", 
        dataPoints: sem_2_quota   
      },

      {        
        type: "bar",
        showInLegend: true,
        name: "Sem 2 Demand",
        color: "skyblue",
        indexLabelFontColor: "#161616",      
        dataPoints: sem_2_demand
      },

      {        
        type: "bar",
        showInLegend: true,
        name: "",
        color: "white",
        indexLabelFontColor: "#161616",      
        dataPoints: filler
      }

      ]
    });

	chart.render();
}

function scrollToTenta(element, duration) {
	document.getElementById('editSpecificInfoWarning').style.display = "block";
	document.getElementById('editSpecificInfoWarning').style.color = "red";

	var startingY = window.pageYOffset;
	var elementY = getPosY(element);
	var diff = elementY - startingY;  
	var start;

	// Bootstrap our animation - it will get called right before next frame shall be rendered.
	window.requestAnimationFrame(function step(timestamp) {
		if (!start) start = timestamp
		// Elapsed miliseconds since start of scrolling.
		var time = timestamp - start
		// Get percent of completion in range [0, 1].
		var percent = Math.min(time / duration, 1)

		window.scrollTo(0, startingY + diff * percent)

		// Proceed with animation as long as we wanted it to.
		if (time < duration) {
			window.requestAnimationFrame(step)
		}
	});
}

function getPosY(element) {
	var bodyRect = document.body.getBoundingClientRect(),
    elemRect = document.getElementById(element).getBoundingClientRect(),
    offset = elemRect.top - bodyRect.top;
    return offset
}