from django.conf.urls import url,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns=[
    url(r'^$',views.welcome,name = "welcome"),
    url(r'^api/users/$', views.UserList.as_view()),
    url(r'^api/projects/$', views.ProjectList.as_view()),
    url(r'api/user/user-id/(?P<pk>[0-9]+)/$',views.UserDescription.as_view()),
    url(r'api/project/project-id/(?P<pk>[0-9]+)/$',views.ProjectDescription.as_view()),
    url(r'^ajax/welcomeletter/$', views.welcomeletter, name='welcomeletter'),
    url(r'^search/', views.search_results, name='search_results'),
    url(r'updateprofile/(?P<user_id>[0-9]+)',views.updateprofile,name='updateprofile'),
    path('register/', views.registerPage, name="django_registration_register"),
    url(r'login/',views.login_view,name="login"), 
    url(r'^project/(\d+)',views.project,name ='project'),
    url(r'^projects/',views.allprojects,name ='allprojects'),
    path('logout/', views.logout_view, name="logout"),
    url(r'juryverdict/(?P<project_id>[0-9]+)', views.juryverdict, name="juryverdict"),
    url(r'^myprojects/(?P<user_id>[0-9]+)',views.userprojects,name ='myprojects'),
    url(r'^userprofile/(?P<user_id>[0-9]+)',views.userprofile,name ='userprofile'),
    url(r'project/(?P<user_id>[0-9]+)/like', views.increment_counter, name='liked'),
    url(r'^uploadproject/(\d+)',views.uploadproject,name ='uploadpproject'),
    path('change-password/',auth_views.PasswordChangeView.as_view(template_name='change-password.html'),name='password_reset'), 

]
 
urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)