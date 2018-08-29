from django import forms
from django.contrib import auth
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入用户名'}))
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username, password=password)
        if user is None:
            raise forms.ValidationError("用户名或者密码不正确")
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data


class RegForm(forms.Form):
    username = forms.CharField(label='用户名',
                               max_length=30,
                               min_length=3,
                               widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'请输入3-30位用户名'}))
    email = forms.EmailField(label='邮箱',
                             widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'请输入邮箱'}))
    password = forms.CharField(label='密码',
                               min_length=6,
                               widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'请输入密码'}))
    password_again = forms.CharField(label='再输入一次密码',
                                     min_length=6,
                                     widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'再输入一次密码'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已存在')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_again


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, min_length=3, label='表格名称',widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请按提示输入'}))
    file = forms.FileField(label='上传表格文件进行分析')
    is_row = forms.BooleanField(label='是否纵向',required=False)

    def clean(self):
        title = self.cleaned_data['title']
        file = self.cleaned_data['file']
        is_row = self.cleaned_data['is_row']

        if not file.name[-3:] == 'xls':
            raise forms.ValidationError('请上传‘.xls’表格文件')
        return self.cleaned_data
