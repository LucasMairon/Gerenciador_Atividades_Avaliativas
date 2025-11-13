from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.contrib import messages
from django.views.generic import CreateView, DeleteView, UpdateView, View
from question.models import Question
from django.shortcuts import get_object_or_404, redirect
from django_weasyprint.views import WeasyTemplateView
from django.db.models import Q
from django.http import HttpResponse
from alternative.models import Alternative
from django.db import transaction
from .utils import get_question_activity_filter
from core.utils import is_htmx_request
from .forms import ActivityForm
from .models import Activity, QuestionActivity
from .filters import ActivityFilterSet
import random


class ActivityListView(FilterView):
    template_name = 'activities/list.html'
    filterset_class = ActivityFilterSet
    context_object_name = 'activities'
    paginate_by = 6

    def get_queryset(self):
        activities = Activity.objects.filter(owner=self.request.user.id).order_by(
            '-created_at', '-updated_at')
        return activities

    def get_template_names(self):
        if is_htmx_request(self.request):
            return ['activities/partials/list_partial.html']

        return [self.template_name]


class ActivityCreateView(CreateView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/create.html'
    success_url = reverse_lazy('activity:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user

        self.object.save()
        list_of_ids = self.request.POST.get('questions_ids')
        if list_of_ids:
            ordered_list_ids = list_of_ids.split(',')

            for index, question_id in enumerate(ordered_list_ids):
                question = get_object_or_404(Question, id=question_id)
                if question.is_active:
                    question_activity = QuestionActivity.objects.create(
                        activity=self.object, question=question, order=index + 1)
                    question.use_count += 1
                    question.save()
                    question_activity.save()
                else:
                    messages.error(
                        self.request, 'Você está tentando manipular uma questão que não existe mais')
                    return self.form_invalid(form)
            messages.success(
                self.request, 'Atividade avaliativa criada com sucesso!')
            return redirect(self.get_success_url())
        else:
            messages.error(
                self.request, 'Se certifique de adicionar pelo menos uma questão na atividade avaliativa!')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question_activity_filterset = get_question_activity_filter(
            owner=self.request.user,
            request=self.request,
            queryset=None
        )

        context['filter'] = question_activity_filterset
        context['questions'] = question_activity_filterset.qs
        return context

    def get_template_names(self):
        if is_htmx_request(self.request):
            return ['activities/partials/available_questions_list.html']

        return [self.template_name]


class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = 'activities/partials/modal_delete.html'
    context_object_name = 'activity'
    success_url = reverse_lazy('activity:list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        self.object.delete()

        return HttpResponse(status=200)


class ActivityUpdateView(UpdateView):
    model = Activity
    template_name = 'activities/update.html'
    context_object_name = 'activity'
    success_url = reverse_lazy('activity:list')
    form_class = ActivityForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity = self.get_object()
        questions_queryset = Question.objects.filter(Q(visibility=True) | Q(
            owner=self.request.user)).filter(is_active=True).order_by('-updated_at', '-created_at')

        available_questions = questions_queryset.exclude(
            id__in=activity.questions.all())
        question_activity_filterset = get_question_activity_filter(
            owner=self.request.user,
            request=self.request,
            queryset=available_questions
        )

        context['actual_questions'] = activity.questions.all()
        context['filter'] = question_activity_filterset
        context['questions'] = question_activity_filterset.qs
        return context

    def form_valid(self, form):
        actual_questions_ids = set(
            self.object.questionactivity_set.values_list('question_id', flat=True))
        self.object.questionactivity_set.all().delete()
        list_of_ids = self.request.POST.get('questions_ids')

        if list_of_ids:
            ordered_list_ids = list_of_ids.split(',')

            for index, question_id in enumerate(ordered_list_ids):
                question = get_object_or_404(Question, id=question_id)
                question_activity = QuestionActivity.objects.create(
                    activity=self.object, question=question, order=index + 1)

                if question.id not in actual_questions_ids:
                    question.use_count += 1
                    question.save(update_fields=['use_count'])

                question_activity.save()

            messages.success(
                self.request, 'Atividade avaliativa editada com sucesso')
            return super().form_valid(form)

        else:
            messages.error(
                self.request, 'Se certifique de adicionar pelo menos uma questão na atividade avaliativa!')
            return self.form_invalid(form)


class ActivityPDFPreviewView(WeasyTemplateView):
    template_name = 'activities/pdf_preview/detail_pdf.html'
    pdf_attachment = False

    def get_object(self, id):
        return get_object_or_404(Activity, id=id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity_pk = kwargs.get('pk')

        activity = self.get_object(id=activity_pk)

        context['activity'] = activity

        questions_activity = activity.questionactivity_set.all()

        questions = []
        for question in questions_activity:
            questions.append(question.question)

        context['questions'] = questions

        return context

    def get_pdf_filename(self):
        activity = self.get_object(id=self.kwargs.get('pk'))
        return f'{activity.name}-unidade_{activity.unit}-{activity.period}'


class ActivityShuffleView(View):

    def post(self, *args, **kwargs):
        pk = kwargs.get('pk')
        target = kwargs.get('target')
        activity = get_object_or_404(Activity, id=pk)

        questions = activity.questions.all()

        TEMP_OFFSET = 100

        if target == 'questions':
            with transaction.atomic():
                questions_activity = activity.questionactivity_set.all()
                questions_activity_orders_list = [
                    question_activity.order for question_activity in questions_activity]

                random.shuffle(questions_activity_orders_list)

                temp_modified_questions_activity = []
                for index, question_activity in enumerate(questions_activity):
                    question_activity.order = TEMP_OFFSET + question_activity.order
                    temp_modified_questions_activity.append(question_activity)

                QuestionActivity.objects.bulk_update(
                    temp_modified_questions_activity, ['order'])

                modified_questions_activity = []
                for index, question_activity in enumerate(questions_activity):
                    question_activity.order = questions_activity_orders_list[index]
                    modified_questions_activity.append(question_activity)

                QuestionActivity.objects.bulk_update(
                    modified_questions_activity, ['order'])

        elif target == 'alternatives':
            for question in questions:
                if question.type == 'O':
                    alternatives = question.objectivequestion.alternatives.all()

                    alternative_orders_list = [
                        alt.order for alt in alternatives]

                    random.shuffle(alternative_orders_list)

                    modified_alternatives = []

                    for index, alternative in enumerate(alternatives):
                        alternative.order = alternative_orders_list[index]
                        modified_alternatives.append(alternative)

                    Alternative.objects.bulk_update(
                        modified_alternatives, ['order'])

        return redirect('activities/partials/activity.html')
