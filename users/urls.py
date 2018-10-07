
from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from .views import *
urlpatterns = [
    path('logout/', auth_views.logout,{'template_name':'registration/logout.html'}, name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    ]

