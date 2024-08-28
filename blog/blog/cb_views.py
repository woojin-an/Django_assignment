from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(ListView):
    queryset = Blog.objects.all()
    template_name = 'blog/blog_list.html'
    paginate_by = 10
    ordering = ['-created_at']  # 최신순 정렬

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(content__icontains=q)
            )
        return queryset


class BlogDetailView(DetailView):
    queryset = Blog.objects.all()
    template_name = 'blog/blog_detail.html'

    # def get_object(self):
    #     object = super().get_object()
    #     return object
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['blog'] = Blog.objects.get(pk=self.kwargs['pk'])
    #     return context
    #
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(id__lte=50)


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog/blog_create.html'
    fields = ('category', 'title', 'content')

    # form_class = BlogForm
    # success_url = reverse_lazy('cb_blog_detail', kwargs={'pk': object.pk})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    # def get_success_url(self):
    #     return reverse_lazy('blog_detail', kwargs={'pk': self.object.pk})


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name = 'blog/blog_update.html'
    fields = ('category', 'title', 'content')

# 로그인한 유저와 게시글 작성자가 일치하는지 확인
    def get_queryset(self):
        queryset = super().get_queryset()
        # 요청자(삭제요청자)가 관리자권한이 없다면
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)

        return queryset
    # def get_object(self, queryset=None):
    #     self.object = super().get_object(queryset)
    #
    #     if self.object.author != self.request.user:
    #         raise Http404
    #     return self.object
    # def get_success_url(self):
    #     return reverse_lazy('cb_blog_detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog

    def get_queryset(self):
        queryset = super().get_queryset()
        # 요청자(삭제요청자)가 관리자권한이 없다면
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)

        return queryset

    def get_success_url(self):
        return reverse_lazy('blog:list')
