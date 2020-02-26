from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from appinput.models import App
from envx.models import Env
from public.user_group import is_app_admin
from .models import Action, Permission


# Create your views here.
class DefaultView(TemplateView):
    template_name = 'rightadmin/default.html'

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response


class RightAdminView(TemplateView):
    template_name = 'rightadmin/list_rightadmin.html'

    # 防止直接使用url越权获得某应用的权限设置详情
    def get(self, request, *args, **kwargs):
        if is_app_admin(kwargs['pk'], self.request.user):
            return super().get(request, *args, **kwargs)
        return HttpResponse('当前用户无权限，只有管理员才可进入！')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_id = kwargs['pk']
        context['app'] = App.objects.get(id=app_id)
        context['action'] = Action.objects.all().order_by('aid')
        context['env'] = Env.objects.all()
        context['current_page'] = 'rightadmin-list'
        context['current_page_name'] = 'App权限管理'
        return context

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response


def admin_user(request, app_id, action_id, env_id):
    # 防止直接使用url越权获得某应用的权限设置详情
    if not is_app_admin(app_id, request.user):
        return HttpResponse('当前用户无权限，只有管理员才可进入！')

    all_user_set = User.objects.all().order_by('username')
    guests = []
    users = []
    # 使用app_name_id或app_name__id都可以，
    # 因为django建表时，默认给外键列取的列名就是app_name_id，
    # 其他同理
    filter_dict = {
        'app_name_id': app_id,
        'action_name__id': action_id,
    }
    # 在action_name_id为3时,env_id才有值
    if env_id != 0:
        filter_dict['env_name__id'] = env_id
    try:
        # 因为APP在发布之前，环境不能确定，所以env_id均为null,
        # 所以当action不为DEPLOY时，
        # 使用app_name_id和action_name_id就可确认一条唯一的权限
        permission_set = Permission.objects.get(**filter_dict)
        user_set = permission_set.main_user.all()
        for user in all_user_set:
            if user in user_set:
                users.append(user)
            else:
                guests.append(user)
    except Permission.DoesNotExist as e:
        print(e)
        guests = all_user_set
    var_dict = {
        'users': users,
        'app_id': app_id,
        'action_id': action_id,
        'env_id': env_id,
        'guests': guests
    }
    # return render(request, 'rightadmin/edit_user.html', var_dict)
    response = render(request, 'rightadmin/edit_user.html', var_dict)
    response['X-Frame-Options'] = 'SAMEORIGIN'
    return response


@csrf_exempt
def update_permission(request):
    select_user = []
    app_id = 0
    action_id = 0
    env_id = 0
    group_data = request.POST.get('group_data')
    for item in group_data.split('&'):
        if item.startswith('selectUser'):
            select_user.append(item.split('=')[1])
        if item.startswith('app_id'):
            app_id = item.split('=')[1]
        if item.startswith('action_id'):
            action_id = item.split('=')[1]
        if item.startswith('env_id'):
            env_id = item.split('=')[1]
    # 正常应该在admin_user中进行权限管控，因为没有在admin_user中进行权限管控，
    # 所以即便是在list_appinput.html页面“授权按钮”是disabled的情况下，
    # 依然可以直接使用url: 'list'或者'admin_user'进行权限查看，
    # 虽然无法进行修改，但我认为这依然是不合适的，所以做了一些粗略的修改
    if not is_app_admin(app_id, request.user):
        return JsonResponse({'return': 'error'})

    filter_dic = {
        'app_name_id': app_id,
        'action_name_id': action_id,
    }
    # 这里一定要用'0'而不能是0，因为与admin_user()中不同，
    # 访问admin_user时，urls.py中path中已经将env_id转换成了int，
    # 而这里env_id是从请求体中携带的字符串中，经过拆解获取的，所以一定要用'0'，
    # 否则就会有DoesNotExist的异常
    if env_id != '0':
        filter_dic['env_name_id'] = env_id
    try:
        permission_item = Permission.objects.get(**filter_dic)
        new_users = User.objects.filter(id__in=select_user)
        permission_item.main_user.set(new_users)
        permission_item.save()
    except Permission.DoesNotExist:
        new_users = User.objects.filter(id__in=select_user)
        app = App.objects.get(id=app_id)
        action = Action.objects.get(id=action_id)
        name = f'{app_id}-{action_id}-{env_id}'
        dic = {
            'name': name,
            'app_name': app,
            'action_name': action
        }
        if env_id != '0':
            env = Env.objects.get(id=env_id)
            dic['env_name'] = env
        permission_item = Permission.objects.create(**dic)
        permission_item.main_user.set(new_users)
        permission_item.save()
    # 这里，还有上面的JsonResponse相应的字典中的key
    # 应与edit_user.html中的ajax中的判断相对应，
    # 因为前端要获得相应数据中的return的值，所以我们这里就传一个return的值出去，
    # 这个return没有任何特殊意义，取什么名字都可以，只要前后端取一致就行
    # success: function(data) {
    #                 console.log(data);
    #                 if (data['return'] == 'error') {
    #                     $.Huimodalalert("<span class='c-danger'>亲，没有权限更新哟~</span>",3000);
    #                 }
    #                 if (data['return'] == 'success') {
    #                     $.Huimodalalert("<span class='c-success'>权限更改成功！</span>",3000);
    #                 }
    #             }
    return JsonResponse({'return': 'success'})
