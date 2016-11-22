from django.shortcuts import render, redirect
from gathering.models import DataTable, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from gathering.forms import UserProfileForm

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

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
