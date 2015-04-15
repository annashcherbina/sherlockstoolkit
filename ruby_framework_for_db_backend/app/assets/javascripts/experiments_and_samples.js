//sets jQuery UI tabs
function initTabs(){
    $("#tabs").tabs();
}

//clicking in a td element toggles the checkbox
function tdClick(){
    $("td").click(function(event) {
        if(event.target.type != 'checkbox' && event.target.tagName != 'SELECT') {
            var checkbox = $(':checkbox', this);
            checkbox.prop('checked', !checkbox.prop('checked'));
        }
    });
}

//when the parameter group dropdown menu is changed, it triggers the displayed parameters to be changed as well
function dynamicParameterGroupSelectionInit(){
    var ownerSelect = $('.ownerSelect');
    var groupSelect = $('.groupSelect');
    var displayedParams = $('.paramName');

    //assigns a change function to the ownerSelect dropdowns
    ownerSelect.change(
        function(){
            //changing all the owner dropdowns to be synched up
            var selectedOwner = $(this).val();
            ownerSelect.val(selectedOwner);
            //getting the array of groups that belong to said owner
            var arrayGroups = Object.keys(gon.parameters[selectedOwner]);

            //sets each of the group selects to have new values based off of what was chosen for the user
            groupSelect.empty();
            $(arrayGroups).each(function(index, value){
                groupSelect.append($('<option></option>').attr('value', value).text(value));
            });

            //group select changes to the new value
            groupSelect.change();
        }
    ).change();

    //assigns a change function to the groupSelect dropdowns
    groupSelect.change(
        function(){
            var selectedOwner = ownerSelect.val();
            var selectedGroup = $(this).val();
            //changing all the group dropdowns to be synched up
            groupSelect.val(selectedGroup);

            //changing the displayed values on the td cells to be synched up
            $(displayedParams).each(function(){
                var paramName = $(this)[0].innerHTML;
                $(this).next()[0].firstElementChild.innerHTML = gon.parameters[selectedOwner][selectedGroup][paramName];
                $(this).next()[0].lastElementChild.value = gon.parameters[selectedOwner][selectedGroup][paramName];
            });
        }
    );
}


//applies the quality function match to the reference quality dropdown
function qualityDropdownInit(){
    $('select#Reference_Quality, select#Sample_Quality').change(function(){
        displayOnlyMatchingQ($(this).val());
    }).change();
}

//toggles the sample cells that are at the proper quality level
function displayOnlyMatchingQ(qVal){
    //unchecks all checked checkboxes
    $('td.sample_cell :checkbox').prop('checked', false);

    $('table.samples_table tr td.sample_cell').each(function() {
        if ($(this).hasClass("qual"+qVal)) {
            $(this).show();
        } else {
            $(this).hide();
        }
    });
}

//resets all the entries on this form
function resetFormButtonInit(){
    $('.resetFormButton').click(function(){
        $(':checkbox').attr('checked', false);
        $('.parameterEntry').val('');
        $('.groupEntry').val('');
        $('.ownerSelect').val('SYSTEM').change();
        $('select#Reference_Quality').val(0).change();
    });
}


//selects the best samples of each visible row
function selectBestSamplesButtonInit(){
    $('.selectBestSamplesButton').click(function(){
        var target = $(this).attr('data-target');
        var quality = $('#Reference_Quality, #Sample_Quality').val();

        //deselects all cells
        $("td.sample_cell :checkbox").prop('checked', false);

        //selects all the best cells
        $("[id=" + target + "] table.samples_table tr").each(
            function() {
                $(this).find("td.sample_cell.qual" + quality + " :checkbox:first").prop('checked', true);
            });
    });
}

$(function(){
    initTabs();
    tdClick();
    qualityDropdownInit();
    dynamicParameterGroupSelectionInit();
    resetFormButtonInit();
    selectBestSamplesButtonInit();
});