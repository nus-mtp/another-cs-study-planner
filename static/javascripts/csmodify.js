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

function saveChanges() {
    // Submit data to backend for updating the prerequisites for module.
    var modulePrerequisites = convertToData();
    var modulePrereqsJSON = JSON.stringify(modulePrerequisites);
    console.log(modulePrereqsJSON);

    // Retrieve the module code to pass to the handler backend.
    moduleCode = document.getElementsByTagName("h1")[0].children[0].children[0].textContent;

    toSave = window.confirm("Are you sure you want to save your changes?");
    if (toSave) {
        $.ajax({
            type: "POST",
            url: "/editModulePrerequisites",
            data: {
                'code': moduleCode,
                'prerequisites': modulePrereqsJSON,
            }
        }).success(function(isUpdated) {
            console.log(isUpdated);
            if (isUpdated == 'True') {
                window.alert("Your changes have been saved.");
                if (window.opener != null) {
                    window.close();
                } else {
                    window.location.href = ("/editModule?code=" + moduleCode);
                }
            } else {
                window.alert("There are invalid modules in your prerequisites. Please check if all the modules specified in the prerequistes are valid.");
            }
        }).fail(function() {
            window.alert("There was an error processing your request.");
        })
    }
}

function convertToData() {
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

    $('#modified-modules-details-table').DataTable( {
        "aaSorting": [ 0, "asc" ],
        "autoWidth": false,
        "columnDefs": [
            { "targets": 0, "width": "15%" },
            { "targets": 1, "width": "35%" },
        ]
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