from django.urls import path
from directs.views import *

urlpatterns = [
    path('', DirectsListReceived.as_view(), name='directlist_received'),
    path('sent/', DirectsListSent.as_view(), name='directlist_sent'),
    path('send/', directs_send, name='senddirect'),
    path('read/<int:pk>/<int:lst>',directs_detail, name='readdirect'),
    path('read/<int:pk>/delete/<int:lst>',directs_detail_delete, name='deletedirect'),
    path('reply/<int:pk>',directs_reply, name='replydirects'),
    path('deleted', DirectsListDeleted.as_view(), name='directs_deleted'),




]
