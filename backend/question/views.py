from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.db import transaction
from django.db.models import Q
from django_filters.views import FilterView
from django.http import HttpResponse
from django.contrib import messages
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

                alternatives = QuestionAlternativesFormSet(
                    self.request.POST, instance=self.object)

                if alternatives.is_valid():
                    alternative_instances = alternatives.save(commit=False)
                    for idx, instance in enumerate(alternative_instances):
                        instance.order = idx + 1
                    self.object.save()
                    alternatives.save()

                else:
                    return self.form_invalid(form)

            else:
                self.object.type = 'S'
                self.object.save()

        messages.success(self.request, 'Questão criada com sucesso!')

        is_htmx = (
            self.request.headers.get('HX-Request') == 'true' or
            self.request.META.get('HTTP_HX_REQUEST') or
            getattr(self.request, 'htmx', False)
        )

        if is_htmx:
            response = HttpResponse(status=200)
            response['HX-Redirect'] = reverse('question:list')
            return response

        return redirect(self.get_success_url())

    def form_invalid(self, form):
        is_htmx = (
            self.request.headers.get('HX-Request') == 'true' or
            self.request.META.get('HTTP_HX_REQUEST') or
            getattr(self.request, 'htmx', False)
        )

        if is_htmx:
            if self.kwargs.get('type') == 'objective':
                alternatives = QuestionAlternativesFormSet(self.request.POST)
                context = self.get_context_data(form=form)
                context['alternatives'] = alternatives
            else:
                context = self.get_context_data(form=form)

            response = self.render_to_response(context)
            response.status_code = 422
            return response

        return super().form_invalid(form)


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
        question = self.get_object()
        if question.type == 'O':
            question_alternatives = question.alternatives.order_by('order')
            context['alternatives'] = QuestionAlternativesFormSet(
                instance=self.object, queryset=question_alternatives)
        return context

    def form_valid(self, form):
        if form.is_valid():

            if self.object.type == 'O':
                alternatives = QuestionAlternativesFormSet(
                    self.request.POST, instance=self.object)
                if alternatives.is_valid() and form.is_valid():
                    form.save()
                    alternatives.save()
                else:
                    return self.form_invalid(form)
            elif self.object.type == 'S':
                form.save()

            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)


class QuestionDeleteView(DeleteView):
    template_name = 'partials/modal_delete.html'
    success_url = reverse_lazy('question:list')
    model = Question
    context_object_name = 'question'
