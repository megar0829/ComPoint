from django import forms
from .models import Post, Comment
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='제목',
        label_suffix='',
        widget=forms.TextInput(
            attrs={
                'class': 'my-title form-control form-div',
                'placeholder': '제목을 입력해주세요.',
                'maxlength': 30,
            }
        )
    )
    content = forms.CharField(
        label='본문',
        label_suffix='',
        widget=CKEditorWidget(),
        error_messages={
            'required': '내용을 입력해 주세요.'
        }
    )

    # model 등록
    class Meta:
        model = Post
        exclude = ('user', 'like_users', 'category', 'image',)
        

class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        label_suffix='',
        widget=forms.TextInput(attrs={
            'class': 'form-control ',
            'placeholder': '댓글을 작성해주세요.',
            'style' : 'width: 540px; height : 50px;',
            }),
    )
    class Meta:
        model = Comment
        fields = ('content',)
        

