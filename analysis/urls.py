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
  path('user_detail/<int:pk>/', views.user_detail_page, name='detail'),
  path('user_update/<int:pk>/', views.user_update_page, name='user_update'),
  path('user_update_completed/', auth_views.PasswordChangeDoneView.as_view(template_name='analysis/user_update_done.html'), name='user_change_done'),
  path('user_delete/', views.user_delete_page, name='delete'),
  path('user_delete_completed/', views.user_delete_completed, name='user_delete_done'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('password_change/', auth_views.PasswordChangeView.as_view(template_name='analysis/password_change.html'), name='password_change'),
	path('password_change_completed/', auth_views.PasswordChangeDoneView.as_view(template_name='analysis/password_change_done.html'), name='password_change_done'),
	path('user_register/', views.user_register_page, name='register'),
	path('user_register_idcheck/', views.user_register_idcheck, name='registeridcheck'),
	path('user_register_res/', views.user_register_result, name='registerres'),
	path('user_register_completed/', views.user_register_completed, name='registercompleted'),
 
 	path('error/', views.error_page, name='error'),
 	path('no_authority/', views.no_authority_page, name='no_authority'),
  path('login_requied_page/', views.login_required_page, name='login_required_page'),

	path('notices/', views.notice_list_page, name='noticelist'),
 	path('notice_view/<int:pk>/', views.NoticeView.as_view(), name='noticeview'),
  
  path('QnA/', views.QnA_list_page, name='QnAlist'),
  path('QnA_write/', views.QnA_write_page, name='QnAwrite'),
  path('QnA_write_res/', views.QnA_write_result, name='QnAwriteres'),
  path('QnA_view/<int:pk>/', views.QnAView.as_view(), name='QnAview'),
	path('QnA_delete_res/', views.QnA_delete_result, name='QnAdeleteres'),
	path('QnA_modify/<int:pk>/', views.QnAModifyView.as_view(), name='QnAmodify'),
	path('QnA_modify_res/', views.QnA_modify_result, name='QnAmodifyres'),
 
	path('reply_list/<article>/', views.reply_list, name='replylist'),
	path('reply_modify/<int:pk>/', views.ReplyModifyView.as_view(), name='replymodify'),
	path('reply_write_res/', views.reply_write_result, name='replywriteres'),
	path('reply_modify_res/', views.reply_modify_result, name='replymodifyres'),
	path('reply_delete_res/', views.reply_delete_result, name='replydeleteres'),

  path('CV/', views.CV_list_page, name='CVlist'),
  path('CV_write/', views.CV_write_page, name='CVwrite'),
  path('CV_write_res/', views.CV_write_result, name='CVwriteres'),
  path('CV_view/<int:pk>/', views.CvView.as_view(), name='CVview'),
	path('CV_delete_res/', views.CV_delete_result, name='CVdeleteres'),
]