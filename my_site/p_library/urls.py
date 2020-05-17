from django.urls import path
from .views import AuthorEdit, AuthorList, author_create_many, books_authors_create_many

urlpatterns = [
    path('create', AuthorEdit.as_view(), name='author_create'),
    path('', AuthorList.as_view(), name='author_list'),
    path('create_many', author_create_many, name='author_create_many'),
    path('create_book_many', books_authors_create_many, name='author_book_create_many'),
]
