from django.core.exceptions import PermissionDenied
from users.models import Group
from .models import Campaign


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

class CampaignAuthorizeMixin(object):

    def dispatch(self, request, *args, **kwargs):
        campaign_slug = self.kwargs.get("slug","")
        campaign = Campaign.objects.filter(slug=campaign_slug).first()
        if campaign:
            pass
        else:
            raise PermissionDenied
        return super(CampaignAuthorizeMixin, self).dispatch(request, *args, **kwargs)