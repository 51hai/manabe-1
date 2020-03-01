from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from appinput.models import App
from public.user_group import has_right, get_app_admin
from rightadmin.models import Action
from serverinput.models import Server
from .models import DeployPool
from .salt_cmd_views import deploy
from django.utils import timezone
from django.conf import settings
from django.db.models import Q, F


class PublishView(ListView):
    template_name = 'deploy/publish.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return DeployPool.objects.filter(
                Q(name__icontains=search_pk) |
                Q(description__icontains=search_pk)
            ).exclude(deploy_status__name__in=['CREATE', 'BUILD']). \
                order_by("-change_date")
        if self.request.GET.get('app_id'):
            app_id = self.request.GET.get('app_id')
            return DeployPool.objects.filter(app_name__id=app_id). \
                exclude(deploy_status__name__in=['CREATE', 'BUILD']). \
                order_by("-change_date")
        return DeployPool.objects.exclude(deploy_status__name__in=['CREATE', 'BUILD']). \
            order_by("-change_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = 'deploy-list'
        context['current_page_name'] = '发布单列表'
        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + '&'.join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context


class DeployView(ListView):
    template_name = 'deploy/deploy.html'
    paginate_by = 10

    def get_queryset(self):
        return Server.objects.filter(env_name__name=self.kwargs['env']). \
            filter(app_name__name=self.kwargs['app_name']).order_by("-change_date")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        app_name = self.kwargs['app_name']
        deploy_version = self.kwargs['deploy_version']
        context['env'] = self.kwargs['env']
        context['now'] = timezone.now()
        context['current_page'] = 'deploy-list'
        context['current_page_name'] = '部署服务器列表'
        context['app_name'] = app_name
        context['deploy_version'] = deploy_version
        deploy_item = DeployPool.objects.get(name=deploy_version)
        context['is_restart_status'] = deploy_item.app_name.is_restart_status
        context['deploy_type'] = deploy_item.deploy_type
        context['deploy_no'] = deploy_item.deploy_no
        context['is_inc_tot'] = deploy_item.is_inc_tot
        context['mablog_url'] = settings.MABLOG_URL

        app_id = deploy_item.app_name.id
        env_id = deploy_item.env_name.id
        action_item = Action.objects.get(name='DEPLOY')
        action_id = action_item.id
        context['has_right'] = has_right(app_id, action_id, env_id, self.request.user)
        context['admin_user'] = get_app_admin(app_id)

        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + '&'.join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context


@csrf_exempt
def deploy_cmd(request):
    user_name = request.user
    groud_cmd = request.POST.get('group_cmd')
    is_restart_server = False
    subserver_list = []
    p_value = 0
    deploy_version = ''
    app_name = ''
    deploy_type = ''
    sp_type = ''
    operation_type = ''
    for cmd_data in groud_cmd.split('&'):
        if cmd_data.startswith('serverSelect'):
            subserver_list.append(cmd_data.split('=')[1])
        if cmd_data.startswith('operation_type'):
            operation_type = (cmd_data.split('=')[1])
        if cmd_data.startswith('deploy_version'):
            deploy_version = (cmd_data.split('=')[1])
        if cmd_data.startswith('app_name'):
            app_name = (cmd_data.split('=')[1])
        if cmd_data.startswith('deploy_type'):
            deploy_type = (cmd_data.split('=')[1])
        if cmd_data.startswith('is_restart_server'):
            if (cmd_data.split('=')[1]) == 'restart':
                is_restart_server = True
        if cmd_data.startswith('env'):
            env = (cmd_data.split('=')[1])
        if cmd_data.startswith('sp_type'):
            sp_type = (cmd_data.split('=')[1])
        if cmd_data.startswith('p_value'):
            p_value = (cmd_data.split('=')[1])

    if sp_type == "serial_deploy" or p_value > len(subserver_list):
        p_value = len(subserver_list)
    subserver_list_group = mod_group(subserver_list, p_value)
    deploy_version = deploy_version if deploy_version != '' else 'Demo'

    if deploy_version == 'Demo':
        App.objects.filter(name=app_name).update(op_log_no=F('op_log_no') + 1)
    else:
        DeployPool.objects.filter(name=deploy_version). \
            update(deploy_no=F('deploy_no') + 1)

    deploy(subserver_list_group, deploy_type, is_restart_server,
           user_name, deploy_version, operation_type)
    result = {'return': 'OK'}
    return JsonResponse(result, status=200)


def mod_group(alist, agroup):
    tmp_list = [[] for i in range(agroup)]
    for i in range(len(alist)):
        tmp_list[i % agroup].append(alist[i])
    return tmp_list
