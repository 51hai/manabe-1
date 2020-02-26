from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import EnvXListView, change, EnvXHistoryView

app_name = 'envx'

urlpatterns = [
    path('list/', login_required(EnvXListView.as_view()), name='list'),
    path('change/', login_required(change), name='change'),
    path('history/', login_required(EnvXHistoryView.as_view()), name='history')
]
