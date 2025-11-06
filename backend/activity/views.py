from django.urls import reverse_lazy
from django_filters.views import FilterView
from core.utils import is_htmx_request
from .models import Activity, QuestionActivity
from .filters import ActivityFilterSet, QuestionActivityFilterSet
from django.views.generic import CreateView, DeleteView
from .forms import ActivityForm
from question.models import Question
from django.shortcuts import get_list_or_404, get_object_or_404
from django_weasyprint.views import WeasyTemplateView


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


class ActivityCreateView(CreateView, FilterView):
    model = Activity
    form_class = ActivityForm
    template_name = 'activities/create.html'
    filterset_class = QuestionActivityFilterSet
    success_url = reverse_lazy('activity:list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user

        list_of_ids = self.request.POST.get('questions_ids')
        if list_of_ids:
            ordered_list_ids = list_of_ids.split(',')
            questions = get_list_or_404(id=ordered_list_ids)

            for index in len(questions):
                question_activity = QuestionActivity.objects.create(
                    activity=self.object, question=questions[index])
                question_activity.order = index + 1
                question_activity.save()

        self.object.save()

        return super().form_valid(form)


class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = 'activities/partials/modal_delete.html'
    context_object_name = 'activity'
    success_url = reverse_lazy('activity:list')


class ActivityPDFPreviewView(WeasyTemplateView):
    template_name = 'activities/detail_pdf.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        activity_pk = kwargs.get('pk')

        activity = get_object_or_404(Activity, id=activity_pk)

        context['activity'] = activity

        return context
