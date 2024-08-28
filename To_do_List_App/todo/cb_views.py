from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from todo.models import Todo


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todo_list.html'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
    # 관리자 권한이 있을 때 모든 객체를 볼 수 있도록
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)

        q = self.request.GET.get('q')
    # 검색 기능(제목, 내용)
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )
        return queryset


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todo_info.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 글을 조회할 권한이 없습니다.")

        return obj

    def get_context_data(self, **kwargs):
        context = {'todo': self.object.__dict__}
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    template_name = 'todo_create.html'
    fields = ('title', 'description', 'start_date', 'end_date')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.pk})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    template_name = 'todo_update.html'
    fields = ('title', 'description', 'start_date', 'end_date')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # 요청자가 작성자가 아니거나 관리자가 아니라면
        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 게시글을 수정할 권한이 없습니다.")

        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.pk})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.author != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 게시글을 삭제할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')