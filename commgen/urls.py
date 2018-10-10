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
from myapp.views import home,MyView,LoadCalendar,load_prevnext_calendar
from django.conf.urls import include
from django.conf.urls.i18n import i18n_patterns
from django.contrib.auth import views as auth_views
from schedule.periods import Day, Month, Week, Year
from . import settings
urlpatterns = [
	path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    # path('', home,name = 'home'),
    # path('ajax/load_prevnext_calendar', load_prevnext_calendar,name = 'load_prevnext_calendar',kwargs={'calendar_slug':'calendar1','period': Month}),
    path('ajax/load_prevnext_calendar', LoadCalendar.as_view(),name = 'load_prevnext_calendar',kwargs={'calendar_slug':'calendar1','period': Month}),
    path('schedule/', include('schedule.urls')),
    path('campaign/', include('myapp.urls')),
    path('login/', auth_views.login, name='login'),
    url(r'^(?P<calendar_slug>[-\w]+)/$', MyView.as_view(), name='home',kwargs={'period': Month}),
    path('logout/', auth_views.logout,{'template_name':'registration/logout.html'}, name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    ]
# urlpatterns += i18n_patterns(
#     path('admin/', admin.site.urls),
#     path('home/', home),
# )
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)