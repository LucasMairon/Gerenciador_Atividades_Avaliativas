from django.urls import path
from . import views

app_name = 'discipline'

urlpatterns = [
    path('autocomplete/',
         views.DisciplineAutoCompleteView.as_view(), name='autocomplete'),
]
