from django import forms
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class EditorForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields=('campaign_body',)
    campaign_body = forms.CharField(widget=CKEditorUploadingWidget())


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields=('name','description')
    form_type = forms.CharField(required=False)

class MailingListForm(forms.Form):
    entity = forms.ModelChoiceField(queryset=DepartmentSetup.objects.all().values('source').distinct())
    p1_department = forms.ModelMultipleChoiceField(queryset=DepartmentSetup.objects.all().values('m1_department_id','m1_department_name').distinct())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['p1_department'].queryset = DepartmentSetup.objects.none()

        if 'source' in self.data:
            try:
                source = int(self.data.get('source'))
                self.fields['m1_department_id'].queryset = DepartmentSetup.objects.filter(source=source).order_by()
            except (ValueError, TypeError):
                pass