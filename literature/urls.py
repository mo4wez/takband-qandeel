from django.urls import path
from .views import poems_by_author_name

urlpatterns = [
    path('poems/<str:author_name>/', poems_by_author_name, name='poems-by-author'),
]
