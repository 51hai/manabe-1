from django.urls import reverse, reverse_lazy
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from .models import App
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from .forms import AppForm
from public.user_group import is_admin_group, is_app_admin


# Create your views here.

class AppInputCreateView(CreateView):
    template_name = 'appinput/create_appinput.html'
    model = App
    form_class = AppForm

    def get(self, request, *args, **kwargs):
        if is_admin_group(self.request.user):
            return super().get(request, *args, **kwargs)
        else:
            result = '当前用户无权限，只有超级管理员才可进入！'
            return HttpResponse(result)

    def form_invalid(self, form):
        print(form)
        return self.render_to_response({'form': form})

    def form_valid(self, form):
        App.objects.create(
            name=form.cleaned_data['name'],
            description=form.cleaned_data['description'],
            jenkins_job=form.cleaned_data['jenkins_job'],
            git_url=form.cleaned_data['git_url'],
            build_cmd=form.cleaned_data['build_cmd'],
            package_name=form.cleaned_data['package_name'],
            zip_package_name=form.cleaned_data['zip_package_name'],
            is_restart_status=form.cleaned_data['is_restart_status'],
            script_url=form.cleaned_data['script_url'],
            manage_user=form.cleaned_data['manage_user'],
        )
        return HttpResponse(reverse('appinput:list'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['current_page'] = 'appinput-create'
        context['current_page_name'] = '新增APP应用'
        return context


class AppInputUpdateView(UpdateView):
    # 这里千万不要写成  /appinput/edit_appinput.html，这样会因为找不到该文件而报错
    template_name = "appinput/edit_appinput.html"
    model = App
    form_class = AppForm

    def get(self, request, *args, **kwargs):
        # 因为restful url中已经指定携带变量名为pk，
        # 所以就没有必要使用原文那种split path的方式来获取app_id了
        app_id = kwargs.get('pk')
        # app_id = request.path.split("/")[-2]
        print(kwargs)
        if is_app_admin(app_id, self.request.user):
            return super().get(request, *args, **kwargs)
        else:
            result = '当前用户无权限，只有管理员才可进入！'
            return HttpResponse(result)

    def form_invalid(self, form):
        return self.render_to_response({'form': form})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'appinput-edit'
        context['current_page_name'] = '编辑APP应用'
        context['app_id'] = self.kwargs.get(self.pk_url_kwarg)
        return context

    # 请求成功完成后，指定跳转页面的url
    def get_success_url(self):
        return reverse_lazy("appinput:list")


class AppInputListView(ListView):
    template_name = 'appinput/list_appinput.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.GET.get('search_pk'):
            search_pk = self.request.GET.get('search_pk')
            return App.objects.filter(
                Q(name__icontains=search_pk) |
                Q(package_name__icontains=search_pk)
            ).order_by('-change_date')
        return App.objects.all().order_by('-change_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        context['is_admin_group'] = is_admin_group(self.request.user)
        context['current_page'] = 'appinput-list'
        context['current_page_name'] = 'APP应用列表'
        # 这里之所以这样处理query_string，而不是将current_url写死为?&，
        # 是因为如果按条件搜索出指定的结果集后，再进行翻页时，必须要携带原有的搜索条件，
        # 不然就不合理了，举个例子，比如:
        # query_string为search_pk=ABC&page=2
        # 则我们期望“下一页”的url应该是search_pk=ABC&page=3
        # 所以这里我们应当把page去掉，保留其他的参数列表，
        # 所以current_url则应为?search_pk=ABC&
        query_string = self.request.META.get('QUERY_STRING')
        # print(f'*****{query_string}')
        if 'page' in query_string:
            query_list = query_string.split('&')
            query_list = [elem for elem in query_list if not elem.startswith('page')]
            query_string = '?' + '&'.join(query_list) + '&'
            # print(f'+++++++{query_string}')
        elif query_string is not None:
            query_string = '?' + query_string + '&'
            # print(f'========{query_string}')
        context['current_url'] = query_string
        return context


class AppInputDetailView(DetailView):
    template_name = 'appinput/detail_appinput.html'
    model = App

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page_name'] = 'App应用详情'
        context['now'] = timezone.now()
        return context
