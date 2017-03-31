 $(document).ready(function() {
    var table = $('#fixed-mounting-table').DataTable();
    if (table) {
        table.column(3).visible(false);
        table.column(4).visible(false);
        table.column(6).visible(false);
        table.column(7).visible(false);
    }
    var table = $('#tentative-mounting-table').DataTable();
    if (table) {
        table.column(3).visible(false);
        table.column(4).visible(false);
        table.column(6).visible(false);
        table.column(7).visible(false);
    }
 })

// Before sorting quota column, replace quotas that are '-' or '?' or 'Unmounted' with negative numbers
function replaceNilQuotasWithNumbers(elementID){
    var table = $(elementID).DataTable();
    var data = table
        .rows()
        .data();
    
    column1Index = 3
    column2Index = 6
    if (elementID == '#modified-modules-quota-table') {
        column1Index = 2
        column2Index = 3
    }

    for (i=0; i<data.length; i++){
        if (data[i][column1Index].substring(0,1) == '-' || data[i][column1Index].substring(0,1) == 'U'){
            data[i][column1Index] = -2;
        } else if (data[i][column1Index].substring(0,1) == '?'){
            data[i][column1Index] = -1;
        }

        if (data[i][column2Index].substring(0,1) == '-' || data[i][column2Index].substring(0,1) == 'U'){
            data[i][column2Index] = -2;
        } else if (data[i][column2Index].substring(0,1) == '?'){
            data[i][column2Index] = -1;
        }
    }            
}

var quotaDisplay = false;
function toggleQuotaDisplay(elementID){
    var table = $(elementID).DataTable();
    table.column(3).visible(!quotaDisplay);
    table.column(6).visible(!quotaDisplay);
    quotaDisplay = !quotaDisplay;
    $(elementID).width("100%");
}

var numStudentsDisplay = false;
function toggleNumStudentsDisplay(elementID){
    var table = $(elementID).DataTable();
    table.column(4).visible(!numStudentsDisplay);
    table.column(7).visible(!numStudentsDisplay);
    numStudentsDisplay = !numStudentsDisplay;
    $(elementID).width("100%");
}