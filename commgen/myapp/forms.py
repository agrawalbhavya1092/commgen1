from django import forms
from .models import *

class MailingListForm(forms.Form):
    # class Meta:
        # model = Person
        # fields = ('name', 'birthdate', 'country', 'city')

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
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
            # self.fields['m1_department_id'].queryset = self.order_by('name')
            # self.fields['p1_department_id'].queryset = self.instance.country.city_set.order_by('name')