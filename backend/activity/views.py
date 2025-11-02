from django_filters.views import FilterView
from .models import Activity
from .filters import ActivityFilterSet


class ActivityListView(FilterView):
    template_name = 'activities/list.html'
    filterset_class = ActivityFilterSet
    context_object_name = 'activities'
    paginate_by = 6
