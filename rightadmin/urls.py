from django.urls import path
from .views import admin_user, DefaultView, RightAdminView, update_permission
from django.contrib.auth.decorators import login_required

app_name = 'rightadmin'
urlpatterns = [
    path('default/', login_required(DefaultView.as_view()),name='default'),
    path('list/<int:pk>/', login_required(RightAdminView.as_view()), name='list'),
    path('admin_user/<int:app_id>/<int:action_id>/<int:env_id>/',
         login_required(admin_user), name='admin_user'),
    path('update_permission/', login_required(update_permission), name='update_permission')
]
