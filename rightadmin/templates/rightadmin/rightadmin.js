var zTreeObj,
	setting = {
	};
	zTreeNodes = [
		{"name":"应用名称：{{ app.name }}", open:true,
            children: [
                {% for single_action in action %}
                    {% ifnotequal single_action.name 'DEPLOY' %}
                        {
                            "name":"{{ single_action.description }}",
                            "url":"{% url 'rightadmin:admin_user' app_id=app.id action_id=single_action.id env_id=0 %}",
                            "target":"myFrame"
                        },
                    {% endifnotequal %}
                    {% ifequal single_action.name 'DEPLOY' %}
                        {
                            "name":"{{ single_action.description }}", open:true,
                            children:[
                                {% for single_env in env %}
                                    {
                                        "name":"{{ single_env.description }}",
                                        "url":"{% url 'rightadmin:admin_user' app_id=app.id action_id=single_action.id env_id=single_env.id %}",
                                        "target":"myFrame"
                                    },
                                {% endfor %}
                            ]
                        },
                    {% endifequal %}
                {% endfor %}
            ]
		}
	];

	$(document).ready(function(){
		zTreeObj = $.fn.zTree.init($("#treeAppRight"), setting, zTreeNodes);
	});