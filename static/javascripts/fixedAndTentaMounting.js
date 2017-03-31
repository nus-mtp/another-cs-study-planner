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

// Before sorting quota column, replace quotas that are '-' or '?' with negative numbers
function replaceNilQuotasWithNumbers(elementID){
    var table = $(elementID).DataTable();
    var data = table
        .rows()
        .data();
    
    for (i=0; i<data.length; i++){
        if (data[i][3] == '-'){
            data[i][3] = -2;
        } else if (data[i][3] == '?'){
            data[i][3] = -1;
        }

        if (data[i][6] == '-'){
            data[i][6] = -2;
        } else if (data[i][6] == '?'){
            data[i][6] = -1;
        }
    }            
}

var quotaDisplay = false;
function toggleQuotaDisplay(elementID){
    var table = $(elementID).DataTable();
    table.column(3).visible(!quotaDisplay);
    table.column(6).visible(!quotaDisplay);
    quotaDisplay = !quotaDisplay;
}

var numStudentsDisplay = false;
function toggleNumStudentsDisplay(elementID){
    var table = $(elementID).DataTable();
    table.column(4).visible(!numStudentsDisplay);
    table.column(7).visible(!numStudentsDisplay);
    numStudentsDisplay = !numStudentsDisplay;
}