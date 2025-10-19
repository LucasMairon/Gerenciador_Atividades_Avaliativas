from django.urls import path
from . import views

app_name = 'question'

urlpatterns = [
    path('create/<str:type>/',
         views.QuestionCreateView.as_view(), name='create'),
    path('list/', views.QuestionListView.as_view(), name='list')
]
