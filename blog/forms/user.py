from django import forms
from django.contrib.auth import authenticate
from django.conf import settings
from blog.models import ForumUser
from django.forms import ModelForm


error_messages = {
    'username': {
        'required': u'必须填写用户名',
        'min_length': u'用户名长度过短（3-12个字符）',
        'max_length': u'用户名长度过长（3-12个字符）',
        'invalid': u'用户名格式错误（英文字母开头，数字，下划线构成）'
    },
    'email': {
        'required': u'必须填写E-mail',
        'min_length': u'Email长度有误',
        'max_length': u'Email长度有误',
        'invalid': u'Email地址无效'
    },
    'password': {
        'required': u'必须填写密码',
        'min_length': u'密码长度过短（6-64个字符）',
        'max_length': u'密码长度过长（6-64个字符）'
    },
}

class TopicForm(forms.Form):
    title = forms.CharField(min_length=6, max_length=64,
                               error_messages=error_messages.get('title'))


class VideoFileForm(forms.Form):
    id = forms.CharField(required=False,
                           error_messages={'required': "邮箱不能为空"})
    video = forms.FileField(required=True,
                           error_messages={'required': "video不能为空"})
    def clean_video(self):
        mp4 = self.cleaned_data['video']
        if not mp4.name.endswith('mp4'):
            raise forms.ValidationError(u'不是mp4格式')
        return mp4

class fileForm(forms.Form):
    id = forms.CharField(required=False,
                           error_messages={'required': "邮箱不能为空"})
    file = forms.FileField(required=True,
                            error_messages={'required': "video不能为空"})


class LoginForm(forms.Form):
    email = forms.EmailField(required=False,
        error_messages=error_messages.get('email'))
    username = forms.CharField(required=False)
    password = forms.CharField(min_length=6, max_length=64,
        error_messages=error_messages.get('password'))

    def __init__(self, *args, **kwargs):
        self.user_cache = None;
        super(LoginForm, self).__init__(*args,**kwargs)

    def clean(self):
        username = self.cleaned_data.get('email')
        user_name = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        # username = user_name if user_name.strip() != '' else email
        if username and password:
            self.user_cache = authenticate(username=username,password=password)
            if self.user_cache is None:
                print('邮箱或者密码不正确')
                raise forms.ValidationError(u'邮箱或者密码不正确')
            elif not self.user_cache.is_active:
                print('邮箱或者密码不正确')
                raise forms.ValidationError(u'用户被锁定，请联系管理员')
        return self.cleaned_data;
    def get_user(self):
        return self.user_cache

class RegisterForm(forms.ModelForm):
    username = forms.RegexField(min_length=3, max_length=12,
        regex=r'^[a-zA-Z][a-zA-Z0-9_]*$',
        error_messages=error_messages.get('username'))
    email = forms.EmailField(min_length=4, max_length=64,
        error_messages=error_messages.get('email'))
    password = forms.CharField(min_length=6, max_length=64,
        error_messages=error_messages.get('password'))
    password_confirm = forms.CharField(required=False),
    nickname = forms.CharField(required=False,error_messages={'required': "昵称不能为空"})

    class Meta:
        model = ForumUser
        fields = ('username', 'email','nickname')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            ForumUser.objects.get(username=username)
            raise forms.ValidationError(u'所填用户名已经被注册过')
        except ForumUser.DoesNotExist:
            if username in settings.RESERVED:
                raise forms.ValidationError(u'用户名被保留不可用')
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            ForumUser.objects.get(email=email)
            raise forms.ValidationError(u'所填邮箱已经被注册过')
        except ForumUser.DoesNotExist:
            return email

    def clean_password_confirm(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password_confirm')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u'两次输入密码不一致')
        return password2

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        return nickname

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user