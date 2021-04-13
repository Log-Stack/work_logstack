from django.urls import path
from directs.views import *

urlpatterns = [
    path('', DirectsListReceived.as_view(), name='directlist_received'),
    path('sent/', DirectsListSent.as_view(), name='directlist_sent'),
    path('send/',directs_send, name='senddirect'),
    path('read/<int:pk>',directs_detail, name='readdirect'),
    path('reply/<int:pk>',directs_reply, name='replydirects')



]
