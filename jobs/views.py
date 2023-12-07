import datetime

from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from django.db.models import F, Sum, Avg, Count
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import TruncHour, TruncDay, TruncMinute, TruncMonth
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent. Thank you!')
            return redirect('index')
    else:
        form = ContactForm()

    return render(request, 'jobs/index.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, f'Welcome, Please Login')
            return redirect('login')

    else:
        form = SignupForm()
    return render(request, 'jobs/register.html', {'form': form})


def work(request):
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your input has been submitted successfully')
            return redirect('view_jobs')

    else:
        form = WorkForm()
    return render(request, 'jobs/work.html', {'form': form})


def view_jobs(request):
    month = 9
    print1 = Jobs.objects.all().order_by('-date')
    prnts = Jobs.objects.filter(date__lte=datetime.datetime.today(), date__gt=datetime.datetime.today()-datetime.timedelta(days=4)).values('date').annotate(count=Count('id'))
    trun = Jobs.objects.annotate(month=TruncMonth('date')).values('month',).annotate(c=Sum('width')).values('month', 'c', ).filter(print__name='SAV')
    flex = Jobs.objects.annotate(month=TruncMonth('date')).values('month',).annotate(f=Sum('width')).values('month', 'f').filter(print__name='FLEX')

    trt = Jobs.objects.filter(print__name='SAV').aggregate(cal=Sum('width'))
    sum_flex = Jobs.objects.filter(print__name='FLEX').aggregate(flex=Sum('width'))
    page = request.GET.get('page')
    num_of_items = 7
    paginator = Paginator(print1, num_of_items)

    try:
        print1 = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        print1 = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        print1 = paginator.page(page)

    total_height = trt['cal']
    total_width_flex = sum_flex['flex']
    context = {
        'print1': print1,
        'trun': trun,
        'flex': flex,
        'paginator': paginator,
        'total_width_flex': total_width_flex,
        'total_height': total_height,
    }
    return render(request, 'jobs/view_jobs.html', context)


def graph(request):
    count = Jobs.objects.all().count()
    trun = Jobs.objects.annotate(months=TruncMonth('date')).values('months',).annotate(c=Sum('width')).values('months', 'c', ).filter(print__name='SAV')
    flex = Jobs.objects.annotate(months=TruncMonth('date')).values('months',).annotate(f=Sum('width')).values('months', 'f').filter(print__name='FLEX')
    money = Jobs.objects.annotate(months=TruncMonth('date')).values('months',).annotate(mon=Sum('cost')).values('months', 'mon')
    print(money)
    total_cost = Jobs.objects.aggregate(ct=Sum('cost'))
    cost = total_cost['ct']

    trt = Jobs.objects.filter(print__name='SAV').aggregate(cal=Sum('width'))
    sum_flex = Jobs.objects.filter(print__name='FLEX').aggregate(flex=Sum('width'))
    total_width_sav = trt['cal']
    total_width_flex = sum_flex['flex']
    print(count)
    context = {
        'trun': trun,
        'flex': flex,
        'cost': cost,
        'money': money,
        'count': count,
        'total_width_sav': total_width_sav,
        'total_width_flex': total_width_flex

    }
    return render(request, 'jobs/graph.html', context)


def close_record(request):
    if request.method == 'POST':
        form = CloseRecordForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your have closed your account, proceed to download PDF file')
            return redirect('download_file')
    else:
        form = CloseRecordForm()
        context = {
            'form': form
        }
        return render(request, 'jobs/close_record.html', context)


def download_file(request):
    single = CloseRecord.objects.all().order_by('-close_account')
    page = request.GET.get('page')
    num_of_items = 7
    paginator = Paginator(single, num_of_items)

    try:
        single = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        single = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        single = paginator.page(page)

    return render(request, 'jobs/download_file.html', {'single': single, 'paginator': paginator})


def pdf(request, pk):
    path1 = CloseRecord.objects.get(id=pk)
    template_path = 'jobs/pdf.html'
    context = {'path1': path1}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="slickts.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response


