from django.urls import path
from directs.views import *

urlpatterns = [
    path('', directs_list_received, name='directlist_received'),
    path('sent/', DirectsListSent.as_view(), name='directlist_sent'),
    path('send/',directs_send, name='senddirect'),
    path('read/<int:pk>',directs_read, name='readdirect'),



]
