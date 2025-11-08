from django.urls import reverse_lazy
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.contrib import messages
from core.utils import is_htmx_request
from .models import Activity, QuestionActivity
from .filters import ActivityFilterSet, QuestionActivityFilterSet
from django.views.generic import CreateView, DeleteView
from .forms import ActivityForm
from question.models import Question
from django.shortcuts import get_object_or_404, redirect
from django_weasyprint.views import WeasyTemplateView
from django.db.models import Q


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
                question = get_object_or_404(id=question_id)
                question_activity = QuestionActivity.objects.create(
                    activity=self.object, question=question, order=index + 1)
                question.use_count += 1
                question_activity.save()

            return redirect(self.get_success_url())
        else:
            messages.error(
                self.request, 'Se certifique de adicionar pelo menos uma questão a avaliação')
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        questions_queryset = Question.objects.filter(
            Q(visibility=True) | Q(owner=user)).order_by('-updated_at', '-created_at')

        question_activity_filterset = QuestionActivityFilterSet(
            self.request.GET or None,
            queryset=questions_queryset,
            request=self.request,
            prefix='filter'
        )

        paginator = Paginator(question_activity_filterset.qs, 6)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['filter'] = question_activity_filterset
        context['questions'] = page_obj
        context['paginator'] = paginator
        return context

    def get_template_names(self):
        if is_htmx_request(self.request):
            return ['activities/partials/available_questions_list.html']

        return [self.template_name]

    def form_invalid(self, form):
        messages.error(
            self.request, f'{form.errors}')
        response = super().form_invalid(form)
        return response


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

        context['questions_activity'] = activity.questionactivity_set.all()

        return context
