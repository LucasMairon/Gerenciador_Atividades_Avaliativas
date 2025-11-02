from .forms import ObjectiveQuestionForm, SubjectiveQuestionForm

QUESTION_FORM_TYPES = {
    'objective': ObjectiveQuestionForm,
    'subjective': SubjectiveQuestionForm
}


def get_question_form_class(kwargs):
    question_form = QUESTION_FORM_TYPES.get(kwargs.get('type'))

    return question_form
