from django.urls import path
from .views import ServerInputCreateView, ServerInputListView, \
    ServerInputDetailView, ServerInputUpdateView
from django.contrib.auth.decorators import login_required

app_name = 'serverinput'
urlpatterns = [
    path('create/', login_required(ServerInputCreateView.as_view()), name='create'),
    path('list/', login_required(ServerInputListView.as_view()), name='list'),
    path('detail/<int:pk>/', login_required(ServerInputDetailView.as_view()), name='detail'),
    path('edit/<int:pk>/', login_required(ServerInputUpdateView.as_view()), name='edit'),
]
