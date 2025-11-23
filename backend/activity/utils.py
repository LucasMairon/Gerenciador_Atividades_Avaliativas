from question.models import Question
from activity.filters import QuestionActivityFilterSet
from django.db.models import Q


def get_question_activity_filter(owner, request, queryset):
    if queryset is not None:
        questions_queryset = queryset
    else:
        questions_queryset = Question.objects.filter(
            Q(visibility=True) | Q(owner=owner)).filter(is_active=True).order_by('-updated_at', '-created_at')

    question_activity_filterset = QuestionActivityFilterSet(
        request.GET or None,
        queryset=questions_queryset,
        request=request,
        prefix='filter'
    )

    return question_activity_filterset
