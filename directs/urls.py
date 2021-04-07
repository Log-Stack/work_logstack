from django.urls import path
from directs.views import *

urlpatterns = [
    path('', directs_list, name='directlist'),
    path('send/',directs_send, name='senddirect'),



]
