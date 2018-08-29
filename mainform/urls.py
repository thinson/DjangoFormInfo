from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.showlist, name="list"),
    path('<int:sheet_pk>/', views.sheet_detail, name='detail'),
    path('submit/', views.submit, name="submit_answer"),
]