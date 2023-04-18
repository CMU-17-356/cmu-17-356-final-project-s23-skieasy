from skieasy_app.forms import ProfileForm
from skieasy_app.models import Profile
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .forms import EquipmentForm
from .models import Equipment


def welcome(request):
    return render(request, 'skieasy_app/welcome.html', {})


class HomeView(LoginRequiredMixin ,generic.ListView):
    model = Equipment
    template_name = "skieasy_app/home.html"
    context_object_name = "listings"

    def get_queryset(self):
        one = {
            "equipmentListingId": 1,
            "image": "https://shorturl.at/uMV57",
            "title": "Atomic Bend 90",
            "price": 9.99,
            "startDate": "Jan 19, 2023",
            "endDate": "Jan 29, 2023",
        }
        two = {
            "equipmentListingId": 2,
            "image": "https://shorturl.at/BNPTZ",
            "title": "Nordica Enforcers",
            "price": 19.99,
            "startDate": "Jan 18, 2023",
            "endDate": "Jan 25, 2023",
        }
        three = {
            "equipmentListingId": 3,
            "image": "https://shorturl.at/bmxZ2",
            "title": "Armeda",
            "price": 19.99,
            "startDate": "Jan 5, 2023",
            "endDate": "Jan 22, 2023",
        }
        listings = [one, two, three]
        return listings
        # return Equipment.objects.all()


@login_required
def details(request, id):
    # listing = Equipment.objects.get(id=equipmentListingId)
    listing = {
        "id": id,
        "image": "https://shorturl.at/uMV57",
        "title": "Atomic Bend 90",
        "price": 9.99,
        "startDate": "Jan 19, 2023",
        "endDate": "Jan 29, 2023",
    }
    return render(request, 'skieasy_app/details.html', listing)


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
    form = EquipmentForm()

    page = {
        "form": form
    }
    return render(request, 'skieasy_app/create.html', page)
