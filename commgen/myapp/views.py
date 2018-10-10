from django.views.generic.edit import CreateView
from .models import *
from django.shortcuts import render
from django.utils.translation import gettext as _
from django.views.generic import TemplateView
from .mixins import GroupRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from schedule.views import *
from .forms import *

@login_required(login_url='/login/')
def home(request):
	title = _('Welcome to my site')
	return render(request,"index.html",{'title':title})


def load_prevnext_calendar(request,*args,**kwargs):
    calendar = kwargs.get('calendar_slug')
    calendar = Calendar.objects.get(name = calendar)
    period_class = kwargs['period']
    try:
        date = coerce_date_dict(request.GET)
    except ValueError:
        raise Http404
    if date:
        try:
            date = datetime.datetime(**date)
        except ValueError:
            raise Http404
    else:
        date = timezone.now()
    event_list = GET_EVENTS_FUNC(request, calendar)
    my_event_list = GET_MY_EVENTS_FUNC(request, calendar)
    local_timezone = timezone.get_current_timezone()
    period = period_class(event_list, date, tzinfo=local_timezone)
    my_period = period_class(my_event_list, date, tzinfo=local_timezone)

    context.update({
        'date': date,
        'period': period,
        'my_period': my_period,
        'calendar': calendar,
        'weekday_names': weekday_names,
        'here': quote(request.get_full_path()),
    })
    return render(request,'calendar.html',context)

class LoadCalendar(LoginRequiredMixin,GroupRequiredMixin,CalendarMixin, TemplateView):
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super(LoadCalendar, self).get_context_data(**kwargs)
        calendar = self.kwargs.get('calendar_slug')
        calendar = Calendar.objects.get(name = calendar)
        # print("calendar..........................",calendar)
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

        context.update({
            'date': date,
            'period': period,
            'my_period': my_period,
            'calendar': calendar,
            'weekday_names': weekday_names,
            'here': quote(self.request.get_full_path()),
        })
        return context

# class MyView(LoginRequiredMixin,GroupRequiredMixin,CalendarMixin, DetailView):
class MyView(LoginRequiredMixin,CalendarMixin, DetailView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
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

        context.update({
            'date': date,
            'period': period,
            'my_period': my_period,
            'calendar': calendar,
            'weekday_names': weekday_names,
            'here': quote(self.request.get_full_path()),
        })
        return context


class AudienceView(LoginRequiredMixin,TemplateView):
    template_name = "myapp/audience.html"
    def get(self,request,*args,**kwargs):
        campaign_name = kwargs["campaign"]
        form = MailingListForm()
        source = DepartmentSetup.objects.order_by().values('source').distinct()
        return render(request,'myapp/audience.html',{'campaign':campaign_name,'sources':source,'form':form})

class NewCampaignCreate(LoginRequiredMixin,CreateView):
    model = Campaign
    fields = ['name','description']
    template_name = 'myapp/create_new_campaign.html'
    
    def form_valid(self, form):
        print("form valid.......................",form)
        print("form dict..................",dir(form.instance))
        form.instance.creator = self.request.user
        return super(NewCampaignCreate, self).form_valid(form)


def load_p1(request):
    source = request.GET.get('data')
    p1_department = DepartmentSetup.objects.filter(source=source).values('m1_department_id','m1_department_name').distinct().order_by()
    return render(request, 'myapp/ajax/p1_dropdown_list_options.html', {'p1_department': p1_department})

def load_p2(request):
    m1_department_id = request.GET.getlist('data[]')
    p2_department = DepartmentSetup.objects.filter(m1_department_id__in = m1_department_id).values('m2_department_id','m2_department_name').distinct().order_by()
    return render(request, 'myapp/ajax/p2_dropdown_list_options.html', {'p2_department': p2_department})

def load_m3(request):
    p2_department_id = request.GET.getlist('data[]')
    m3_department = DepartmentSetup.objects.filter(m2_department_id__in=p2_department_id).values('m3_department_id','m3_department_name').distinct().order_by()
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

class SearchMailingList(TemplateView):
    def post(self,request,*args,**kwargs):
        print("request SearchMailingList...........",request.POST)
        campaign = request.POST.get('campaign')
        mailing_list = "bhavya1992@orange.com;divyani.dubey@orange.com"
        return render(request,'myapp/audience.html',{'campaign':campaign,'mailing_list':mailing_list,'entity':['OBS']})
