import os
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .forms import ChangeEmailForm


@login_required()
@require_http_methods(['GET', 'POST'])
def change_email(request):
    error = []
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)
        username = request.user.username
        new_email = request.POST.get('new_email1')
        User.objects.filter(username__iexact=username). \
            update(email=new_email)
        email = User.objects.get(username=username).email
        change_email_success = True
        return render(request, 'accounts/change_email.html', locals())
    else:
        form = ChangeEmailForm()
        var_dict = {
            'form': form,
            'current_page_name': '更改邮箱',
            'email': User.objects.get(username=request.user.username).email
        }
        return render(request, 'accounts/change_email.html', var_dict)
