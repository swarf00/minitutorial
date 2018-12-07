from django.contrib import admin

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'date_created')
    list_display_links = ('id', 'title')

    def date_created(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")
    date_created.admin_order_field = 'created_at'
    date_created.short_description = '작성일'
