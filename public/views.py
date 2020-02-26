from django.http import JsonResponse
from appinput.models import App
from envx.models import Env


# Create your views here.

def get_app(request):
    app_dict = {}
    # 如下是获得了一个字典QuerySet
    for app in App.objects.all().values('id', 'name'):
        app_dict[app['id']] = app['name']
    return JsonResponse(app_dict)


def get_env(request):
    env_dict = {}
    # 如下是获得了一个对象QuerySet
    for env in Env.objects.all():
        env_dict[env.id] = env.name
    return JsonResponse(env_dict)
