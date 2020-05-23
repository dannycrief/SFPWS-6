"""my_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from p_library import views
from django.conf.urls.static import static
from allauth.account.views import login, logout, signup
from p_library.views import profile, CreateUserProfile

urlpatterns = [
    path('admin/', admin.site.urls),
    path('library/', views.index, name='my-library'),
    path('index/book_increment/', views.book_increment),
    path('index/book_decrement/', views.book_decrement),
    path('publishes/', views.redactions, name='publishes'),
    path('authors/', include('p_library.urls')),
    path('accounts/', include('allauth.urls')),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', signup, name='register'),
    path('profile/', profile, name='profile-page'),
    path('profile-create/', CreateUserProfile.as_view(), name='profile-create'),
    path('', views.index_redirect),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
