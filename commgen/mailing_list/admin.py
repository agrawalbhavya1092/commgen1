from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(MailingList)
admin.site.register(MailingListUser)
admin.site.register(MailingListCustomerUpload)
admin.site.register(MailingListSetup)
