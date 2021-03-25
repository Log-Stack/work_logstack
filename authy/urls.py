from django.urls import path, include
from rest_framework import routers

from django.contrib.auth import views as authViews

from authy import views
from authy.views import index, CreateUserView, CreateTeamView, EditProfileView, ChangePWView, ChangePWDoneView, UserSearchView, SearchSelectView, UserDetailView, ProfileView

router = routers.DefaultRouter()
router.register(r'teams', views.TeamViewSet)
router.register(r'profiles', views.ProfileViewSet)


urlpatterns = [
    path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', authViews.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
   	path('', index, name='index'),

    # 팀장
    path('create/team',CreateTeamView, name='createteam'),
    path('create/user', CreateUserView, name='createuser'),

    # 팀원
    path('profile', ProfileView, name='profile'),
    path('profile/edit', EditProfileView, name='editprofile'),
    path('profile/changepw', ChangePWView, name='changepw'),
    path('profile/changepw/done',ChangePWDoneView, name='changepwdone'),
    path('search',UserSearchView,name='search'),
    path('search/select',SearchSelectView, name='searchselect'),
    path('search/<int:user_id>', UserDetailView, name='userdetail'),



    # api
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('byteam/<int:team>',views.TeamMates),
]

