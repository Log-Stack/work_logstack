from django.urls import path, include
from rest_framework import routers

from django.contrib.auth import views as authViews

from authy import views
from authy.views import index, CreateUserView, CreateTeamView, EditProfileView, ChangePWView, ChangePWDoneView, \
    UserSearchView, SearchSelectView, UserDetailView, ProfileView, SearchAllView

# from .views import manage_list, manage_detail, manage_delete, manage_permit, manage_position, manage_team, calc_work_hours, send_work_log, SearchAllView, manage_delete_real
from .views import *

router = routers.DefaultRouter()
router.register(r'teams', views.TeamViewSet)
router.register(r'profiles', views.ProfileViewSet)


urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', authViews.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
   	path('index/', index, name='index'),

    # 팀장
    path('create/team',CreateTeamView, name='createteam'),
    path('create/user', CreateUserView, name='createuser'),
    path('edit/profile/<int:pk>/', EditProfileData, name='editprofile_manage'),

    # 팀원
    path('profile', ProfileView, name='profile'),
    path('profile/edit', EditProfileView, name='editprofile'),
    path('profile/changepw', ChangePWView, name='changepw'),
    path('profile/changepw/done',ChangePWDoneView, name='changepwdone'),
    path('search',UserSearchView,name='search'),
    path('search/all/',SearchAllView, name='searchall'),
    path('search/select',SearchSelectView, name='searchselect'),
    path('search/select/<int:pk>', UserDetailView, name='userdetail'),



    # api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('byteam/<int:team>',views.TeamMates),

    # 팀원 관리
    path('manage_list/', manage_list, name='manage_list'),
    path('manage_detail/<int:pk>/', manage_detail, name='manage_detail'),
    path('manage_delete/<int:pk>/', manage_delete, name='manage_delete'),
    path('manage_permit/<int:pk>/', manage_permit, name='manage_permit'),
    path('manage_position/<int:pk>/<str:position_name>', manage_position, name='manage_position'),
    path('manage_team/<int:pk>/<str:team_name>', manage_team, name='manage_team'),
    path('manage_delete_real/<int:pk>/', manage_delete_real, name='manage_delete_real'),

    # 매니지 디테일 페이지 관련 api
    path('calc_work_hours/', calc_work_hours, name='calc_work_hours'),
    path('send_work_log/<int:member_pk>/<str:date>', send_work_log, name='send_work_log'),

]

