from django_filters.views import FilterView
from core.utils import is_htmx_request
from .models import Activity
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
            return ['activities/partials/activity.html']

        return [self.template_name]
