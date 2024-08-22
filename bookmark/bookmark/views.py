from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from bookmark.models import Bookmark
from django.http import Http404

def bookmark_list(request):
    bookmarks = Bookmark.objects.filter(id__gte=50)

    context = {
        'bookmarks': bookmarks
    }
    return render(request, template_name='bookmark_list.html', context=context)


def bookmark_detail(request, pk):
    # try:
    #     bookmark = Bookmark.objects.get(pk=pk)
    # except:
    #     raise Http404("Bookmark not found")
    bookmark = get_object_or_404(Bookmark, pk=pk)
    context = {'bookmark': bookmark}

    return render(request, template_name='bookmark_detail.html', context=context)