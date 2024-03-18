from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import get_user_model
from django.forms import TextInput, EmailInput, PasswordInput
from django.utils.safestring import SafeString

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = '비밀번호'
        self.fields['password2'].label = '비밀번호 확인'
        self.fields['password1'].widget =  PasswordInput(attrs={
                'class':'form-control shadow-sm',
                'style' : 'width: 100%;',
                'placeholder':'최소 8자 이상 (숫자로만 이루어질 수 없습니다.)',
            })
        self.fields['password2'].widget = PasswordInput(attrs={
                'class':'form-control shadow-sm',
                'style' : 'width: 100%;',
                'placeholder': '비밀번호 확인'
            })

        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    # def as_div(self):
    #     return SafeString(super().as_div().replace("<div>", "<div class='form-floating'>"))
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'nickname', 'email')
        labels = {
            'username':'아이디',
            'nickname':'닉네임',
            'email':'이메일',
        }
        help_texts = {
            'username':'',
            'password1':'test',
        }
        widgets = {
            'username': TextInput(attrs={
                'class':'form-control shadow-sm',
                'style' : 'width: 100%;',
                'placeholder':'4~15자 이내로 입력해주세요.',
            }),
            'nickname': TextInput(attrs={
                'class':'form-control shadow-sm',
                'style' : 'width: 100%;',
                'placeholder':'별명을 알파벳, 한글, 숫자로 20자 이하로 입력해주세요.'
            }),
            'email' : EmailInput(attrs={
                'class':'form-control shadow-sm',
                'style' : 'width: 100%;',
                'placeholder':'example@compoint.com'
            }),
        }


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('nickname', 'email')

    nickname = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={
            'class': 'form-control  shadow-sm',
            'placeholder': 'nickname',
            'style' : 'width: 100%;',
            }),
        required=False)

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control  shadow-sm',
            'placeholder': 'email',
            'style' : 'width: 100%;',
            }),)
    
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['nickname'].label = '닉네임'
        self.fields['email'].label = '이메일'
        self.fields.pop('password')


class MyAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '아이디'
        self.fields['password'].label = '비밀번호'
        self.fields['username'].widget = forms.widgets.TextInput(attrs={
                'class': 'form-control  shadow-sm',
                'style' : 'width: 100%;',
            })
        self.fields['password'].widget = forms.widgets.PasswordInput(attrs={
                'class': 'form-control  shadow-sm',
                'style' : 'width: 100%;',
            })
        

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].label = '기존 비밀번호'
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control  shadow-sm',
            'autofocus': False,
        })
        self.fields['new_password1'].label = '새 비밀번호'
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control  shadow-sm',
        })
        self.fields['new_password1'].help_text = ''

        self.fields['new_password2'].label = '새 비밀번호 확인'
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control  shadow-sm',
        })