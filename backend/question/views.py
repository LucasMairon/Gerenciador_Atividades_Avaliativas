from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.db import transaction
from django.db.models import Q
from django_filters.views import FilterView
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Question, ObjectiveQuestion, SubjectiveQuestion
from .forms import QuestionAlternativesFormSet
from .utils import get_question_form_class, is_htmx_request
from .filters import QuestionFilterSet


class QuestionCreateView(LoginRequiredMixin, CreateView):
    template_name = 'question/create.html'
    success_url = reverse_lazy('question:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_type = self.kwargs.get('type')

        if question_type == 'objective':
            if self.request.method == 'GET':
                alternatives = QuestionAlternativesFormSet(
                    self.request.GET.get('alternatives'), prefix='alternatives')
            else:
                alternatives = QuestionAlternativesFormSet(self.request.POST)
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

        if is_htmx_request(self.request):
            response = HttpResponse(status=200)
            response['HX-Redirect'] = self.get_success_url()
            return response

        return redirect(self.get_success_url())

    def form_invalid(self, form):

        if is_htmx_request(self.request):
            if self.kwargs.get('type') == 'objective':
                alternatives = QuestionAlternativesFormSet(
                    self.request.POST, prefix='alternatives')
                context = self.get_context_data(form=form)
                context['alternatives'] = alternatives
            else:
                context = self.get_context_data(form=form)

            response = self.render_to_response(context)
            response.status_code = 422
            return response

        return super().form_invalid(form)

    def get_template_names(self):
        if self.kwargs.get('type') == 'objective':
            if is_htmx_request(self.request):
                return ['partials/alternatives_form.html']
            else:
                return [self.template_name]
        elif self.kwargs.get('type') == 'subjective':
            return super().get_template_names()


class QuestionListView(LoginRequiredMixin, FilterView):
    template_name = 'question/list.html'
    context_object_name = 'questions'
    filterset_class = QuestionFilterSet
    paginate_by = 6

    def get_queryset(self):
        user = self.request.user
        questions = Question.objects.filter(
            Q(visibility=True) | Q(owner=user)).order_by('-created_at')
        return questions

    def get_template_names(self):

        if is_htmx_request(self.request):
            return ['partials/list_partial.html']

        return [self.template_name]


class QuestionUpdateView(LoginRequiredMixin, UpdateView):
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
                instance=self.object, queryset=question_alternatives, prefix='alternatives')
        return context

    def form_valid(self, form):
        form.save()
        if self.object.type == 'O':
            alternatives = QuestionAlternativesFormSet(
                self.request.POST, instance=self.object, prefix='alternatives')
            if alternatives.is_valid():
                alternatives.save()
            else:
                return self.form_invalid(form)
        messages.success(
            self.request, 'Questão editada com sucesso!')
        return redirect(self.get_success_url())

    def get_template_names(self):
        if self.kwargs.get('type') == 'objective':
            if is_htmx_request(self.request):
                return ['partials/alternatives_form.html']
            else:
                return [self.template_name]
        elif self.kwargs.get('type') == 'subjective':
            return super().get_template_names()


class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'partials/modal_delete.html'
    success_url = reverse_lazy('question:list')
    model = Question
    context_object_name = 'question'


class QuestionDetailView(LoginRequiredMixin, DetailView):
    template_name = 'partials/modal_detail.html'
    context_object_name = 'question'

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
        question = self.object
        if question.type == 'O':
            question_alternatives = question.alternatives.order_by('order')
            context['alternatives'] = QuestionAlternativesFormSet(
                instance=self.object, queryset=question_alternatives)
        return context
