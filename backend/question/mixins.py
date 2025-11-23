from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Question


class QuestionOwnerCheckMixin(UserPassesTestMixin):

    def test_func(self):
        question = Question.objects.get(id=self.kwargs.get('pk'))

        return question.owner == self.request.user
