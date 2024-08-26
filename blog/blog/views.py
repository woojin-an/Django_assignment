from django.shortcuts import render, get_object_or_404, redirect

from blog.models import Blog


def blog_list(request):
    blogs = Blog.objects.all()
    context = {
            'blogs': blogs,
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