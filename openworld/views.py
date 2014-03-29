from django.shortcuts import render, render_to_response
from django.contrib.auth.views import logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext, loader
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from openworld.forms import UserForm, RequestForm, NewRequestForm
from openworld.models import Entry, ExtraEntry, TagModifications, Pending
from django.core.urlresolvers import reverse
from django.contrib import messages
import json


def index(request):
    with open('openworld/taxonomy.json', 'r') as f:
        jsondata = json.load(f)
    return render(request, 'openworld/index.html', {'taxonomy':jsondata})


def search(request):
    services_term = request.GET['servicesquery']
    situations_term = request.GET['situationsquery']
 
    services_query_tags = json.loads('["%s"]' % services_term.replace(',','","'))
    situations_query_tags = json.loads('["%s"]' % situations_term.replace(',','","'))

    results = []
    for entry in Entry.objects.all():
        if entry.tags:
            entry_tags = json.loads(entry.tags)
            situations_tags = entry_tags['situations']
            services_tags = entry_tags['services']
            if any(tag in situations_query_tags for tag in situations_tags) or any(tag in services_query_tags for tag in services_tags):
                results.append(entry)

    paginator = Paginator(results, 30)
    page = request.GET.get('page')
    try:
        paged_results = paginator.page(page)
    except PageNotAnInteger:
        paged_results = paginator.page(1)
    except EmptyPage:
        paged_results = paginator.page(paginator.num_pages)
    return render(request, 'openworld/search.html', {'results':paged_results})


@login_required
def dashboard(request):
    latest_entries = Entry.objects.order_by('-id')
    paginator = Paginator(latest_entries, 30)

    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    context = {"entries": entries}
    return render(request, 'openworld/dashboard.html', context)


@login_required
def user_info(request):
    return render(request, 'openworld/profile.html', {"profile": request.user})


@login_required
def view_entries(request):
    latest_entries = Entry.objects.order_by('-id')
    paginator = Paginator(latest_entries, 30)

    page = request.GET.get('page')
    try:
        entries = paginator.page(page)
    except PageNotAnInteger:
        entries = paginator.page(1)
    except EmptyPage:
        entries = paginator.page(paginator.num_pages)

    context = {"entries": entries}
    return render(request, 'openworld/viewentries.html', context)


@login_required
def view_entry(request, entry_id):
    entry = Entry.objects.get(id=entry_id)
    extra_entry = ExtraEntry.objects.get(entry=entry)

    if extra_entry.url and extra_entry.url[:7] != "http://":
        extra_entry.url = "http://" + extra_entry.url
    if extra_entry.agency_url and extra_entry.agency_url[:7] != "http://":
        extra_entry.agency_url = "http://" + extra_entry.agency_url
    return render(request, 'openworld/viewentry.html', {'entry': entry, 'extra_entry': extra_entry})


@login_required
def tagged_entries(request):
    try:
        latest_entries = TagModifications.objects.filter(user=request.user).order_by('-id')
        paginator = Paginator(latest_entries, 30)

        page = request.GET.get('page')
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)

        context = {"entries": entries}
    except:
        context = {"entries": None}
    return render(request, 'openworld/taggedentries.html', context)


@login_required
def view_requests(request):
    try:
        latest_entries = Pending.objects.filter(user=request.user).order_by('-id')
        paginator = Paginator(latest_entries, 30)

        page = request.GET.get('page')
        try:
            entries = paginator.page(page)
        except PageNotAnInteger:
            entries = paginator.page(1)
        except EmptyPage:
            entries = paginator.page(paginator.num_pages)

        context = {"entries": entries}
    except:
        context = {"entries": None}
    return render(request, 'openworld/viewrequests.html', context)


@login_required
def submit_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
 
        if form.is_valid():
            cleaned_data = form.cleaned_data
            try:
                jsondata = json.loads(cleaned_data['file'].read().decode())
                if type(jsondata) is list or not jsondata.get('data'):
                    jsondata = {'data':jsondata}
            except ValueError:
                messages.success(request, 'Error: Invalid JSON file')
                return HttpResponseRedirect(reverse('dashboard'))

            pending = Pending(user=request.user, source=cleaned_data['source'], url=cleaned_data['source'].url, data=jsondata) 
            pending.save()
            messages.success(request, 'Success: Request submitted.')
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.error(request, 'Error: Request submission failed.')
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = RequestForm()
        return render(request, 'openworld/submitrequest.html', {'form':form})


@login_required
def submit_new_request(request):
    if request.method == 'POST':
        form = NewRequestForm(request.POST, request.FILES)
 
        if form.is_valid():
            cleaned_data = form.cleaned_data
            try:
                jsondata = json.loads(cleaned_data['file'].read().decode())
                if type(jsondata) is list or not jsondata.get('data'):
                    jsondata = {'data':jsondata}
            except ValueError:
                messages.success(request, 'Error: Invalid JSON file')
                return HttpResponseRedirect(reverse('dashboard'))

            pending = Pending(user=request.user, source=cleaned_data['source'], url=cleaned_data['url'], data=jsondata) 
            pending.save()
            messages.success(request, 'Success: Request submitted.')
            return HttpResponseRedirect(reverse('dashboard'))
        else:
            messages.error(request, 'Error: Request submission failed.')
            return HttpResponseRedirect(reverse('dashboard'))
    else:
        form = NewRequestForm()
        return render(request, 'openworld/submitrequest.html', {'form':form, 'new_request':True})


@login_required
def submit_tags(request):
    if request.method == 'POST':
        entry = Entry.objects.filter(id=request.POST['id'])

        if not entry:
            messages.error(request, 'Error: entry does not exist.')
            return HttpResponseRedirect(reverse('dashboard'))
        entry = entry[0]

        try:
            services_tags = json.loads('["%s"]' % request.POST['servicestags'].replace(',', '","'))
            situations_tags = json.loads('["%s"]' % request.POST['situationstags'].replace(',', '","'))
        except ValueError:
            messages.error(request, 'Error: Invalid json format.')
            return HttpResponseRedirect(reverse('dashboard'))
 
        # If tags are empty or user has elevated privileges, then replace the tags
        if not entry.tags or request.user.is_staff or request.user.is_superuser:
            entry.tags = {'services':services_tags, 'situations':situations_tags}
        else:
            # Otherwise just append new tags only
            entry_tags = json.loads(entry.tags)
            if situations_tags and not situations_tags == [""]:
                new_situations_tags = list(set(entry_tags['situations']).union(set(situations_tags)))
            else:
                new_situations_tags = entry_tags['situations']

            if services_tags and not services_tags == [""]:
                new_services_tags = list(set(entry_tags['services']).union(set(services_tags)))
            else:
                new_services_tags = entry_tags['services']

            entry.tags = {'situations': new_situations_tags, 'services': new_services_tags}
            
        entry.save()
        tag_modification = TagModifications(user=request.user, entry=entry, tags=entry.tags) 
        tag_modification.save()

        # Success
        return render(request, 'openworld/submittags.html', {'postrequest':request.POST}) 
    else:
        messages.error(request, 'Error: Request submission failed.')
        return HttpResponseRedirect(reverse('dashboard'))


@login_required
def tags_form(request, entry_id):
    entry = Entry.objects.get(id=entry_id)

    with open('openworld/taxonomy.json', 'r') as f:
        jsondata = json.load(f)
    return render(request, 'openworld/submittags.html', {'taxonomy':jsondata, 'entry_id':entry_id, 'entry_tags':entry.tags})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/openworld/')


def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()

    return render_to_response(
            'openworld/register.html',
            {'user_form': user_form, 'registered': registered},
            context)
