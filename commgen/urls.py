"""dummy_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path
from django.conf.urls import url
from myapp.views import MyView
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from schedule.periods import Day, Month, Week, Year
from . import settings
urlpatterns = [
    path('accounts/', include('users.urls')),
	path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('schedule/', include('schedule.urls')),
    path('campaign/', include('myapp.urls')),
    path('accounts/login/', auth_views.login, name='login'),
    url(r'^$', MyView.as_view(), name='home',kwargs={'period': Month,'calendar_slug':'dashboard'}),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    ]
# urlpatterns += i18n_patterns(
#     path('admin/', admin.site.urls),
#     path('home/', home),
# )
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)