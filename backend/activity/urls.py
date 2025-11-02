from django.urls import path
from . import views

app_name = 'question'

urlpatterns = [
    path('list/', views.ActivityListView.as_view(), name='list'),
]
