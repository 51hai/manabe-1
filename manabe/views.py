import platform
import django
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from appinput.models import App
from deploy.models import DeployPool
from serverinput.models import Server
from .forms import RegisterForm, LoginForm


# def redirect_login(request):
#     pass


def redirect_login(request):
    """
    当使用了login_required装饰器后，访问原url时如果未登录，则会重定向到LOGIN_URL,
    并且在LOGIN_URL后加上next参数，参数内容为原url，如下：
    http://127.0.0.1:8000/accounts/login/?next=/accounts/change_email/
    settings.py中默认LOGIN_URL为'/accounts/login/'，该值可以在settings.py中修改
    GET请求会将请求内容放在头部，而POST请求是将内容放在包体，
    所以，当使用POST请求上述url时，有俩种办法获取next的值：
    1.最直接的是，在这里直接使用request.GET.get('next','')，来获取POST请求的头部携带变量，
      即URL中携带的参数及参数值
    2.由于第一次请求是一次get请求，user_login会返回一个空form，
      在login.html中添加一个hidden类型的input:
      <input type="hidden" name="next" value="{{ request.GET.next }}">
      则可以获取到这次get请求中的next的值，并把这个值再赋给这个name也为next的input.
      然后下一次请求必然是POST请求，就可以使用request.POST.get('next','')
      来间接获取next的值了。
    """
    login_url = reverse('index')
    # print(request.POST.get('next'))
    # print(request.POST)
    # print(request.GET)
    # 这里因为urls.py中index的url为''，所以reverse的结果是'/'，所以这里可以反解析'index'
    # 如果request.POST.get('next') == NONE，则request.POST.get('next') = index的url
    # return HttpResponseRedirect(request.POST.get('next', login_url))
    return HttpResponseRedirect(request.GET.get('next', login_url))


@require_http_methods(['GET', 'POST'])
def user_register(request):
    error = []
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            email = data['email']
            password = data['password']
            password2 = data['password2']
            if not User.objects.filter(username__iexact=username):
                if form.pwd_validate(password, password2):
                    user = User.objects.create_user(username, email, password)
                    user.save()
                    user = authenticate(username=username, password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            return redirect_login(request)
                else:
                    error.append('密码不一致，请确认')
            else:
                error.append('该用户名已使用，请更换用户名')
        else:
            error.append('请确认各输入框填写无误')
        var_dict = {
            'form': form,
            'error': error
        }
        return render(request, 'accounts/register.html', var_dict)
    else:
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(['GET', 'POST'])
def user_login(request):
    error = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            vc = request.POST['vc']
            username = data['username']
            password = data['password']
            if vc.upper() == request.session['verify_code']:
                user = authenticate(username=username, password=password)
                if user:
                    if user.is_active:
                        login(request, user)
                        return redirect_login(request)
                    else:
                        error.append('用户未被激活')
                else:
                    error.append('请输入正确的用户名和密码')
            else:
                error.append('验证码错误!')
        else:
            error.append('请确认各输入框填写无误')
        var_dict = {
            'form': form,
            'error': error
        }
        # 不将vc作为LoginForm属性，这里返回form时，就不会携带上一次输入的验证码
        return render(request, 'accounts/login.html', var_dict)
    else:
        form = LoginForm()
        # print(request.GET.get('next'))
        return render(request, 'accounts/login.html', {'form': form})


class IndexView(TemplateView):
    template_name = "manabe/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page'] = 'index'
        context['app_count'] = App.objects.count()
        context['server_count'] = Server.objects.count()
        context['deploy_count'] = DeployPool.objects.count()
        context['REMOTE_ADDR'] = self.request.META.get("REMOTE_ADDR")
        context['HTTP_USER_AGENT'] = self.request.META.get("HTTP_USER_AGENT")
        context['HTTP_ACCEPT_LANGUAGE'] = self.request.META.get('HTTP_ACCEPT_LANGUAGE')
        context['platform'] = platform.platform()
        context['python_version'] = platform.python_version()
        context['django_version'] = django.get_version()

        return context
