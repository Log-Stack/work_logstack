from django.urls import path
from .views import inputPage, applyList, applyDetail, pdf

urlpatterns = [
    path('apply/', inputPage, name="hireInput"),
    path('list/', applyList, name="applyList"),
    path('detail/<int:pk>/', applyDetail, name="applyDetail"),
    path('pdf/<name>/', pdf, name="pdfviewer")
]