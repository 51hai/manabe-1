from django import forms


class RegisterForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='用户名',
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder': '账号',
                'rows': 1,
                'class': 'input-text size-L',
            }
        )
    )
    email = forms.EmailField(
        required=True,
        label='邮箱',
        error_messages={'required': '请输入电子邮箱'},
        widget=forms.TextInput(
            attrs={
                'placeholder': '此邮箱用于密码找回',
                'rows': 1,
                'class': 'input-text size-L'
            }
        )
    )
    password = forms.CharField(
        required=True,
        error_messages={'required': '请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '密码',
                'rows': 1,
                'class': 'input-text size-L'
            }
        )
    )
    password2 = forms.CharField(
        required=True,
        error_messages={'required': '请再次输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '确认密码',
                'rows': 1,
                'class': 'input-text size-L'
            }
        )
    )

    @staticmethod
    def pwd_validate(p1, p2):
        return p1 == p2


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label='用户名',
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'class': 'input-text size-L',
                'placeholder': '账号',
                'rows': 1
            }
        )
    )

    password = forms.CharField(
        required=True,
        label='密码',
        error_messages={'required': '请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': '密码',
                'rows': 1,
                'class': 'input-text size-L'
            }
        )
    )


class ChangeEmailForm(forms.Form):
    new_email1 = forms.EmailField(
        required=True,
        error_messages={'required': '请输入新邮箱地址'},
        label='新邮箱地址',
        widget=forms.TextInput(
            attrs={
                'placeholder': '新邮箱地址',
                'rows': 1,
                'class': 'input-text size-L'
            }
        )
    )

    new_email2 = forms.EmailField(
        required=True,
        label='新邮箱地址',
        error_messages={'required': '请再次输入新邮箱地址'},
        widget=forms.TextInput(
            attrs={
                'placeholder': '确认新邮箱地址',
                'rows': 1,
                'class': 'input-text size-L'
            }
        )
    )

    def clean(self):
        print(self.cleaned_data, "% % % % % % % %")
        if not self.is_valid():
            raise forms.ValidationError('所有项都为必填项')
        elif self.changed_data['new_email1'] != self.changed_data['new_email2']:
            print('****************')
            raise forms.ValidationError('俩次输入的邮箱地址不一样')
        else:
            cleaned_data = super(ChangeEmailForm, self).clean()
            print('&&&&&&&&&&&&&&&')
            print(cleaned_data)
        return cleaned_data;
