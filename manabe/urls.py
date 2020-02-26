"""manabe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.views.generic.base import RedirectView
from django.contrib.staticfiles.views import serve
from django.contrib import admin
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views, change_views
from public.verifycode import verify_code

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/register/', views.user_register, name='register'),
    path('accounts/login/', views.user_login, name='login'),
    path('verify_code', verify_code, name='verify_code'),
    path('accounts/change_email/', change_views.change_email, name='change_email'),
    path('logout/', logout_then_login, name='logout'),
    path('app/', include('appinput.urls')),
    path('public/', include('public.urls')),
    path('server/', include('serverinput.urls')),
    path('deploy/', include('deploy.urls')),
    path('envx/', include('envx.urls')),
    path('rightadmin/', include('rightadmin.urls')),
    # path('favicon.ico', RedirectView.as_view(url=r'static/favicon.ico')),
    path('favicon.ico', serve, {'path': 'static/favicon.ico'}),
    path('', login_required(views.IndexView.as_view()), name='index')
]
