import requests
from requests.adapters import HTTPAdapter
from django.http import JsonResponse
import json

HOST = '192.168.12.103'
USERNAME = 'salt-api-client'
PORT = '8899'
PASSWORD = 'oracle'
EPROTO = 'pam'
SECURE = True

requests.packages.urllib3.disable_warnings()
requests_session = requests.Session()
requests_session.mount('http://', HTTPAdapter(max_retries=3))
requests_session.mount('https://', HTTPAdapter(max_retries=3))


class SaltStack:
    cookies = None
    host = None

    def __init__(self, host, username, password, port='8000',
                 secure=True, eproto='pam'):
        proto = 'https' if secure else 'http'
        self.host = f'{proto}://{host}:{port}'
        self.login_url = self.host + '/login'
        self.logout_url = self.host + '/logout'
        self.minions_url = self.host + '/minions'
        self.jobs_url = self.host + '/jobs'
        self.runs_url = self.host + '/runs'
        self.events_url = self.host + '/events'
        self.ws_url = self.host + '/ws'
        self.hook_url = self.host + '/hook'
        self.status_url = self.host + '/status'

        if self.cookies is None:
            try:
                r = requests_session.post(self.login_url,
                                          verify=False,
                                          data={'username': username,
                                                'password': password,
                                                'eauth': eproto
                                                },
                                          timeout=3
                                          )
                if r.status_code == 200:
                    self.cookies = r.cookies
                    # print(r.text)
                    # print(r.cookies)
                else:
                    raise Exception(f'Error from source {r.text}')
            except Exception as e:
                print(e)

    def cmd_run(self, tgt,
                arg=None, fun='cmd.run',
                expr_form='compound', timeout=600):
        try:
            if arg:
                r = requests_session.post(
                    self.host,
                    verify=False,
                    cookies=self.cookies,
                    data={
                        'client': 'local',
                        'tgt': tgt,
                        'expr_form': expr_form,
                        'fun': fun,
                        'arg': arg,
                        'timeout': timeout
                    }
                )
            else:
                r = requests_session.post(
                    self.host,
                    verify=False,
                    cookies=self.cookies,
                    data={
                        'client': 'local',
                        'tgt': tgt,
                        'expr_form': expr_form,
                        'fun': fun,
                        'timeout': timeout
                    }
                )
            if r.status_code == 200:
                return r.json()
            else:
                raise Exception(f'Error from source {r.text}')
        except Exception as e:
            print(e)

    def cmd_script(self, tgt, arg,
                   expr_form='compound', timeout=600):
        fun = 'cmd.script'
        try:
            r = requests_session.post(
                self.host,
                verify=False,
                cookies=self.cookies,
                data={
                    'client': 'local',
                    'tgt': tgt,
                    'expr_form': expr_form,
                    'fun': fun,
                    'arg': arg,
                    'timeout': timeout
                }
            )
            if r.status_code == 200:
                return r.json()
            else:
                raise Exception(f'Error from source {r.text}')
        except Exception as e:
            print(e)

    def cp_file(self, tgt, from_path, to_path,
                expr_form='compound', timeout=600):
        fun = 'cp.get_file'
        try:
            r = requests_session.post(
                url=self.host, verify=False, cookies=self.cookies,
                data={
                    'client': 'local',
                    'tgt': tgt,
                    'expr_form': expr_form,
                    'fun': fun,
                    'arg': [from_path, to_path],
                    'timeout': timeout,
                    'makedirs': 'True',
                }
            )
            if r.status_code == 200:
                return r.json()
            else:
                raise Exception(f'Error from source {r.text}')
        except Exception as e:
            print(e)

    def cp_dir(self, tgt, from_path, to_path,
               expr_form='compound', timeout=600):
        fun = 'cp.get_dir'
        try:
            r = requests_session.post(
                url=self.host, verify=False, cookies=self.cookies,
                data={
                    'client': 'local',
                    'tgt': tgt,
                    'expr_form': expr_form,
                    'fun': fun,
                    'arg': [from_path, to_path],
                    'timeout': timeout,
                    'makedirs': 'True',
                }
            )
            if r.status_code == 200:
                return r.json()
            else:
                raise Exception(f'Error from source {r.text}')
        except Exception as e:
            print(e)


def salt_api_inst():
    return SaltStack(host=HOST,
                     port=PORT,
                     username=USERNAME,
                     password=PASSWORD,
                     secure=SECURE,
                     eproto=EPROTO)


def demo():
    attach_arg_list = [None] * 9
    attach_arg_list[0] = "ZEP-BACKEND-JAVA"
    attach_arg_list[1] = "test"
    # attach_arg_list[2] = "2020-0213-2334-34XZ"
    attach_arg_list[2] = "2020-02-25-002806TO"
    attach_arg_list[3] = "javademo-1.0.jar"
    attach_arg_list[4] = "18080"
    attach_arg_list[5] = "stop"
    attach_arg_list[6] = "tot"
    attach_arg_list[7] = "http://www.yanxin.com"
    # attach_arg_list[8] = "javademo-1.0.tar.gz"
    attach_arg_list[8] = "haha.tar.gz"

    attach_arg = ' '.join(attach_arg_list)
    s = salt_api_inst()
    tgt = '192.168.12.107'
    scripts_url = 'http://192.168.12.103:9999/scripts/start_demo.sh'
    result = s.cmd_script(tgt, arg=[scripts_url, attach_arg,
                                    'runas=root', 'env={"LC_ALL":""}'])
    # print(result['return'])
    print(result['return'][0][tgt]['stdout'])
    # scripts_url = 'http://192.168.12.103:9999/scripts/test.sh'
    # print(s.cmd_run(tgt, fun='test.ping'))
    # print(s.cmd_script(tgt, arg=[scripts_url,"ens32 ens33"]).get('return')[0].get(tgt).get('stdout'))
    # print(s.cp_file(tgt,'salt://a/b/c/1.txt','/tmp/'))
    # print(s.cp_dir(tgt, 'salt://a', '/tmp/'))


if __name__ == '__main__':
    demo()
