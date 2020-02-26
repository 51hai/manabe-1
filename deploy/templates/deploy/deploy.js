function getParallelOptions(sp_select_id){
    if(sp_select_id=="parallel_deploy" && $("#p_select_id").length <= 0){
        html_str = '<select name="p_value" id="p_select_id" class="select"> \
                    +       <option selected value='1'> 1 </option> \
                    +       <option selected value='2'> 2 </option> \
                    +       <option selected value='3'> 3 </option> \
                    +       <option selected value='4'> 4 </option> \
                    +       <option selected value='5'> 5 </option> \
                    + </select>'
        $("#sp_select_id").after(html_str);
    }
    if(sp_select_id=="serial_deploy" && $("#p_select_id").length > 0){
        $("#p_select_id").remove();
    }
}

$("#close_deploylogout").click(function(){
    $('#deploylogout').hide();
    window.location.reload();
});

$("#btn-deploy").click(function(evt){
    
});