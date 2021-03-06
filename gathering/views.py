from django.shortcuts import render, redirect
from gathering.models import DataTable, UserProfile, DataTableItem, DataTableOwner
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from gathering.forms import UserProfileForm

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.db import transaction

import csv

# Create your views here.
def index (request):
    return render(request, 'gathering/index.html')

@login_required
def register_profile (request):
    form = UserProfileForm()

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
            user_profile = form.save(commit=False)
            # build relation between user and user profile
            user_profile.user = request.user
            user_profile.save()
            return redirect('index')
        else:
            print(form.errors)

    context_dict = {'form': form}
    return render(request, 'gathering/profile_registration.html', context_dict)

@login_required
def profile (request, username):
    try:
        user = User.objects.get_by_natural_key(username=username)
    except User.DoesNotExist:
        return redirect('index')

    userprofile = UserProfile.objects.get_or_create(user=user)[0]
    form = UserProfileForm({'website': userprofile.website, 'face': userprofile.face})

    if request.method == 'POST':
        # update Not create a new one, pass a instance parameter
        form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if form.is_valid():
            form.save(commit=True)
            return redirect('profile', user.username)
        else:
            print(form.error)

    return render(request, 'gathering/profile.html',
                  {'userprofile': userprofile, 'selecteduser': user, 'form': form})


@login_required
def show_table_detail (request, serial_key):
    try:
        datatable = DataTable.objects.get(serial_key=serial_key)
        ownername = datatable.owner.name
        tablename = datatable.name
        tablehead = datatable.head.strip().split(',')
        sample = datatable.sample.strip().split(',')
        datatable_item = DataTableItem.objects.filter(datatable=datatable)
        order_num = [item.order_num for item in datatable_item]
        item_list = [item.content.strip().split(',') for item in datatable_item]
        for i, n in enumerate(order_num):
            item_list[i].insert(0, n)

        context_dict = {
            'ownername': ownername,
            'tablename': tablename,
            'tablehead': tablehead,
            'sample': sample,
            'item_list': item_list,
            'serial_key': serial_key,
        }
        return render(request, 'gathering/show_table_detail.html', context_dict)
    except DataTable.DoesNotExist:
        return render(request, 'gathering/404.html')


def fill_table (request):
    if request.method == 'POST':
        serial_key = request.POST.get('serial_key', '')
        if serial_key:
            try:
                datatable = DataTable.objects.get(serial_key=serial_key)
                ownername = datatable.owner.name
                tablename = datatable.name
                tablehead = datatable.head.strip().split(',')
                sample = datatable.sample.strip().split(',')

                context_dict = {
                    'serial_key': serial_key,
                    'ownername': ownername,
                    'tablename': tablename,
                    'tablehead': tablehead,
                    'sample': sample,
                }
                return render(request, 'gathering/fill_table.html', context_dict)
            except DataTable.DoesNotExist:
                return render(request, 'gathering/404.html')


def filling_complete (request):
    if request.method == 'POST':
        serial_key = request.POST.get('serial_key', '')
        filling_list = request.POST.getlist('filling_content')
        filling_list = list(map(lambda s: s.strip(), filling_list))
        filling_content = ','.join(filling_list)

        with transaction.atomic():
            try:
                datatable = DataTable.objects.get(serial_key=serial_key)
                order_num = DataTableItem.objects.filter(datatable=datatable).count() + 1
                datatable_item = DataTableItem(datatable=datatable)
                datatable_item.order_num = order_num
                datatable_item.content = filling_content
                datatable_item.save()
            except DataTable.DoesNotExist:
                pass
        return render(request, 'gathering/filling_complete.html')

@login_required
def download_table (request, serial_key):
    if serial_key:
        try:
            datatable = DataTable.objects.get(serial_key=serial_key)
            datatable_items = DataTableItem.objects.filter(datatable=datatable)
            content = 'id,' + datatable.head + '\n'
            for item in datatable_items:
                content += (str(item.order_num) + ',')
                content += item.content
                content += '\n'

            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=' + datatable.name + '.csv'
            response.write(content)
            return response
        except DataTable.DoesNotExist:
            return render(request, 'gathering/404.html')


@login_required
def show_all_tables (request):
    user = request.user
    owner = DataTableOwner.objects.get(user=user)
    datatables = DataTable.objects.filter(owner=owner)
    return render(request, 'gathering/show_all_tables.html',
                  {'datatables': datatables})


def publish_table (request):
    if request.method == 'POST':

        pass
    return render(request, 'gathering/publish_table.html')
