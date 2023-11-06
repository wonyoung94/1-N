from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = '__all__'

        # fields :  추가할 필드 이름 (~를 다 보여줘)
        # fields = ('content',)
        #exclude : 제외할 필드 이름 (~ 빼고 다 보여줘)
        exclude = ('article',)