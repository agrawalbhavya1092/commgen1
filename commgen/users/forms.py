from django import forms
from .models import *

class NewCampaignCreateForm(forms.Forms):
	name = forms.CharField(label='Campaign Title',max_length=150)
	description = forms.CharField(label='Description',widget=forms.Textarea)
	




