from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.http import HttpResponseRedirect
from django.urls import reverse

from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    queryset = Blog.objects.all()
    template_name = 'list.html'


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ('title', 'content', 'published_at',)
    template_name = 'form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return HttpResponseRedirect(
            reverse('blog_list')
        )
