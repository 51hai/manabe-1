from django.contrib import messages
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView
from django.db.models import Q
from public.user_group import has_right, get_app_admin
from rightadmin.models import Action
from .models import Env
from deploy.models import DeployPool, DeployStatus, History
import time


# Create your views here.


class EnvXListView(ListView):
    template_name = 'envx/list_envx.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return DeployPool.objects.filter(
                Q(name__icontains=search_pk) |
                Q(description__icontains=search_pk)
            ).exclude(
                deploy_status__name__in=['CREATE']
            ).order_by('-change_date')
        if self.request.GET.get('app_id'):
            app_id = self.request.GET.get('app_id')
            return DeployPool.objects.filter(
                app_name_id=app_id
            ).exclude(
                deploy_status__name__in=['CREATE']
            ).order_by('-change_date')

        return DeployPool.objects.exclude(deploy_status__name__in=['CREATE']). \
            order_by('-change_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = 'envx-list'
        context['current_page_name'] = '环境流转'
        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + '&'.join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['query_string'] = query_string
        return context


def change(request):
    if request.POST:
        if request.POST.get('deploy_id') is None or \
                request.POST.get('env_id') is None:
            messages.error(request, '参数错误，请重新选择！', extra_tags='c-error')
            return redirect('envx:list')
        else:
            user = request.user
            deploy_id = request.POST.get('deploy_id')
            env_id = request.POST.get('env_id')
            deploy_item = DeployPool.objects.get(id=deploy_id)
            app_item = deploy_item.app_name
            org_env_name = deploy_item.env_name.name \
                if deploy_item.env_name is not None else 'BUILD'
            action_item = Action.objects.get(name='XCHANGE')
            app_id = app_item.id
            action_id = action_item.id
            if not has_right(app_id, action_id, 0, user):
                manage_user = get_app_admin(app_id)
                # extra_tags就是自定义的tag，
                # 可以在template中使用.tags获取到
                messages.error(request, f'没有权限，请联系该应用管理员{manage_user}',
                               extra_tags='c-error')
                return redirect('envx:list')
            env_name = Env.objects.get(id=env_id)
            deploy_status = DeployStatus.objects.get(name='READY')
            DeployPool.objects.filter(id=deploy_id).update(
                env_name=env_name, deploy_status=deploy_status
            )
            messages.success(request, '环境流转成功！', extra_tags='c-success')

            History.objects.create(
                name=f'{app_item.name}-xchange-{deploy_item.name}-'
                     f'{time.strftime("%Y-%m-%d-%H%M%S", time.localtime())}',
                user=user,
                app_name=app_item,
                deploy_name=deploy_item,
                do_type='XCHANGE',
                content={'before': org_env_name, 'after': env_name.name}
            )
            return redirect('envx:list')
    messages.error(request, '请求无效', extra_tags='c-error')
    return redirect('envx:list')


class EnvXHistoryView(ListView):
    template_name = 'envx/list_history.html'
    paginate_by = 20

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return History.objects.filter(
                Q(name__icontains=search_pk) |
                Q(app_name___name__icontains=search_pk)
            ).filter(do_type='XCHANGE').order_by('-add_date')

        if self.request.GET.get('app_id'):
            app_id = self.request.GET.get('app_id')
            # 这里用filter，不要用get，省的处理History.DoesNotExist异常
            return History.objects.filter(app_name_id=app_id). \
                filter(do_type='XCHANGE').order_by('-add_date')
        return History.objects.filter(do_type='XCHANGE').order_by('-add_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = 'envx-history'
        context['current_page_name'] = '环境流转历史'
        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + '&'.join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['query_string'] = query_string
        return context
