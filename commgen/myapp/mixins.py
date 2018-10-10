from django.core.exceptions import PermissionDenied
from users.models import Group


class GroupRequiredMixin(object):
    """
        group_required - list of strings, required param
    """

    group_required = 'test_group2'

    def dispatch(self, request, *args, **kwargs):
        my_group = Group.objects.get(name='test_group')
        # my_group.user_set.add(request.user)
        if not request.user.is_authenticated:
            raise PermissionDenied
        else:
            user_groups = []
            for group in request.user.groups.values_list('name', flat=True):
                user_groups.append(group)
            if len(set(user_groups).intersection({self.group_required})) <= 0:
                raise PermissionDenied
        return super(GroupRequiredMixin, self).dispatch(request, *args, **kwargs)