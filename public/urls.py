from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import get_app, get_env

app_name = 'public'

urlpatterns = [
    path('get-env/', login_required(get_env), name='get-env'),
    path('get-app/', login_required(get_app), name='get-app'),
]
