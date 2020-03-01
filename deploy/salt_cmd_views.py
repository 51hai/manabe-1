import uuid
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from django.http import JsonResponse
from django.conf import settings
from serverinput.models import Server
from .models import DeployPool, DeployStatus, History
from public.salt import salt_api_inst

mylog = logging.getLogger('manabe')


def deploy(subserver_list_group, deploy_type, is_restart_server,
           user_name, deploy_version, operation_type):
    worker_num = len(subserver_list_group[0])
    executor = ThreadPoolExecutor(max_workers=worker_num)
    if deploy_type in ['deployall', 'deploypkg', 'deploycfg']:
        action_list = ['prepare', 'backup', 'stop', deploy_type, 'start', 'check'] \
            if is_restart_server else ['prepare', 'backup', deploy_type, 'check']
    elif deploy_type == 'rollback':
        action_list = ['stop', 'rollback', 'start', 'check'] \
            if is_restart_server else ['rollback', 'check']
    elif deploy_type == 'stop':
        action_list = ['stop']
    elif deploy_type == 'start':
        action_list = ['start', 'check']
    elif deploy_type == 'restart':
        action_list = ['stop', 'start', 'check']
    else:
        return False
    action_len = len(action_list)
    for item in subserver_list_group:
        for index, action in enumerate(action_list):
            # percent_value = "%.0f%%" % ((index + 1) / action_len * 100)
            percent_value = f'{((index + 1) / action_len * 100):.0f}%'
            # server_id = []
            # for item_id in item:
            #     server_id.append(item_id)
            # server_len = len(server_id)
            server_len = len(item)
            for data in executor.map(action_run, item,
                                     [action] * server_len,
                                     [user_name] * server_len,
                                     [percent_value] * server_len,
                                     [deploy_version] * server_len,
                                     [operation_type] * server_len):
                if not data:
                    return False
    return True


def action_run(server_id, action, user_name, percent_value,
               deploy_version=None, operation_type=None):
    server_item = Server.objects.get(id=server_id)
    tgt = server_item.salt_name
    port = server_item.port
    app_user = server_item.app_user
    env_name = server_item.env_name.name.lower()
    app_name = server_item.app_name.name
    script_url = server_item.app_name.script_url
    zip_package_name = server_item.app_name.zip_package_name
    package_name = server_item.app_name.zip_package_name
    nginx_url = settings.NGINX_URL

    if deploy_version != 'Demo':
        deploypool_item = DeployPool.objects.get(name=deploy_version)
        is_inc_tot = deploypool_item.is_inc_tot
        deploy_no = deploypool_item.deploy_no
    else:
        deploypool_item = None
        is_inc_tot = "tot"
        deploy_no = server_item.app_name.op_log_no

    arg_args = f"-a {app_name} -e {env_name} -v{deploy_version} " \
               f"-z {zip_package_name} -p {package_name} -o {port} " \
               f"-c {action} -i {is_inc_tot} -u {nginx_url}"
    arg = [script_url, arg_args, 'runas=' + app_user, 'env={"LC_ALL":""}']
    result = salt_run(tgt=tgt, arg=arg)

    mylog.debug(f"deploy argument is: {arg}.")
    mylog.debug(f"deploy_result is {result}.")

    try:
        result_retcode = result['return'][0][tgt]['retcode']
        result_stderr = result['return'][0][tgt]['stderr']
        result_stdout = result['return'][0][tgt]['stdout'].replace('\r\n', '')
        print(result_retcode, result_stderr, result_stdout, result, '@@@@@@@')
    except Exception as e:
        print(e)
        return False
    if result_retcode == 0:
        if 'deploy' in action or 'rollback' in action:
            change_server(server_id, deploy_version, action, "success")
            change_deploypool(env_name, deploy_version, app_name, action)
        content = {
            'msg': 'success',
            'ip': server_item.ip_address,
            'action': action
        }
        log_content = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime()
        ) + action + '\n' + tgt + ', deploy progress ' + percent_value + '\n'

        add_history(
            user_name,
            server_item.app_name,
            deploypool_item,
            server_item.env_name,
            operation_type,
            content
        )
    else:
        change_server(server_id, deploy_version, action, "error")
        change_deploypool(env_name, deploy_version, app_name, action)
        content = {
            'msg': 'success',
            'ip': server_item.ip_address,
            'action': action
        }
        log_content = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime()
        ) + action + '\n' + tgt + ', error \n' + result

        add_history(
            user_name,
            server_item.app_name,
            deploypool_item,
            server_item.env_name,
            operation_type,
            content
        )
        return False
    time.sleep(2)
    return True


def salt_run(tgt=None, arg=None):
    return salt_api_inst().cmd_script(tgt=tgt, arg=arg)


def change_server(server_id, deploy_version, action, result):
    server_item = Server.objects.get(id=server_id)
    server_item.deploy_status = f"{action}:{result}"
    if "deploy" in action:
        if server_item.history_deploy:
            temp_list = server_item.history_deploy.split(',')
            if len(temp_list) > 10:
                history_deploy = f'{deploy_version},' + ','.join(temp_list[:-1])
            else:
                history_deploy = f'{deploy_version},' + server_item.history_deploy
        else:
            history_deploy = deploy_version
        server_item.history_deploy = history_deploy
    if "rollback" in action:
        if len(server_item.history_deploy.split(',')) < 2:
            result = {'return': '没有可回滚版本'}
            return JsonResponse(result, status=400)
        else:
            hd = server_item.history_deploy
            server_item.history_deploy = hd[hd.index(',') + 1:]

    server_item.save()


def change_deploypool(env_name, deploy_version, app_name, action):
    deploypool_item = DeployPool.objects.get(name=deploy_version)
    server_set = Server.objects.filter(
        app_name__name=app_name,
        env_name__name=env_name.upper()
    )
    svr_his_version_total = []
    svr_status_total = ""

    if "rollback" in action:
        pass
    else:
        for server_item in server_set:
            if server_item.history_deploy:
                temp_item = server_item.history_deploy.split(",")[0]
                if temp_item not in svr_his_version_total:
                    svr_his_version_total.append(temp_item)
                else:
                    pass
            else:
                svr_his_version_total.append("None")
            if server_item.deploy_status:
                svr_status_total += server_item.deploy_status
            else:
                svr_status_total += 'None'

        if 'error' in svr_status_total:
            deploy_status = DeployStatus.objects.get(name='ERROR')
        elif len(svr_his_version_total) > 1:
            deploy_status = DeployStatus.objects.get(name='ING')
        elif len(svr_his_version_total) == 1:
            deploy_status = DeployStatus.objects.get(name='FINISH')
        else:
            deploy_status = DeployStatus.objects.get(name='ERROR')
        deploypool_item.deploy_status = deploy_status
        deploypool_item.save()


def add_history(user, app_name, deploy_name, env_name, do_type, content):
    rid = uuid.uuid4()
    History.objects.create(
        name=rid,
        user=user,
        app_name=app_name,
        deploy_name=deploy_name,
        env_name=env_name,
        do_type=do_type,
        content=content
    )
