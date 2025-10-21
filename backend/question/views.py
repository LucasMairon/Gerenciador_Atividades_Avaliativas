from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.db import transaction
from django.db.models import Q
from django_filters.views import FilterView

from .models import Question, ObjectiveQuestion, SubjectiveQuestion
from .forms import QuestionAlternativesFormSet
from .utils import get_question_form_class
from .filters import QuestionFilterSet


class QuestionCreateView(CreateView):
    template_name = 'question/create.html'
    success_url = reverse_lazy('question:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_type = self.kwargs.get('type')

        if question_type == 'objective':
            alternatives = QuestionAlternativesFormSet()
            if self.request.GET.get('extra_alternative'):
                alternatives.extra = 1
            context['alternatives'] = alternatives

        context['question_type'] = question_type

        return context

    def get_form_class(self):
        return get_question_form_class(self.kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.owner = self.request.user
            if self.kwargs.get('type') == 'objective':
                self.object.type = 'O'

                alternatives = QuestionAlternativesFormSet(self.request.POST)
                if alternatives.is_valid():
                    self.object.save()
                    alternatives.instance = self.object
                    alternatives.save()
                else:
                    return self.form_invalid(form)

            else:
                self.object.type = 'S'
                self.object.save()

        return redirect(self.get_success_url())


class QuestionListView(FilterView):
    template_name = 'question/list.html'
    context_object_name = 'questions'
    filterset_class = QuestionFilterSet
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        questions = Question.objects.filter(
            Q(visibility=True) | Q(owner=user)).order_by('-created_at')
        return questions


class QuestionUpdateView(UpdateView):
    template_name = 'question/update.html'
    context_object_name = 'question'
    http_method_names = ['get', 'patch', 'post']
    success_url = reverse_lazy('question:list')

    def get_form_class(self):
        return get_question_form_class(self.kwargs)

    def get_object(self, queryset=None):
        question_type = self.kwargs.get('type')
        if question_type == 'objective':
            model = ObjectiveQuestion
        elif question_type == 'subjective':
            model = SubjectiveQuestion

        pk = self.kwargs.get('pk')

        object = model.objects.get(id=pk)
        return object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_type'] = self.kwargs.get('type')
        return context
