from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from blog.models import Blog, Comment

admin.site.register(Comment)


class CommentInline(admin.TabularInline):   # 댓글을 표 형태로 만들어서
    model = Comment
    fields = ['content', 'author']


@admin.register(Blog)
class BlogAdmin(SummernoteModelAdmin):          # 게시글에 댓글이 들어가도록
    summernote_fields = ['content',]
    inlines = [
        CommentInline
    ]
