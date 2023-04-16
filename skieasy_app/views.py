from skieasy_app.forms import ProfileForm
from skieasy_app.models import Profile
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def welcome(request):
    return render(request, 'skieasy_app/welcome.html', {})


@login_required
def home(request):

    one = {
        "equipmentListingId": 1,
        "image": "https://cdn.skiessentials.com/media/catalog/product/cache/a62fda1dbcde718479b9c838816c57df/aa0029434k.jpg",
        "title": "Atomic Bend 90",
        "price": 9.99,
        "startDate": "Jan 19, 2023",
        "endDate": "Jan 29, 2023",
    }
    two = {
        "equipmentListingId": 2,
        "image": "https://images.evo.com/imgp/zoom/224769/902350/clone.jpg",
        "title": "Nordica Enforcers",
        "price": 19.99,
        "startDate": "Jan 18, 2023",
        "endDate": "Jan 25, 2023",
    }
    three = {
        "equipmentListingId": 3,
        "image": "data:image/jpeg;base64,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",
        "title": "Armeda",
        "price": 19.99,
        "startDate": "Jan 5, 2023",
        "endDate": "Jan 22, 2023",
    }
    listings = [one, two, three]

    page = {
        "listings": listings
    }
    return render(request, 'skieasy_app/home.html', page)


@login_required
def details(request, id):
    # listing = Equipment.objects.get(id=equipmentListingId)
    listing = {
        "id": id,
        "image": "https://cdn.skiessentials.com/media/catalog/product/cache/a62fda1dbcde718479b9c838816c57df/aa0029434k.jpg",
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
    return render(request, 'skieasy_app/create.html', {})
