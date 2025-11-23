from django_tomselect.autocompletes import AutocompleteModelView

from .models import Discipline


class DisciplineAutoCompleteView(AutocompleteModelView):
    model = Discipline
    search_lookups = ['name__icontains', 'code__icontains']
    value_fields = ['id', 'name', 'code']

    def prepare_results(self, results):
        return super().prepare_results(results)

    def get_result_label(self, item):
        return f'{item.code} - {item.name}'
