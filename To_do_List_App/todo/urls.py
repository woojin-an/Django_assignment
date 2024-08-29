from django.urls import path, include

from todo.cb_views import TodoListView, TodoDetailView, TodoCreateView, TodoUpdateView, TodoDeleteView, \
    CommentUpdateView, CommentDeleteView, CommentCreateView

urlpatterns = [
    # CBV
    path('todo/', TodoListView.as_view(), name='cbv_todo_list'),
    path('todo/<int:pk>/', TodoDetailView.as_view(), name='cbv_todo_info'),
    path('create/', TodoCreateView.as_view(), name='cbv_todo_create'),
    path('todo/<int:pk>/update/', TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('todo/<int:pk>/delete/', TodoDeleteView.as_view(), name='cbv_todo_delete'),
    path('comment/<int:todo_id>/create/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:todo_id>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:todo_id>/delete/', CommentDeleteView.as_view(), name='comment_delete'),

]