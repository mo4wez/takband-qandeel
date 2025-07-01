from django.shortcuts import render

from .models import Poem

# Create your views here.
def poems_by_author_name(request, author_name: str):
    poems = Poem.objects.filter(work__group__author__name=author_name, is_published=True)
    
    return render(request, 'index.html', {'poems': poems, 'author': author_name})