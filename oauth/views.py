from django.shortcuts import render
from django.conf import settings
from .oauth_client import OAuth
from django.shortcuts import HttpResponseRedirect
from .models import OAuthyb
from django.contrib import auth
from django.urls import reverse
from .forms import YBLoginForm, YBRegForm
from django.contrib.auth.models import User

# Create your views here.

def yb_login(request):
    oauth_yb = OAuth(settings.APPID, settings.APPSECRET, settings.CALLBACK)
    url = oauth_yb.get_auth_url()
    return HttpResponseRedirect(url)

def yb_check(request):
    request_code = request.GET.get('code')
    oauth_yb = OAuth(settings.APPID, settings.APPSECRET, settings.CALLBACK)
    access_token = oauth_yb.get_access_token(request_code)

    print('access_key=%s' % access_token)

    # 获取用户信息
    infos = oauth_yb.get_yb_info()
    if infos['status'] == 'success':
        user_id = infos['info']['yb_userid']
        user_name = infos['info']['yb_username']
        # ORM查找易班id是否已绑定
        id_models = OAuthyb.objects.filter(yb_id=user_id)
        # 已绑定登录
        if id_models:
            user = id_models[0].user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            auth.login(request, user)
            return HttpResponseRedirect(reverse('home'))
        # 未登录，携带信息跳转到跳转到绑定页面
        else:
            url = '%s?user_id=%s&user_name=%s' % (reverse('yb_bind'), user_id, user_name)
            return HttpResponseRedirect(url)
    # 获取用户信息失败返回错误信息
    else:
        context = {}
        context['message'] = infos['info']['msgCN']
        return render(request, 'message.html', context)


def yb_bind(request):
    if request.method == 'POST':
        reg_form = YBRegForm(request.POST)
        if reg_form.is_valid():

            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']

            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()

            user_id = reg_form.cleaned_data['user_id']

            oauth_obj = OAuthyb()
            oauth_obj.yb_id = user_id
            oauth_obj.user = user
            oauth_obj.save()
            auth.login(request, user)
            return HttpResponseRedirect(reverse('home'))
    else:
        login_form = YBRegForm()
    context = {}
    context['login_form'] = YBRegForm
    context['user_id'] = request.GET.get('user_id')
    context['user_name'] = request.GET.get('user_name')
    return render(request, 'yb_login_bind.html', context)
