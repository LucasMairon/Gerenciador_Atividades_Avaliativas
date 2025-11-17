from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.UserLoginView.as_view(), name='login'),
    path('user/logout/', views.UserLogoutView.as_view(), name='logout')
]
