//creates accordions
function accordion(){
    $("div.accordion").accordion({
        autoHeight: false,
        heightStyle: "content",
        collapsible: true,
        active: true
    });
}

//hides and unhides new kinship module name field if the kinship module name dropdown selection is changed to New or not
function kinshipModuleDropdownInit(){
    $('#Kinship_Training_Module').change(function(){
       if($(this).val() == 'New Training Module'){
           $('#New_Kinship_Module_Name').removeClass('hidden');
       }else{
           $("#New_Kinship_Module_Name").val("");
           $('#New_Kinship_Module_Name').addClass('hidden');
       }
    });

    //default behavior is to hide this
    $('#New_Kinship_Module_Name').addClass('hidden');
}

$(function(){
    console.time('kinship dropdown init');
    kinshipModuleDropdownInit();
    console.timeEnd('kinship dropdown init');
    console.time('accordion');
    accordion();
    console.timeEnd('accordion');
});