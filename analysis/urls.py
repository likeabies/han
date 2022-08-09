"""han_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
  path('', views.main_page, name='main'),
  path('login/', auth_views.LoginView.as_view(template_name='analysis/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('password_change/', auth_views.PasswordChangeView.as_view(template_name='analysis/password_change.html'), name='password_change'),
	path('password_change_completed/', auth_views.PasswordChangeDoneView.as_view(template_name='analysis/password_change_done.html'), name='password_change_done'),
	path('user_register/', views.user_register_page, name='register'),
	path('user_register_idcheck/', views.user_register_idcheck, name='registeridcheck'),
	path('user_register_res/', views.user_register_result, name='registerres'),
	path('user_register_completed/', views.user_register_completed, name='registercompleted'),
 
 	path('error/', views.error_page, name='error'),

	path('notices/', views.notice_list_page, name='noticelist'),
 	path('notice_view/<int:pk>/', views.NoticeView.as_view(), name='noticeview'),
]