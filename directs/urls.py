from django.urls import path
from directs.views import *

urlpatterns = [
    path('', directs_list_received, name='directlist_received'),
    path('sent/', directs_list_sent, name='directlist_sent'),
    path('send/',directs_send, name='senddirect'),
    path('read/',directs_read, name='readdirect'),



]
