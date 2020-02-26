from random import sample, choice
import time
from string import ascii_letters
from deploy.models import DeployPool, DeployStatus
from django.contrib.auth.models import User
from appinput.models import App
from envx.models import Env


def fake_deploy_pool_data():
    DeployPool.objects.all().delete()
    print('delete all deploy pool data')
    app_set = App.objects.all()
    env_set = Env.objects.all()
    user_set = User.objects.all()
    is_inc_tot = ['TOT', 'INC']
    deploy_type = ['deployall', 'deploycfg', 'deploypkg']
    deploy_status_set_rife = DeployStatus.objects. \
        filter(name__in=['READY', 'ING', 'FINISH', 'ERROR'])
    deploy_status_set_create = DeployStatus.objects.get(name='CREATE')
    deploy_status_set_build = DeployStatus.objects.get(name='BUILD')

    for date_no in range(30):
        random_letter = ''.join(sample(ascii_letters, 2))
        t = (2020, 3, date_no + 1, 17, 3, 38, 1, 48, 0)
        fake_time_str = time.strftime('%Y-%m-%d-%H%M%S', t)
        name = fake_time_str + random_letter.upper()
        DeployPool.objects.create(
            name=name,
            description='test',
            branch_build='master',
            jenkins_number=date_no,
            code_number=date_no + 10,
            is_inc_tot=choice(is_inc_tot),
            deploy_type=choice(deploy_type),
            create_user=choice(user_set),
            app_name=choice(app_set),
            env_name=choice(env_set),
            deploy_status=choice(deploy_status_set_rife),
            nginx_url='http://www.yanxin.com/'
        )
    for date_no in range(30):
        random_letter = ''.join(sample(ascii_letters, 2))
        t = (2020, 3, date_no + 1, 17, 3, 38, 1, 48, 0)
        fake_time_str = time.strftime('%Y-%m-%d-%H%M%S', t)
        name = fake_time_str + random_letter.upper()
        if date_no % 2 == 1:
            DeployPool.objects.create(
                name=name,
                description='test',
                branch_build='master',
                jenkins_number=date_no,
                code_number=date_no + 10,
                is_inc_tot=choice(is_inc_tot),
                deploy_type=choice(deploy_type),
                create_user=choice(user_set),
                app_name=choice(app_set),
                env_name=choice(env_set),
                deploy_status=deploy_status_set_create
            )
        else:
            DeployPool.objects.create(
                name=name,
                description='test',
                branch_build='master',
                jenkins_number=date_no,
                code_number=date_no + 10,
                is_inc_tot=choice(is_inc_tot),
                deploy_type=choice(deploy_type),
                create_user=choice(user_set),
                app_name=choice(app_set),
                env_name=choice(env_set),
                deploy_status=deploy_status_set_build,
                nginx_url='http://www.yanxin.com/'
            )
    print('create all deploy pool data')
