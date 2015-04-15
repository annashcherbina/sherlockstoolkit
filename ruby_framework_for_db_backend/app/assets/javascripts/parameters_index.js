//creates a data table with multi column filtering via a dropdown menu
function setParameterDataTable(){
    var parameterTable = $('.parameterTable');
    if (parameterTable.length == 0){
        return;
    }

    //sets up the specialized table with no lengthChange option, with each page showing a complete set
    var table = parameterTable.DataTable(
        {
            iDisplayLength: gon.unique_param_names,
            bLengthChange: false
        }
    );

    //each footer th cell that has class 'filter' will have a dropdown filter
    $(".parameterTable tfoot th.filter").each( function (i) {
        var select = $('<select><option value="">No Filter</option></select>')
            .appendTo($(this).empty())
            .on('change', function () {
                if ($(this).val() == '') {
                    table.column(i).search('.*').draw();
                } else {
                    table.column(i)
                        .search('^' + $(this).val() + '$', true, false)
                        .draw();
                }
            });

        //populating that dropdown menu
        table.column(i).data().unique().sort().each(function (d) {
            select.append('<option value="' + d + '">' + d + '</option>');
        });
    } );
}

$(function(){
    setParameterDataTable();
});