from django.urls import path
from . import views

app_name = 'activity'

urlpatterns = [
    path('list/', views.ActivityListView.as_view(), name='list'),
    path('create/', views.ActivityCreateView.as_view(), name='create')
]
