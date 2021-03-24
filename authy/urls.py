from django.urls import path, include
from rest_framework import routers

from django.contrib.auth import views as authViews

from authy import views
from authy.views import index, CreateUserView, CreateTeamView, EditProfileView

from .views import manage_list, manage_detail, manage_delete, manage_permit, manage_position, manage_team

router = routers.DefaultRouter()
router.register(r'teams', views.TeamViewSet)
router.register(r'profiles', views.ProfileViewSet)


urlpatterns = [
    path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
   	path('', index, name='index'),

    # 팀장
    path('create/team',CreateTeamView, name='createteam'),
    path('create/user', CreateUserView, name='createuser'),

    # 팀원
    path('profile/edit', EditProfileView, name='editprofile'),


    # api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('byteam/<int:team>',views.TeamMates),

    # 팀원 관리
    path('manage_list/', manage_list, name='manage_list'),
    path('manage_detail/<int:pk>/', manage_detail, name='manage_detail'),
    path('manage_delete/<int:pk>/', manage_delete, name='manage_delete'),
    path('manage_permit/<int:pk>/', manage_permit, name='manage_permit'),
    path('manage_position/<int:pk>/', manage_position, name='manage_position'),
    path('manage_team/<int:pk>/', manage_team, name='manage_team'),

]
