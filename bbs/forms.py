from django.forms import ModelForm

from bbs.models import Article


class ArticleForm(ModelForm):

    class Meta:
        model = Article
        fields = [
            'title', 'content', 'author'
        ]