from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.UserLoginView.as_view(), name='login'),
    path('user/logout/', views.UserLogoutView.as_view(), name='logout'),
    path('user/password_reset/',
         views.UserPasswordResetView.as_view(), name='password_reset'),
    path('user/password_reset_confirm/<uidb64>/<token>/',
         views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
]
