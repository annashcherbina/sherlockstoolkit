// This is a manifest file that'll be compiled into application.js, which will include all the files
// listed below.
//
// Any JavaScript/Coffee file within this directory, lib/assets/javascripts, vendor/assets/javascripts,
// or vendor/assets/javascripts of plugins, if any, can be referenced here using a relative path.
//
// Read Sprockets README (https://github.com/sstephenson/sprockets#sprockets-directives) for details
// about supported directives.
//
//= require jquery
//= require jquery_ujs
//= require jquery-ui
//= require local_time
//= require dataTables/jquery.dataTables

var oTable;
//creates the data table
function setDataTable(){
    oTable = $('.dataTable:not(.parameterTable)').DataTable({
        bPaginate: true,
        sPaginationType: "full_numbers",
        iDisplayLength: 25,
        aLengthMenu: [25, 50, 100, 1000],
        'drawCallback': swapTextInit
    });
}

//allows pagination checkboxes submissions on data tables
function dataTablePaginatedForm(){
    $('form.paginated_checkbox_datatable_form').submit( function() {
        oTable.$('input:checked').each( function (index, element) {
            var currentInput = $(element);

            var input = $("<input>")
                .attr("type", "hidden")
                .attr("name", currentInput.attr("name"))
                .val(currentInput.val());

            $('form').append($(input));
        });

        return true;
    } );
}

function shortenDescription(str){
    var lines = str.split("<br>");
    if (lines.length <= 5){
        return str;
    }else{
        return lines.slice(0,3).join("<br>")+"<br>...";
    }
}

//for images and attachments index page, shortens the descriptions and expands if clicked
function swapTextInit(){
    $('td.swap').click(function() {
        var target = $(this).find('div');

        //removes the swap class and css styling from short descriptions
        if ($(target).data('textorig').split("<br>").length <= 5){
            $(this).removeClass('swap');
        }

        //toggles the shown text
        if ($(target).hasClass('originalText')) {
            $(target).html($(target).data('textorig'));
        }else{
            $(target).html(shortenDescription($(target).data('textorig')));
        }

        $(target).toggleClass('originalText');
    }).click();
}

//on load functions
$(function () {
    setDataTable();
    dataTablePaginatedForm();
});