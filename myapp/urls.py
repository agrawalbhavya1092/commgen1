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
from django.urls import path
from .views import *
from django.conf.urls import url
# from django.conf.urls.i18n import i18n_patterns
from django.conf.urls import include
urlpatterns = [
    path('newcampaign/', NewCampaignCreate.as_view(),name='newcampaign'),
    path('search-mailing-list/', SearchMailingList.as_view(),name='search_mailing_list'),
    path('ajax/p1/', load_p1,name='load_p1'),
    path('ajax/p1_inner/', load_p1_inner,name='load_p1_inner'),
    path('ajax/p2/', load_p2,name='load_p2'),
    path('ajax/m3/', load_m3,name='load_m3'),
    path('ajax/m4/', load_m4,name='load_m4'),
    path('ajax/m5/', load_m5,name='load_m5'),
    path('ajax/m6/', load_m6,name='load_m6'),
    path('ajax/region/', load_region,name='load_region'),
    path('ajax/country/', load_country,name='load_country'),
    path('ajax/location/', load_location,name='load_location'),
    url(r'^audience/(?P<slug>[-\w]+)/$', AudienceView.as_view(), name='audience'),
    url(r'^updatecampaign/(?P<slug>[-\w]+)/$', CampaignUpdate.as_view(), name='updatecampaign'),
    url(r'^editor/(?P<slug>[-\w]+)/$', MailingTemplateEditorView.as_view(), name='editor'),
    url(r'^editordraft/(?P<slug>[-\w]+)/$', SaveDraftEditorView.as_view(), name='editor_draft'),
    url(r'^template/(?P<slug>[-\w]+)/$', SelectTemplateView.as_view(), name='template'),
]
# urlpatterns += i18n_patterns(path('',include('myapp.urls')))
# urlpatterns += i18n_patterns(path('home/', home))
