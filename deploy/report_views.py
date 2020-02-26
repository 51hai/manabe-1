from datetime import timedelta
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.http import JsonResponse
from .models import DeployPool
from envx.models import Env
from django.db.models import Count


def get_deploy_count(request):
    return_list = []
    # 这里因为在settings中设有USE_TZ = True，
    # 所以如果使用datetime.datetime.now()会有warning：
    # RuntimeWarning: DateTimeField DeployPool.add_date received a naive datetime
    # ... while time zone support is active.
    # 所以这里使用django.utils.timezone.now()
    now = timezone.now()
    a_month = now - timedelta(days=60)
    select = {'day': 'date(add_date)'}
    env = request.GET.get('env', 'All')
    if env != 'All':
        # 这里之所以分俩次查询，先查出env_id，再到deploypool中进行取值，
        # 而不是直接使用env_name__name=env，
        # 是因为使用__name的方式是两表关联查询，而俩表中都有add_date字段，
        # 在使用extra(select={...})时,会出现column ambiguous的问题。
        env_id = Env.objects.get(name=env).id
        a_month_deploy_qs = DeployPool.objects. \
            filter(env_name_id=env_id).filter(add_date__range=(a_month, now)). \
            extra(select=select).values('day'). \
            annotate(number=Count('id')).order_by('day')
    else:
        # 如下查询相当与sql:
        # select date(add_date) day, count(id) from deploy_pool
        #  where add_date between between DATE_SUB(now(), INTERVAL 60 DAY) and now()
        #  group by day
        #  order by day
        a_month_deploy_qs = DeployPool.objects. \
            filter(add_date__range=(a_month, now)). \
            extra(select=select).values('day'). \
            annotate(number=Count('id')).order_by('day')

    for item in a_month_deploy_qs:
        item_dict = {}
        item_key = item['day'].strftime('%m-%d')
        item_dict[item_key] = item['number']
        return_list.append(item_dict)

    return JsonResponse(return_list, safe=False)


class DeployCountView(TemplateView):
    template_name = 'deploy/deploy_count.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_page_name'] = '发布数据'
        return context
