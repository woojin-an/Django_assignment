from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from todo.forms import TodoForm
from todo.models import Todo


@login_required
def todo_list(request):
    todo_list = Todo.objects.all()
    q = request.GET.get('q')
    if q:
        # 제목과 내용으로 검색할 수 있도록 필터설정
        todo_list = todo_list.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q)
        )

    paginator = Paginator(todo_list, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'page_obj': page_obj,
        'todo_list': todo_list,

    }

    return render(request, 'todo_list.html', context)


@login_required
def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    context = {
        'id': todo.id,
        'title': todo.title,
        'description': todo.description,
        'start_date': todo.start_date,
        'end_date': todo.end_date,
        'is_completed': todo.is_completed,
        'todo': todo,
    }

    return render(request, 'todo_info.html', context)


@login_required
def todo_create(request):
    form = TodoForm(request.POST or None)
    if form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect(reverse('todo_list'))

    context = {
        'form': form,
    }

    return render(request, 'todo_create.html', context)


@login_required     # 버전 관리(revision), 작성 중 저장(db 저장..?), 뒤로가기(목록), 변경사항(다른 점)
def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    form = TodoForm(request.POST or None, instance=todo)
    if form.is_valid():
        todo = form.save()
        return redirect(reverse('todo_list'))
    context = {
        'form': form,
        'todo': todo,
    }
    return render(request, 'todo_update.html', context)


@login_required
@require_http_methods(['POST'])
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    todo.delete()
    return redirect(reverse('todo_list'))
