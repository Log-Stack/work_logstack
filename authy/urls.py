from django.urls import path

from django.contrib.auth import views as authViews

from authy.views import index

urlpatterns = [
    path('login/', authViews.LoginView.as_view(template_name='login.html'), name='login'),
   	path('', index, name='index'),
]
