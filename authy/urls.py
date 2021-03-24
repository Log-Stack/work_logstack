from django.urls import path, include
from rest_framework import routers

from django.contrib.auth import views as authViews

from authy import views
from authy.views import index, CreateUserView, CreateTeamView, EditProfileView, ChangePWView, ChangePWDoneView,SearchView

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
    path('profile/changepw', ChangePWView, name='changepw'),
    path('profile/changepw/done',ChangePWDoneView, name='changepwdone'),
    path('search',SearchView,name='search'),


    # api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('byteam/<int:team>',views.TeamMates),
]
