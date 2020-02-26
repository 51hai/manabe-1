from django import forms
from .models import Server
from appinput.models import App
from envx.models import Env


class ServerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        label='服务器名称',
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

    ip_address = forms.CharField(
        label='IP',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'IP地址',
                'class': 'input-text'
            }
        )
    )

    port = forms.CharField(
        label='端口',
        widget=forms.TextInput(
            attrs={
                'placeholder': '端口',
                'class': 'input-text'
            }
        )
    )

    salt_name = forms.CharField(
        label='SaltStack minion名称',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'SaltStack minion名称',
                'class': 'input-text'
            }
        )
    )

    app_name = forms.ModelChoiceField(
        label='应用名称',
        queryset=App.objects.all(),
        widget=forms.Select(
            attrs={
                'style': """width:40%;""",
                'class': 'select-box'
            }
        )
    )
    env_name = forms.ModelChoiceField(
        label='所属环境',
        queryset=Env.objects.all(),
        widget=forms.Select(
            attrs={
                'style': """width:40%;""",
                'class': 'select-box'
            }
        )
    )
    app_user = forms.CharField(
        label='启动用户',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'root',
                'class': 'input-text'
            }
        )
    )

    class Meta:
        model = Server
        fields = ('name', 'description',
                  'ip_address', 'salt_name',
                  'port', 'app_user',
                  'app_name', 'env_name')
