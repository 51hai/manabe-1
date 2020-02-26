from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from .models import Server
from .forms import ServerForm
from public.user_group import is_admin_group


# Create your views here.

class ServerInputCreateView(CreateView):
    template_name = 'serverinput/create_serverinput.html'
    model = Server
    form_class = ServerForm

    def get(self, request, *args, **kwargs):
        if is_admin_group(self.request.user):
            return super().get(request, *args, **kwargs)
        else:
            result = '当前用户无权限，只有管理员才可进入！'
            return HttpResponse(result)

    def form_invalid(self, form):
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        current_user = self.request.user
        Server.objects.create(
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            ip_address=form.cleaned_data['ip_address'],
            salt_name=form.cleaned_data['salt_name'],
            port=form.cleaned_data['port'],
            app_user=form.cleaned_data['app_user'],
            app_name=form.cleaned_data['app_name'],
            env_name=form.cleaned_data['env_name'],
            op_user=current_user
        )
        return HttpResponseRedirect(reverse('serverinput:list'))

    def get_success_url(self):
        return reverse_lazy('serverinput:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = 'serverinput-create'
        context['current_page_name'] = '新增服务器'
        return context


class ServerInputListView(ListView):
    template_name = 'serverinput/list_serverinput.html'
    paginate_by = 10

    # 默认传到template的对象名是object_list，可使用如下方式进行修改
    # 在list_appinput.html中我保持默认，
    # 在list_serverinput.html中，我试验自定义命名
    context_object_name = 'server'

    def get_queryset(self):
        # 这里对应前端search模块
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return Server.objects.filter(
                Q(name__icontains=search_pk) |
                Q(ip_address__icontains=search_pk) |
                Q(port__icontains=search_pk)
            ).order_by('-change_date')
        # 这里对应前端filter模块
        if self.request.GET.get('app_id'):
            app_id = self.request.GET.get('app_id')
            return Server.objects.filter(app_name_id=app_id).order_by('-change_date')
        return Server.objects.all().order_by('-change_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_admin_group'] = is_admin_group(self.request.user)
        context['now'] = timezone.now()
        context['current_page'] = 'serverinput-list'
        context['current_page_name'] = '服务器列表'
        query_string = self.request.META.get('QUERY_STRING')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + '&'.join(query_list) + '&'
        elif query_string is not None:
            query_string = '?' + query_string + '&'
        context['current_url'] = query_string
        return context


class ServerInputDetailView(DetailView):
    template_name = 'serverinput/detail_serverinput.html'
    model = Server

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page_name'] = '服务器详情'
        context['now'] = timezone.now()
        return context


class ServerInputUpdateView(UpdateView):
    template_name = 'serverinput/edit_serverinput.html'
    model = Server
    form_class = ServerForm

    def get(self, request, *args, **kwargs):
        if is_admin_group(self.request.user):
            return super().get(request, *args, **kwargs)
        return HttpResponse('当前用户无权限，只有超级管理员才可进入！')

    def form_invalid(self, form):
        return self.render_to_response({'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'serverinput-edit'
        context['current_page_name'] = '编辑服务器'
        context['now'] = timezone.now()
        context['server_id'] = self.kwargs.get(self.pk_url_kwarg, None)
        print(f'===>{self.pk_url_kwarg}')
        print(self.kwargs)
        return context

    def get_success_url(self):
        return reverse_lazy('serverinput:list')
