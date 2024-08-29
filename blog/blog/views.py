from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect, Http404
from django.urls import reverse
from blog.models import Blog
from blog.forms import BlogForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods


def blog_list(request):
    blogs = Blog.objects.all().order_by('-created_at')

    q = request.GET.get('q')
    if q:
        blogs = blogs.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )
        # blogs = blogs.filter(title__icontains=q)

    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    page_object = paginator.get_page(page)

    context = {
            'object_list': page_object.object_list,
            'page_obj': page_object,
        }
    return render(request, 'blog/blog_list.html', context)

# 쿠키와 세션에서 사용한 blog_list
# def blog_list(request):
#     blogs = Blog.objects.all()
#
#     visits = int(request.COOKIES.get('visits', 0)) + 1
#
#     request.session['count'] = request.session.get('count', 0) + 1
#
#     context = {
#         'blogs': blogs,
#         'count': request.session['count'],
#     }
#
#     response = render(request, 'blog/blog_list.html', context=context)
#     response.set_cookie('visits', visits)
#     return response


def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    context = {'blog': blog}
    return render(request, 'blog/blog_detail.html', context=context)


@login_required()
def blog_create(request):
    # if not request.user.is_authenticated:
    #     return redirect(reverse('login'))
    form = BlogForm(request.POST or None)
    if form.is_valid():
        blog = form.save(commit=False)
        blog.author = request.user
        blog.save()
        return redirect(reverse('fb:detail', kwargs={'pk': blog.pk}))

    context = {'form': form}
    return render(request, 'blog/blog_form.html', context)


@login_required()
def blog_update(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    # if request.user != blog.author:     # 작성자와 로그인정보가 다를 때
    #     raise Http404
    form = BlogForm(request.POST or None, instance=blog)
    if form.is_valid():
        blog = form.save()
        return redirect(reverse('fb:detail', kwargs={'pk': blog.pk}))
    context = {
        'form': form,
        'blog': blog,
    }
    return render(request, "blog/blog_form.html", context)


@login_required()
@require_http_methods(['POST'])
def blog_delete(request, pk):
    # if request.method != 'POST':
    #     raise Http404
    blog = get_object_or_404(Blog, pk=pk, author=request.user)
    blog.delete()

    return redirect(reverse('fb:list'))
