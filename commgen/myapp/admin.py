from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Campaign)
admin.site.register(DepartmentSetup)
admin.site.register(CampaignAuthor)
admin.site.register(CampaignReader)
admin.site.register(CampaignApprover)
