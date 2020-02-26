$(document).ready(function(){
    $.ajax({
        type: "GET",
        url: "{% url 'public:get-env' %}",
        dataType: "json",
        success: function(data){
            console.log(data);
            $.each(data, function(index,value){
                $('.envSelect').append('<option value="' + index + '">' + value + '</option>');
            });
        },
        error: function(){
            alert("系统出现问题");
        }
    });
    {% for msg in messages %}
        $.Huimodalalert('<span {% if msg.tags %} class="{{ msg.tags }}"{% endif %}>{{ msg }}</span>',3000);
    {% endfor %}


    $(".envChange").click(function(){
        deploy_id = $(this).attr('deploy_id');
        deploy_name = $(this).attr('deploy_name');
        org_env_id = $(this).attr('org_env_id');
        env_id = $(this).prev().find("option:selected").val();
        env_name = $(this).prev().find("option:selected").text();
        console.log(org_env_id + '===>' + env_id);
        if(org_env_id == env_id || env_id == ""){
            $.Huimodalalert('<span class="c-error">环境为空或无效，请重新选择!</span>',3000);
            return false;
        }
        $('#selectDeploy').html(deploy_name);
        $('#selectEnv').html(env_name);
        $('#deploy_id').val(deploy_id);
        $('#env_id').val(env_id);
        $("#modal-demo").modal("show");
    });


    $('#changeEnvModal').click(function(){
        $('#envForm').submit();
    }
    );
});