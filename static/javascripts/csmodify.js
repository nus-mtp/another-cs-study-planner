/****************************************************************/
/* =============== CS-MODIFY JAVASCRIPT FILE ================== */
/* This file serves as the central javascript source for all the*/
/* custom-defined animations or interactions on the page.       */
/****************************************************************/

/* VARIABLES USED FOR THE INTERFACE FOR EDITING MODULE PREREQUISITES */
var unitTemplate;
var addUnitConnector = '<tr><td colspan="12">and</td></tr>';
var addModuleTemplate;
var addModuleTemplateConnector = '<td>or</td>';

/* VARIABLES USED FOR THE INTERFACE FOR EDITING MODULE PRECLUSIONS */
var preclusionUnitTemplate;

/*
 * FUNCTIONS FOR SIDEBAR ANIMATIONS
 */

/* Set the width of the side navigation to 400px */
function openSidebar() {
    document.getElementById("sidebar").style.width = "400px";
}

/* Set the width of the side navigation to 0 */
function closeSidebar() {
    document.getElementById("sidebar").style.width = "0";
}

$(function () {
    $('[data-toggle="tooltip"]').tooltip();

    $('#sidebar-button').click(function(e) {
        e.stopPropagation();
        openSidebar();
    });

    $('body').click(function(e) {
        if (e.target.id != 'sidebar') {
            closeSidebar();
        }
    });

    unitTemplate = document.getElementById("prereq-unit-template");
    if (unitTemplate != null) {
        unitTemplate.removeAttribute("id");
    }

    addModuleTemplate = document.getElementById("module-template");
    if (addModuleTemplate != null) {
        addModuleTemplate.removeAttribute("id");
    }

    preclusionUnitTemplate = document.getElementById("preclusion-unit-template");
    if (preclusionUnitTemplate != null) {
        preclusionUnitTemplate.removeAttribute("id");
    }
})

/*
 * FUNCTIONS FOR SCROLLING TO TOP OF PAGE
 */

// Collapses the navbar on scroll
$(window).scroll(function() {
    try{
        if ($(".navbar").offset().top > 50) {
            $(".navbar-fixed-top").addClass("top-nav-collapse");
        } else {
            $(".navbar-fixed-top").removeClass("top-nav-collapse");
        }
    }catch(err){
        console.log(err.message, err.name);
    }
});

// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $($anchor.attr('href')).offset().top
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});

/*
 *   FUNCTION FOR SHOWING PROMPT WHEN USER CLICKS ON LOGOUT BUTTON
 */
 function confirmLogout() {
    toLogout = window.confirm("Are you sure you want to logout?");
    if (toLogout) {
        $.ajax({
            type: "POST",
            url: "/logout"
        }).done(function() {
            window.location = "/login";
        })
    }
 }

/*
 * FUNCTIONS FOR CUSTOM VALIDATION MESSAGES FOR LOGIN
 * AND REGISTRATION FORMS
 */
function check(input) {
    if (input.validity.patternMismatch) {
        input.setCustomValidity("User ID should be alphanumeric and within 9 characters.");
    } else if (input.validity.valueMissing) {
        input.setCustomValidity("Please fill in your User ID.");
    }
}

/*
 * FUNCTIONS USED FOR THE INTERFACE FOR EDITING MODULE PREREQUISITES
 */
function attachListenersToInputs(length) {
    $("input").on("input", function() {
        $("input").each(function() {
            var parentColumn = this.parentElement;
            if (length == 1) {
                parentColumn.style.backgroundColor = "#ffffff";
            } else if (length == 2) {
                parentColumn.style.backgroundColor = "#9bc2e4";
            }

            if (parentColumn.children.length != length) {
                parentColumn.removeChild(parentColumn.lastChild);
            }
        });
    });
}

function addModule(btn) {
    // Get the parent row, to add <td> elements to.
    var parentRow = btn.parentElement.parentElement;

    // Creates a table column <td>, which represents the 'OR'
    // module prerequisite unit.
    var moduleUnit = addModuleTemplate.cloneNode(true);

    // Creates another table column containing the word 'or',
    // as a 'connector' to the 'OR' unit.
    var moduleConnectorUnit = document.createElement("td");
    moduleConnectorUnit.innerHTML = addModuleTemplateConnector;

    // Hide the last 'OR'.
    moduleConnectorUnit.style.display = "none"
    
    // Add the module unit to the row.
    parentRow.appendChild(moduleUnit);
    parentRow.appendChild(moduleConnectorUnit);

    // Reveal the previous 'OR'.
    moduleUnit.previousElementSibling.style.display = "";

    // Re-initialize all tooltips to ensure that even newly added
    // HTML elements receive the tooltip event listener.
    $('[data-toggle="tooltip"]').tooltip();
}

function removeModule(btn) {
    // Gets the target column and the 'OR' column.
    var parentTd = btn.parentElement;
    var nextTd = parentTd.nextElementSibling;

    // Gets the row that the column belongs to.
    var parentRow = parentTd.parentElement;

    // Case 1: Prerequisite unit only contains 1 module.
    // (Options column + [Module column & 'OR' column])
    // Action: Drop the whole unit altogether, and
    // perform hiding + deletion of adjacent 'AND' rows.
    if (parentRow.children.length == 3) {
        // Retrieve the target row's delete button.
        var deleteUnitButton = btn.parentElement.parentElement.firstElementChild.children[1];

        // Call the delete-prerequisite-unit function with it.
        deletePrereqUnit(deleteUnitButton);
    }
    else {
        // Case 2: Module deleted from the end.
        // Action: after deletion of module unit,
        // hide the new last 'OR' column.
        if (parentRow.lastElementChild.previousElementSibling == parentTd) {
            // Hide the new last 'OR' column.
            parentTd.previousElementSibling.style.display = "none";

            // Delete the module unit with its accompanying 'OR' column.
            parentRow.removeChild(parentTd);
            parentRow.removeChild(nextTd);
        }
        else {
            // Delete the module unit with its accompanying 'OR' column.
            parentRow.removeChild(parentTd);
            parentRow.removeChild(nextTd);
        }
    }
}

function addPrereqUnit() {
    // Creates a table row <tr>, which represents the 'AND'
    // module prerequisite unit.
    var prereqUnit = unitTemplate.cloneNode(true);

    // Also create the row containing the 'AND'.
    var prereqUnitConnector = document.createElement("tr");
    prereqUnitConnector.innerHTML = addUnitConnector;
    prereqUnitConnector.children[0].style.display = "none";

    document.getElementsByTagName("tbody")[0].appendChild(prereqUnit);
    document.getElementsByTagName("tbody")[0].appendChild(prereqUnitConnector);

    // Reveal the 'AND' row (when there is more than 1 AND unit).
    if (prereqUnit.previousElementSibling != null) {
        prereqUnit.previousElementSibling.children[0].style.display = ""
    }

    // Creates a table column <td>, which represents the 'OR'
    // module prerequisite unit.
    var moduleUnit = addModuleTemplate.cloneNode(true);

    // Creates another table column containing the word 'or',
    // as a 'connector' to the 'OR' unit.
    var moduleConnectorUnit = document.createElement("td");
    moduleConnectorUnit.innerHTML = addModuleTemplateConnector;

    // Hide the last 'OR'.
    moduleConnectorUnit.style.display = "none"
    
    // Add the module unit to the row.
    prereqUnit.appendChild(moduleUnit);
    prereqUnit.appendChild(moduleConnectorUnit);

    // Re-initialize all tooltips to ensure that even newly added
    // HTML elements receive the tooltip event listener.
    $('[data-toggle="tooltip"]').tooltip();
}

function deletePrereqUnit(btn) {
    var parentTr = btn.parentElement.parentElement;
    var tableBody = parentTr.parentElement;

    // Case 1: Only 1 'AND' unit present.
    // Action: Delete whole unit.
    if (tableBody.children.length == 2) {
        tableBody.removeChild(parentTr.nextElementSibling);
        tableBody.removeChild(parentTr);
    }
    else {
        // Case 2: Last prerequisite unit is deleted.
        // Action: delete the last prerequisite unit,
        // and hide the 'AND' row.
        if (tableBody.lastElementChild.previousElementSibling == parentTr) {
            parentTr.previousElementSibling.children[0].style.display = "none";
            tableBody.removeChild(parentTr.nextElementSibling);
            tableBody.removeChild(parentTr);
        }
        else {
            tableBody.removeChild(parentTr.nextElementSibling);
            tableBody.removeChild(parentTr);
        }
    }
}

function saveChangesPrerequisite() {
    attachListenersToInputs(2);

    // Submit data to backend for updating the prerequisites for module.
    var modulePrerequisites = convertToDataPrerequisite();
    var modulePrereqsJSON = JSON.stringify(modulePrerequisites);

    // Retrieve the module code to pass to the handler backend.
    var moduleCode = document.getElementsByTagName("h1")[0].children[0].children[0].textContent;

    var toSave = window.confirm("Are you sure you want to save your changes?");
    if (toSave) {
        $.ajax({
            type: "POST",
            url: "/editModulePrerequisites",
            data: {
                'code': moduleCode,
                'prerequisites': modulePrereqsJSON,
            }
        }).success(function(data) {
            var parsedData = JSON.parse(data);
            if (parsedData[0] == true) {
                window.alert("Your changes have been saved.");
                if (window.opener != null) {
                    window.close();
                } else {
                    window.location.href = ("/editModule?code=" + moduleCode);
                }
            } else {
                highlightErrorFieldsPreclusion(parsedData[1]);
            }
        }).fail(function() {
            window.alert("There was an error processing your request.");
        })
    }
}

function convertToDataPrerequisite() {
    var prerequisites = [];
    // For iterating through units comprising of
    // [[Module-columns],[AND-column]]
    var rows = document.getElementsByTagName("tbody")[0].children;

    for (i = 0; i < rows.length; i+=2) {
        // Reads the prerequisite modules for each unit
        var modulesInUnit = [];
        var columns = rows[i].children;

        for (j = 1; j < columns.length; j+=2) {
            // Reads off the module code in the input fields for each unit.
            var moduleCode = columns[j].children[0].value;

            if (moduleCode != "") {
                modulesInUnit.push(columns[j].children[0].value);
            }
        }

        if (modulesInUnit.length != 0) {
            prerequisites.push(modulesInUnit);
        }
    }

    return prerequisites;
}

function revertChangesPrerequisite() {
    var toRevert = window.confirm("Are you sure you want to revert your changes?");
    if (toRevert) {
        var moduleCode = document.getElementsByTagName("h1")[0].children[0].children[0].textContent;
        window.location.href = ('/editModulePrerequisites?code=' + moduleCode);
    }
}

/*
 * FUNCTIONS USED FOR THE INTERFACE FOR EDITING MODULE PRECLUSIONS
 */
function addPreclusionModule(btn) {
    // Get the <tbody>, to add the <tr> elements to.
    var tableBody = document.getElementsByTagName("tbody")[0];

    // Creates the table row <tr>
    var preclusionModuleUnit = preclusionUnitTemplate.cloneNode(true);
    
    // Add the row to the table body
    tableBody.appendChild(preclusionModuleUnit);

    // Re-initialize all tooltips to ensure that even newly added
    // HTML elements receive the tooltip event listener.
    $('[data-toggle="tooltip"]').tooltip();
}

function removePreclusionModule(btn) {
    // Get the <tbody>, to add the <tr> elements to.
    var tableBody = document.getElementsByTagName("tbody")[0];

    // Gets the target row
    var parentRow = btn.parentElement.parentElement;

    // Remove target row from table body
    tableBody.removeChild(parentRow);
}

function saveChangesPreclusion() {
    attachListenersToInputs(1);

    // Submit data to backend for updating the preclusions for module.
    var modulePreclusions = convertToDataPreclusion();
    var modulePreclusionsJSON = JSON.stringify(modulePreclusions);

    var moduleCode = document.getElementsByTagName("h1")[0].children[0].children[0].textContent;

    var toSave = window.confirm("Are you sure you want to save your changes?");
    if (toSave) {
        $.ajax({
            type: "POST",
            url: "/editModulePreclusions",
            data: {
                'code': moduleCode,
                'preclusions': modulePreclusionsJSON,
            }
        }).success(function(data) {
            var parsedData = JSON.parse(data);
            if (parsedData[0] == true) {
                window.alert("Your changes have been saved.");
                if (window.opener != null) {
                    window.close();
                } else {
                    window.location.href = ("/editModule?code=" + moduleCode);
                }
            } else {
                highlightErrorFieldsPreclusion(parsedData[1]);
            }
        }).fail(function() {
            window.alert("There was an error processing your request.");
        })
    }
}

function convertToDataPreclusion() {
    var preclusions = [];

    // For iterating through all the preclusion modules
    var rows = document.getElementsByTagName("tbody")[0].children;

    for (i = 0; i < rows.length; i++) {
        var moduleInput = rows[i].children[1].children[0];

        if (moduleInput.value != "") {
            preclusions.push(moduleInput.value);
        }
    }

    return preclusions;
}

function revertChangesPreclusion() {
    var toRevert = window.confirm("Are you sure you want to revert your changes?");
    if (toRevert) {
        var moduleCode = document.getElementsByTagName("h1")[0].children[0].children[0].textContent;
        window.location.href = ('/editModulePreclusions?code=' + moduleCode);
    }
}

function highlightErrorFieldsPrerequisite(data) {
    var message_start = "<p><b>Message for ";
    var message_end = "</b></p>";

    var rows = document.getElementsByTagName("tbody")[0].children;

    for (i = 0; i < rows.length; i+=2) {
        // Reads the prerequisite modules for each unit
        var columns = rows[i].children;

        for (j = 1; j < columns.length; j+=2) {
            // Reads off the module code in the input fields for each unit.
            var targetColumn = columns[j];
            var moduleCode = columns[j].children[0].value;

            if (targetColumn.children.length != 2) {
                // Removal of message in preparation of adding a new message (if necessary)
                targetColumn.removeChild(targetColumn.lastChild);
            }

            if (moduleCode != "") {
                var messageElement = document.createElement("p");
                messageElement.innerHTML = (message_start + moduleCode + message_end);
                targetColumn.appendChild(messageElement);
                targetColumn.style.backgroundColor = "#d9534f";
            }
        }
    }
}

function highlightErrorFieldsPreclusion(data) {
    var modulesWithErrors = data;

    var rows = document.getElementsByTagName("tbody")[0].children;
    var message_start = "<p><b>";
    var message_end = "</b></p>";

    // Locates the element containing the module code,
    // and attaches a message there.
    for (i = 0; i < rows.length; i++) {
        var targetRow = rows[i];
        var moduleCodeColumn = targetRow.children[1];
        var moduleCode = moduleCodeColumn.children[0].value;

        for (k = 0; k < data.length; k++) {
            if (modulesWithErrors[k][0] == moduleCode) {
                var messageElement = document.createElement("p");
                messageElement.innerHTML = (message_start + modulesWithErrors[k][1] + message_end);
                moduleCodeColumn.appendChild(messageElement);
                moduleCodeColumn.style.backgroundColor = "#d9534f";
                break;
            }
        }
    }
}


/* ========== DOCUMENT-READY FUNCTIONS ========== */
$(document).ready(function() {
    /*
     * READY FUNCTION:FUNCTIONS FOR ENABLING SORTING FOR CERTAIN TABLES
     */

    /*
     * order: [column #, asc/desc],
     * where column # uses 0-based indexing
     * from left to right
    */
    $('#module-listing-table').DataTable( {
        "aaSorting": []
    } );

    $('#delete-module-table').DataTable( {
        "aaSorting": []
    } );

    $('#fixed-mounting-table').DataTable( {
        "aaSorting": []
    } );

    $('#tentative-mounting-table').DataTable( {
        "aaSorting": []
    } );

    $('#student-year-table').DataTable( {
        "aaSorting": [],
        "bPaginate": false,
        "searching": false
    } );

    $('#modified-modules-summary-table').DataTable( {
        "aaSorting": [ 0, "asc" ],
        "autoWidth": false,
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "35%" }
        ]
    } );

    $('#modified-modules-mounting-table').DataTable( {
        "aaSorting": [ 0, "asc" ],
        "autoWidth": false,
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "35%" }
        ]
    } );

    $('#modified-modules-quota-table').DataTable( {
        "aaSorting": [ 0, "asc" ],
        "autoWidth": false,
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "35%" },
            { "targets": [2, 3, 4], "width": "13%" }
        ]
    } );

    var modifiedModuleDetailsTable = $('#modified-modules-details-table').DataTable( {
        "aaSorting": [ 0, "asc" ],
        "autoWidth": false,
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "35%" },
        ]
    } );

    // Add event listener for opening and closing details
    $('#modified-modules-details-table tbody').on('click', 'td.details-control', function () {
        var cell_data = modifiedModuleDetailsTable.cell(this).data();
        var tr = $(this).closest('tr');
        var row = modifiedModuleDetailsTable.row( tr );
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            var formattedData = format(cell_data);
            if (formattedData != '') {
                // Open this row
                row.child(formattedData).show();
                tr.addClass('shown');
            }
        }
    } );

    $('#specific-modified-module').DataTable( {
        "autoWidth": false,
        "columnDefs": [
            { "targets": [0, 1], "width": "25%" }
        ]
    } );

    $('#student-focus-area-table').DataTable( {
        "aaSorting": [],
        "pageLength": 25,
        "bPaginate": false,
        "searching": false
    } );

    $('#oversubscribed-modules-table').DataTable( {
        "order": [[ 4, "desc" ]],
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "35%" }
        ]
    } );

    $('#modules-taken-prior-table').DataTable( {
        "order": [[ 6, "desc" ], [ 0, "asc" ], [ 3, "asc" ]],
        "columnDefs": [
            { "targets": [0, 3], "width": "8%" },
            { "targets": [1, 4], "width": "20%" },
            { "targets": 6, "width": "20%" }
        ]
    } );

    $('#modules-taken-prior-intern-table').DataTable( {
        "order": [[ 2, "desc" ]],
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "60%" },
        ]
    } );
     
    $('#common-module-table').DataTable( {
        "aaSorting": []
    } );

    $('#non-overlap-table').DataTable( {
        "aaSorting": [],
        "deferRender": true
    } );
     
    $('#students-taking-module-table').DataTable({
       aaSorting: [],
        "deferRender": true
    });

    $('#mod-specific-size-table').DataTable( {
        "order": [[ 2, "asc"]]
    } );
});

function format(data) {
    var split = data.split("<!--p>");
    if (split.length > 1) {
        var d1 = split[1].trim();
        var d2 = split[2].split("</p-->")[0];

        var originalDescription = d1.substring(0, d1.length - 6);
        var modifiedDescription = d2;

        return '<div class="row">' +
               '<div class="col-md-5 text-justify">' +
               '<b>From</b><br>' +
               '<i>' + originalDescription + '</i>' +
               '</div>' +
               '<div class="col-md-2">' +
               '<h3>&#8594;</h3>' +
               '</div>' +
               '<div class="col-md-5 text-justify">' +
               '<b>To</b><br>' +
               '<i>' + modifiedDescription + '</i><br><br>' +
               '</div>' +
               '</div>';
    } else {
        return '';
    }    
}