from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Activity


class ActivityOwnerCheckMixin(UserPassesTestMixin):

    def test_func(self):
        activity = Activity.objects.get(id=self.kwargs.get('pk'))

        return activity.owner == self.request.user
