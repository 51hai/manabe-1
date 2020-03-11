from django.urls import path

from .report_views import get_deploy_count, DeployCountView
from .views import DeployCreateView, DeployListView, DeployDetailView, \
    jenkins_build, jenkins_status, update_deploypool_jenkins
from .deploy_views import PublishView, DeployView, deploy_cmd, HistoryView, \
    OperateView, OperateAppView
from django.contrib.auth.decorators import login_required

app_name = 'deploy'
urlpatterns = [
    path('create/', login_required(DeployCreateView.as_view()), name='create'),
    path('list/', login_required(DeployListView.as_view()), name='list'),
    path('view/<slug:pk>/', login_required(DeployDetailView.as_view()), name='detail'),
    path('jenkins_build/', login_required(jenkins_build), name='jenkins_build'),
    path('jenkins_status/', login_required(jenkins_status), name='jenkins_status'),
    path('update_deploypool_jenkins/', login_required(update_deploypool_jenkins),
         name='update_deploypool_jenkins'),
    path('publish/', login_required(PublishView.as_view()), name='publish'),
    path('deploy/<slug:app_name>/<slug:deploy_version>/<slug:env>/',
         login_required(DeployView.as_view()), name='deploy'),
    path('deploy_cmd/', login_required(deploy_cmd), name='deploy_cmd'),
    path('operate/', login_required(OperateView.as_view()), name='operate'),
    path('operate_app/<slug:app_id>/<slug:env>/', login_required(OperateAppView.as_view()), name='operate_app'),
    path('history/', login_required(HistoryView.as_view()), name='history'),
]

urlpatterns += [
    path('get_deploy_count/', login_required(get_deploy_count),
         name='get_deploy_count'),
    path('deploy_count/', login_required(DeployCountView.as_view()),
         name='deploy_count'),
]
