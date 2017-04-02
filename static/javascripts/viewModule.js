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

  // Get the modal
  var modal = document.getElementById('myModal');
  // Get the button that opens the modal
  var edit_specific_info_btn = document.getElementById("edit-specific-info");
  var overlapping_mods_btn = document.getElementById("view-mods-overlapping");

  // When the user clicks the button, open the modal 
  edit_specific_info_btn.onclick = function() {
      modal.style.display = "block";
      document.getElementById("edit-specific-info-modal").style.display = "block";
      document.getElementById("overlapping-mods-modal").style.display = "none";
  }
  overlapping_mods_btn.onclick = function() {
      modal.style.display = "block";
      document.getElementById("edit-specific-info-modal").style.display = "none";
      document.getElementById("overlapping-mods-modal").style.display = "block";
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
