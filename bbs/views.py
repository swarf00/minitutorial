from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.views.generic import TemplateView

from bbs.models import Article


class ArticleListView(TemplateView):
    template_name = 'article_list.html'
    queryset = Article.objects.all()

    def get(self, request, *args, **kwargs):
        ctx = {
            'articles': self.queryset
        }
        return self.render_to_response(ctx)


class ArticleDetailView(TemplateView):
    template_name = 'article_detail.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        article = queryset.filter(pk=pk).first()

        if not article:
            raise Http404('invalid pk')
        return article

    def get(self, request, *args, **kwargs):
        article = self.get_object()

        ctx = {
            'article': article
        }
        return self.render_to_response(ctx)


class ArticleCreateUpdateView(LoginRequiredMixin, TemplateView):
    login_url = settings.LOGIN_URL
    template_name = 'article_update.html'
    queryset = Article.objects.all()
    pk_url_kwargs = 'article_id'

    def get_object(self, queryset=None):
        queryset = queryset or self.queryset
        pk = self.kwargs.get(self.pk_url_kwargs)
        article = queryset.filter(pk=pk).first()

        if pk:
          if not article:
            raise Http404('invalid pk')
          elif article.author != self.request.user:                             # 작성자가 수정하려는 사용자와 다른 경우
            raise Http404('invalid user')
        return article

    def get(self, request, *args, **kwargs):
        article = self.get_object()

        ctx = {
            'article': article,
        }
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        post_data = {key: request.POST.get(key) for key in ('title', 'content')} # 작성자를 입력받지 않도록 수정
        for key in post_data:
            if not post_data[key]:
                messages.error(self.request, '{} 값이 존재하지 않습니다.'.format(key), extra_tags='danger')

        post_data['author'] = self.request.user

        if len(messages.get_messages(request)) == 0:
            if action == 'create':
                article = Article.objects.create(**post_data)
                messages.success(self.request, '게시글이 저장되었습니다.')
            elif action == 'update':
                article = self.get_object()
                for key, value in post_data.items():
                    setattr(article, key, value)
                article.save()
                messages.success(self.request, '게시글이 저장되었습니다.')
            else:
                messages.error(self.request, '알 수 없는 요청입니다.', extra_tags='danger')

            return HttpResponseRedirect('/article/')

        ctx = {
            'article': self.get_object() if action == 'update' else None
        }
        return self.render_to_response(ctx)


def hello(request, to):
    return HttpResponse('Hello {}.'.format(to))