from django.contrib import admin
from todo.models import Todo, Comment


class CommnetInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('message', 'author')


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'title', 'description', 'is_completed', 'start_date', 'end_date')
    list_filter = ('is_completed',)
    search_fields = ('title',)
    ordering = ('start_date',)
    list_display_links = ('title',)
    fieldsets = (
        ('Todo Info', {
            'fields': ('author', 'title', 'description', 'completed_image', 'is_completed',)
        }),
        ('Date Range', {
            'fields': ('start_date', 'end_date',)
        }),
    )
    inlines = [CommnetInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'todo', 'author', 'message', 'created_at')
    list_filter = ('todo', 'author')
    search_fields = ('message', 'author')
    ordering = ('-created_at',)
    list_display_links = ('message',)
    fieldsets = (
        ('Comment Info', {
            'fields': ('todo', 'author', 'message')
        }),
    )