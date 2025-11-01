from django.urls import path
from . import views

app_name = 'question'

urlpatterns = [
    path('create/<str:type>/',
         views.QuestionCreateView.as_view(), name='create'),
    path('list/', views.QuestionListView.as_view(), name='list'),
    path("update/<str:type>/<uuid:pk>/",
         views.QuestionUpdateView.as_view(), name="update"),
    path('delete/<uuid:pk>/', views.QuestionDeleteView.as_view(), name='delete'),
    path('detail/<str:type>/<uuid:pk>/',
         views.QuestionDetailView.as_view(), name='detail'),
]
