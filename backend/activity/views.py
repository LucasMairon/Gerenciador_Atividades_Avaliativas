from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.contrib import messages
from django.views.generic import CreateView, DeleteView
from question.models import Question
from django.shortcuts import get_object_or_404, redirect
from django_weasyprint.views import WeasyTemplateView
from django.db.models import Q
from django.http import HttpResponse
from .utils import get_question_activity_filter
from core.utils import is_htmx_request
from .forms import ActivityForm
from .models import Activity, QuestionActivity
from .filters import ActivityFilterSet


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
                question_activity = QuestionActivity.objects.create(
                    activity=self.object, question=question, order=index + 1)
                question.use_count += 1
                question.save()
                question_activity.save()

            return redirect(self.get_success_url())
        else:
            messages.error(
                self.request, 'Se certifique de adicionar pelo menos uma questão na atividade avaliativa!')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        question_activity_filterset = get_question_activity_filter(
            owner=self.request.user,
            request=self.request
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
