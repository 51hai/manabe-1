from django.contrib.auth.models import User, Group
from appinput.models import App
from rightadmin.models import Permission


def is_admin_group(user):
    try:
        user_group = Group.objects.get(user=user)
    except Group.DoesNotExist:
        return False
    # 书中这里有问题
    if 'admin' == user_group.name:
        return True
    else:
        return False


def is_app_admin(app_id, user):
    app = App.objects.get(id=app_id)
    if user == app.manage_user or is_admin_group(user):
        return True
    return False


def get_app_admin(app_id):
    return App.objects.get(id=app_id).manage_user


def get_app_user(app_id, action_id, env_id):
    filter_dict = {
        "app_name_id": app_id,
        "action_name_id": action_id,
    }
    if int(env_id) != 0:
        filter_dict["env_name_id"] = env_id
    try:
        permission = Permission.objects.get(**filter_dict)
    except Permission.DoesNotExist:
        return set()
    user_set = permission.main_user.all()
    return user_set


def has_right(app_id, action_id, env_id, user):
    return is_admin_group(user) or \
           user in get_app_user(app_id, action_id, env_id)
