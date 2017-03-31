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

        if (data[i][5] == '-'){
            data[i][5] = -2;
        } else if (data[i][5] == '?'){
            data[i][5] = -1;
        }
    }            
}