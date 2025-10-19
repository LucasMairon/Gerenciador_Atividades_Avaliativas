import django_filters
from .models import Question


class QuestionFilterSet(django_filters.FilterSet):

    discipline__name = django_filters.CharFilter(
        field_name='discipline__name',
        lookup_expr='icontains'
    )

    owner__name = django_filters.CharFilter(
        field_name='owner__username',
        lookup_expr='icontains'
    )

    class Meta:
        model = Question
        fields = {
            'type': ['exact'],
            'difficulty_level': ['exact'],
            'visibility': ['exact'],
            'subject': ['icontains'],
            'statement': ['icontains'],
        }
