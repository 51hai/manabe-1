from envx.models import Env


def fake_env_data():
    Env.objects.all().delete()
    print('delete all env data')
    Env.objects.create(name='DEV', description='DEV环境', eid=1)
    Env.objects.create(name='TEST', description='TEST环境', eid=2)
    Env.objects.create(name='PROD', description='PROD环境', eid=3)
    print('create all env data')
