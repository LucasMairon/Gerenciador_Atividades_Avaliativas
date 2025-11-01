from .forms import ObjectiveQuestionForm, SubjectiveQuestionForm

QUESTION_FORM_TYPES = {
    'objective': ObjectiveQuestionForm,
    'subjective': SubjectiveQuestionForm
}


def get_question_form_class(kwargs):
    question_form = QUESTION_FORM_TYPES.get(kwargs.get('type'))

    return question_form


def is_htmx_request(request):
    is_htmx = getattr(request, 'htmx', False)
    if is_htmx:
        return True
    else:
        return False
