from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.yb_login, name='yb_login'),
    path('check/', views.yb_check, name='yb_check'),
    path('bind/', views.yb_bind, name='yb_bind'),
]