from django.views.generic.edit import CreateView
from .models import *
# from django.shortcuts import render
# from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from .mixins import GroupRequiredMixin,CampaignAuthorizeMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from schedule.views import *
from .forms import *
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .constants import *
from django.forms.utils import ErrorList
from .utils import get_unique_slug
import json
# from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect,render


class MyView(LoginRequiredMixin,CalendarMixin, DetailView):
    template_name = 'index.html'
    def get_context_data(self, **kwargs):
        try:
            context = super(MyView, self).get_context_data(**kwargs)
            calendar = self.object
            period_class = self.kwargs['period']
            try:
                date = coerce_date_dict(self.request.GET)
            except ValueError:
                raise Http404
            if date:
                try:
                    date = datetime.datetime(**date)
                except ValueError:
                    raise Http404
            else:
                date = timezone.now()
            event_list = GET_EVENTS_FUNC(self.request, calendar)
            my_event_list = GET_MY_EVENTS_FUNC(self.request, calendar)
            local_timezone = timezone.get_current_timezone()
            period = period_class(event_list, date, tzinfo=local_timezone)
            my_period = period_class(my_event_list, date, tzinfo=local_timezone)
            campaigns = Campaign.objects.filter(creator=self.request.user)

            context.update({
                'campaigns':campaigns,
                'date': date,
                'period': period,
                'my_period': my_period,
                'calendar': calendar,
                'weekday_names': weekday_names,
                'here': quote(self.request.get_full_path()),
            })
        except Exception as e:
            context = {}
        return context

class AudienceView(LoginRequiredMixin,TemplateView):
    template_name = "myapp/delivery.html"

    def get(self,request,*args,**kwargs):
        campaign_name = kwargs["slug"]
        form = MailingListForm()
        source = DepartmentSetup.objects.order_by().values('source').distinct()
        p1_department = DepartmentSetup.objects.order_by().values('source','m1_department_name','m1_department_id').distinct()
        p2_department = DepartmentSetup.objects.order_by().values('m1_department_name','m2_department_name','m1_department_id').distinct()
        generic_company = LocationSetup.objects.order_by().values('generic_company').distinct()
        return render(request,self.template_name,{'p1_department': p1_department,'p2_department': p2_department,'campaign':campaign_name,'sources':source,'form':form,'generic_company':generic_company,'staff_status':STAFF_STATUS,'manager':MANAGER,'regular':REGULAR,'language':LANGUAGE})

    def post(self,request,*args,**kwargs):
        campaign_name = kwargs["slug"]
        form = MailingListForm()
        source = DepartmentSetup.objects.order_by().values('source').distinct()
        generic_company = LocationSetup.objects.order_by().values('generic_company').distinct()
        no_of_email = 3
        email_list = "bhavya.agrawal@puresoftware.com;divyani.dubey@orange.com;rahul.kaundal@orange.com"
        return render(request,self.template_name,{'campaign':campaign_name,'sources':source,'form':form,'generic_company':generic_company,'staff_status':STAFF_STATUS,'manager':MANAGER,'regular':REGULAR,'language':LANGUAGE,'no_of_email':no_of_email,"email_list":email_list})

class MailingTemplateEditorView(LoginRequiredMixin,CampaignAuthorizeMixin,TemplateView):
    template_name = "myapp/editor.html"
    def get(self,request,*args,**kwargs):
        campaign_name = kwargs["slug"]
        form = EditorForm(instance=Campaign.objects.get(slug=campaign_name))

        source = DepartmentSetup.objects.order_by().values('source').distinct()
        return render(request,self.template_name,{'campaign':campaign_name,'source':source,'form':form})

    def post(self,request,*args,**kwargs):
        campaign_name = kwargs["slug"]
        form = EditorForm(request.POST,instance=Campaign.objects.get(slug=campaign_name))
        if form.is_valid():
            form.instance.status = 'Sent'
            form.save()
        else:
            source = "Christmas"
            return render(request,'myapp/editor.html',{'campaign':campaign_name,'sources':source,'form':form})
        campaign = request.POST.get('campaign_body').replace(' ','')
        campaign_body = request.POST.get('campaign_body')
        if 'src="/media' in campaign or "src='/media" in campaign:
            replace1 = '"'+PROJECT_URL + '/media'
            replace2 = "'"+PROJECT_URL + "/media"
            campaign_body = campaign_body.replace('"/media',replace1).replace("'/media",replace2)
        send_mail(
            'Greetings from Commgen',
            '',
            'Commgen',[request.user.email],
            fail_silently=True,
            html_message = campaign_body
            )
        return redirect('audience',slug=campaign_name)

class SaveDraftEditorView(LoginRequiredMixin,CampaignAuthorizeMixin,TemplateView):
    template_name = "myapp/editor.html"
    def post(self,request,*args,**kwargs):
        campaign_name = kwargs["slug"]
        form = EditorForm(request.POST,instance=Campaign.objects.get(slug=campaign_name))
        if form.is_valid():
            form.save()
        else:
            source = "Christmas"
            return render(request,'myapp/editor.html',{'campaign':campaign_name,'sources':source,'form':form})
        return redirect('home')

class SelectTemplateView(LoginRequiredMixin,CampaignAuthorizeMixin,TemplateView):
    template_name = "myapp/template.html"


class NewCampaignCreate(LoginRequiredMixin,CreateView):
    model = Campaign
    # fields = ['name','description']
    template_name = 'myapp/create_new_campaign.html'
    success_url = '/campaign/template/'
    form_class = CampaignForm
    
    
    def form_valid(self, form):
        campaign_slug = get_unique_slug(form.instance.name)
        form.instance.creator = self.request.user
        form.instance.status = 'Draft'
        form.instance.creation_date = datetime.datetime.now()
        campaign_name = form.instance.name
        request_type = form.cleaned_data.get('form_type','')
        form.instance.slug = campaign_slug
        self.success_url = self.success_url + campaign_slug
        obj = Campaign.objects.filter(name=campaign_name,creator=self.request.user)
        print("form type....",request_type)
        if len(obj)>0:
            form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
                    u'Campaign name already exists. Please enter another name for campaign.'
                ])
            print("erroe.....")
            if request_type == 'ajax_request':
                print("erroe ajax.......")
                return json.dumps({'error': 404,'message': form.errors,})
            return self.form_invalid(form)
        return super(NewCampaignCreate, self).form_valid(form)

class CampaignUpdate(LoginRequiredMixin,CampaignAuthorizeMixin,UpdateView):
    model = Campaign
    template_name = 'myapp/create_new_campaign.html'
    success_url = '/campaign/template/'
    form_class = CampaignForm
    def form_valid(self, form):
        request_type = form.cleaned_data.get('form_type','')
        campaign_name = form.instance.name
        campaign_slug = self.kwargs["slug"]
        form.instance.creation_date = datetime.datetime.now()
        form.instance.slug = campaign_slug
        self.success_url = self.success_url + campaign_slug
        obj = Campaign.objects.filter(name=campaign_name,creator=self.request.user).first()
        if obj is not None:
            if obj.slug == campaign_slug:
                pass
            else:
                form._errors[forms.forms.NON_FIELD_ERRORS] = ErrorList([
                        u'Campaign name already exists. Please enter another name for campaign.'
                    ])
                if request_type == 'ajax_request':
                    return json.dumps({'error': 404,'message': form.errors,})
                return self.form_invalid(form)
        return super(CampaignUpdate, self).form_valid(form)


def load_p1(request):
    source = request.GET.get('data')
    p1_department = DepartmentSetup.objects.filter(source=source).values('m1_department_id','m1_department_name').distinct().order_by()
    return render(request, 'myapp/ajax/p1_dropdown_list_options.html', {'p1_department': p1_department})

def load_p1_inner(request):
    source = request.GET.get('data')
    p1_department = DepartmentSetup.objects.filter(source=source).values('m1_department_id','m1_department_name').distinct().order_by()
    return render(request, 'myapp/ajax/p1_dropdown_list_options_inner.html', {'p1_department': p1_department})


def load_p2(request):
    m1_department_id = request.GET.getlist('data[]')
    p2_department = DepartmentSetup.objects.filter(m1_department_id__in = m1_department_id).values('m2_department_id','m2_department_name').distinct().order_by()
    return render(request, 'myapp/ajax/p2_dropdown_list_options.html', {'p2_department': p2_department})

def load_m3(request):
    p2_department_id = request.GET.getlist('data[]')
    m3_department = DepartmentSetup.objects.filter(m2_department_id__in=p2_department_id).values('m3_department_id','m3_department_name').distinct().order_by()
    print("m3...",m3_department)
    return render(request, 'myapp/ajax/m3_dropdown_list_options.html', {'m3_department': m3_department})

def load_m4(request):
    m3_department_id = request.GET.getlist('data[]')
    m4_department = DepartmentSetup.objects.filter(m3_department_id__in=m3_department_id).values('m4_department_id','m4_department_name').distinct().order_by()
    return render(request, 'myapp/ajax/m4_dropdown_list_options.html', {'m4_department': m4_department})

def load_m5(request):
    m4_department_id = request.GET.getlist('data[]')
    m5_department = DepartmentSetup.objects.filter(m4_department_id__in=m4_department_id).values('m5_department_id','m5_department_name').distinct().order_by('m5_department_name')
    return render(request, 'myapp/ajax/m5_dropdown_list_options.html', {'m5_department': m5_department})

def load_m6(request):
    m5_department_id = request.GET.getlist('data[]')
    m6_department = DepartmentSetup.objects.filter(m5_department_id__in=m5_department_id).values('m6_department_id','m6_department_name').distinct().order_by('m6_department_name')
    return render(request, 'myapp/ajax/m6_dropdown_list_options.html', {'m6_department': m6_department})

def load_region(request):
    generic_company = request.GET.getlist('data')
    region = LocationSetup.objects.filter(generic_company__in=generic_company).values('region').order_by('region').distinct()
    return render(request, 'myapp/ajax/region_dropdown_list_options.html', {'region': region})

def load_country(request):
    region = request.GET.getlist('data[]')
    country = LocationSetup.objects.filter(region__in=region).values('country').order_by('country').distinct()
    return render(request, 'myapp/ajax/country_dropdown_list_options.html', {'country': country})

def load_location(request):
    country = request.GET.getlist('data[]')
    location = LocationSetup.objects.filter(country__in=country).values('location').order_by('location').distinct()
    return render(request, 'myapp/ajax/location_dropdown_list_options.html', {'location': location})

 
class SearchMailingList(TemplateView):
    def post(self,request,*args,**kwargs):
        campaign = request.POST.get('campaign')
        mailing_list = "bhavya1992@orange.com;divyani.dubey@orange.com"
        return render(request,'myapp/audience.html',{'campaign':campaign,'mailing_list':mailing_list,'entity':['OBS']})
