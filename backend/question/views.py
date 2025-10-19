from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.db import transaction
from .forms import QuestionAlternativesFormSet
from .utils import get_question_form_class


class QuestionCreateView(CreateView):
    template_name = 'question/create.html'
    success_url = reverse_lazy('question:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs.get('type') == 'objective':
            alternatives = QuestionAlternativesFormSet()
            if self.request.GET.get('extra_alternative'):
                alternatives.extra = 1
            context['alternatives'] = alternatives

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
