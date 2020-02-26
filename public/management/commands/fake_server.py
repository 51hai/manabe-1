from django.contrib.auth.models import User
from random import choice
from appinput.models import App
from envx.models import Env
from serverinput.models import Server


def fake_server_data():
    Server.objects.all().delete()
    print('delete all server data')
    user_set = User.objects.all()
    app_set = App.objects.all()
    env_set = Env.objects.all()
    for i in range(1,101):
        ip_address = salt_name = f'192.168.12.{i}'
        for j in [80, 443, 8080, 8888]:
            port = j
            name = f'192.168.12.{i}_{port}'
            app_user = choice(['root', 'tomcat', 'javauser'])
            op_user = choice(user_set)
            app_name = choice(app_set)
            env_name = choice(env_set)

            Server.objects.create(name=name,
                                  ip_address=ip_address,
                                  port=port,
                                  salt_name=salt_name,
                                  app_name=app_name,
                                  op_user=op_user,
                                  app_user=app_user,
                                  env_name=env_name)
    print('create all server data')
