from django.contrib.auth.models import User
from django import forms
from .models import App


class AppForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        # required的值默认为True，所以当可为空时才需要专门指定为False
        # error_messages的效果没看出来
        required=True,
        error_messages={'required': '不能为空'},
        label='App组件名称',
        widget=forms.TextInput(
            attrs={
                'placeholder': '名称',
                'class': 'input-text'
            }
        )
    )

    description = forms.CharField(
        required=False,
        label='描述',
        widget=forms.Textarea(
            attrs={
                'placeholder': '描述',
                'class': 'input-text'
            }
        )
    )

    jenkins_job = forms.CharField(
        label='JENKINS JOB名称',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Jenkins Job',
                'class': 'input-text'
            }
        )
    )

    git_url = forms.CharField(
        label='GIT地址',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'GIT地址',
                'class': 'input-text'
            }
        )
    )

    dir_build_file = forms.CharField(
        label='编译目录',
        widget=forms.TextInput(
            attrs={
                'placeholder': '编译目录',
                'class': 'input-text'
            }
        )
    )

    build_cmd = forms.CharField(
        label='编译命令',
        widget=forms.TextInput(
            attrs={
                'placeholder': '编译命令',
                'class': 'input-text'
            }
        )
    )
    package_name = forms.CharField(
        required=False,
        label='软件包名称',
        widget=forms.TextInput(
            attrs={
                'placeholder': '编译后的软件包名称',
                'class': 'input-text'
            }
        )
    )
    zip_package_name = forms.CharField(
        required=False,
        label='压缩包名称',
        widget=forms.TextInput(
            attrs={
                'placeholder': '软件包和配置文件集成的压缩包',
                'class': 'input-text'
            }
        )
    )

    is_restart_status = forms.CharField(
        label='重启服务',
        widget=forms.CheckboxInput(
            attrs={
                'class': 'radio-box',
            }
        )
    )
    manage_user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='管理员',
        widget=forms.Select(
            attrs={
                'style': """width:40%;""",
                'class': 'select-box'
            }
        )
    )
    script_url = forms.CharField(
        required=False,
        label='app脚本链接',
        widget=forms.TextInput(
            attrs={
                'class': 'input-text',
                'placeholder': 'http://[nginx]/scripts/[app_name]/[script_name]'
            }
        )
    )

    class Meta:
        model = App
        exclude = ['op_log_no']
