from skieasy_app.forms import ProfileForm
from skieasy_app.models import Profile
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def welcome(request):
    return render(request, 'skieasy_app/welcome.html', {})


@login_required
def home(request):
    return render(request, 'skieasy_app/home.html', {})


@login_required
def register(request):
    context = {}
    context['form'] = ProfileForm()
    if (request.method == 'GET'):
        return render(request, 'skieasy_app/register.html', context)

    form = ProfileForm(request.POST)

    if (not form.is_valid()):
        return render(request, 'skieasy_app/register.html', context)

    new_profile = Profile(user=request.user,
                          neighborhood=form.cleaned_data['neighborhood'],
                          height=form.cleaned_data['height'],
                          gender=form.cleaned_data['gender'],
                          bootSize=form.cleaned_data['bootSize'],
                          userType=form.cleaned_data['userType'])
    new_profile.save()

    return render(request, 'skieasy_app/home.html', {})

@login_required
def manage(request):
    return render(request, 'skieasy_app/manage.html', {})


@login_required
def create(request):
    return render(request, 'skieasy_app/create.html', {})
