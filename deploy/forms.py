from django import forms
from .models import DeployPool
from appinput.models import App

IS_INC_TOT_CHOICES = (
    ('TOT', '全量部署'),
    ('INC', '增量部署'),
)

DEPLOY_TYPE_CHOICES = (
    ('deployall', '发布所有'),
    ('deploypkg', '发布程序'),
    ('deploycfg', '发布配置'),
)


class DeployForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        kwargs['initial'] = initial
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        # 这里一定要是required=False，
        # 因为发布单名称要靠程序来生成，
        # 这里输入框是只显示但不允许用户填写，因为设置了disabled属性
        required=False,
        label='发布单名称',
        widget=forms.TextInput(
            attrs={
                'placeholder': '自动生成',
                'class': 'input-text',
                'disabled': 'disabled',
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

    branch_build = forms.CharField(
        label='Git分支',
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Git分支',
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

    is_inc_tot = forms.CharField(
        label='部署方式',
        widget=forms.Select(
            choices=IS_INC_TOT_CHOICES,
            attrs={
                'class': 'select-box'
            }
        )
    )

    deploy_type = forms.CharField(
        label='部署类型',
        widget=forms.Select(
            choices=DEPLOY_TYPE_CHOICES,
            attrs={
                'class': 'select-box'
            }
        )
    )

    class Meta:
        model = DeployPool
        fields = ('name', 'description', 'app_name',
                  'branch_build', 'is_inc_tot', 'deploy_type')


class UploadFileForm(forms.Form):
    name = forms.CharField(
        # 这里一定要是required=False，
        # 因为发布单名称要靠程序来生成，
        # 这里输入框是只显示但不允许用户填写，因为设置了disabled属性
        required=False,
        label='发布单名称',
        widget=forms.TextInput(
            attrs={
                'placeholder': '自动生成',
                'class': 'input-text',
                'disabled': 'disabled',
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

    is_inc_tot = forms.CharField(
        label='部署方式',
        widget=forms.Select(
            choices=IS_INC_TOT_CHOICES,
            attrs={
                'class': 'select-box'
            }
        )
    )

    deploy_type = forms.CharField(
        label='部署类型',
        widget=forms.Select(
            choices=DEPLOY_TYPE_CHOICES,
            attrs={
                'class': 'select-box'
            }
        )
    )

    file_path = forms.CharField(
        required=False,
        label='上传文件',
        widget=forms.TextInput(
            attrs={
                'rows': 2,
                'placeholder': '上传后自动生成'
            }
        )
    )

    class Meta:
        model = DeployPool
        fields = ('name', 'description', 'app_name', 'is_inc_tot', 'deploy_type')
