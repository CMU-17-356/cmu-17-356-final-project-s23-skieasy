
from skieasy_app.forms import ProfileForm, EquipmentListingForm, EquipmentForm
from skieasy_app.models import Profile, Equipment, EquipmentListing
from skieasy_app.models import NEIGHBORHOOD_CHOICES
from skieasy_app.filters import EquipmentFilter
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from urllib.parse import urlencode
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView


def welcome(request):
    return render(request, 'skieasy_app/welcome.html', {})


class HomeView(LoginRequiredMixin, FilterView):
    model = Equipment
    filterset_class = EquipmentFilter
    template_name = "skieasy_app/home.html"
    context_object_name = "listings"
    paginate_by = 12
    ordering = ['profile_id']


@login_required
def home_query_generator(request):
    '''
    Function takes the 'POST' to the filter component, executes
    business logic to create query parameters based on the filter
    form inputs, and then redirects to the home page with query
    parameters passed.
    '''
    query_params = {}
    boot_size_difference = 1
    equipment_height_difference = 3

    start_date = request.POST.get('start_date', None)
    if start_date and (not start_date == ''):
        start_date = (
            datetime
            .strptime(start_date, '%m/%d/%Y')
            .strftime('%Y-%m-%d')
        )
        query_params['start_date'] = start_date
    end_date = request.POST.get('end_date', None)
    if end_date and (not end_date == ''):
        end_date = (
            datetime
            .strptime(end_date, '%m/%d/%Y')
            .strftime('%Y-%m-%d')
        )
        query_params['end_date'] = end_date
    neighborhoods = []
    for (value, _enum) in NEIGHBORHOOD_CHOICES:
        neighborhood = request.POST.get(value, None)
        if neighborhood:
            neighborhoods.append(value)
    if len(neighborhoods) > 0:
        query_params['neighborhoods'] = ','.join(neighborhoods)
    equipment_type = request.POST.get('equipment_type', None)
    if equipment_type and (not equipment_type == 'Either'):
        query_params['equipment_type'] = equipment_type
    gender = request.POST.get('gender', None)
    if gender and (not gender == 'Unspecified'):
        query_params['gender'] = gender
    min_price = request.POST.get('min_price', None)
    if min_price and (not min_price == ''):
        query_params['min_price'] = min_price
    max_price = request.POST.get('max_price', None)
    if max_price and (not max_price == ''):
        query_params['max_price'] = max_price
    equipment_height = request.POST.get('equipment_height', None)
    allow_similar_heights = request.POST.get('allow_similar_heights', None)
    if equipment_height and allow_similar_heights and \
        (not equipment_height == ''):
            query_params['min_equipment_height'] \
                = float(equipment_height) - equipment_height_difference
            query_params['max_equipment_height'] \
                = float(equipment_height) + equipment_height_difference
    elif equipment_height and (not equipment_height == ''):
        query_params['equipment_height'] = equipment_height
    boot_size = request.POST.get('boot_size', None)
    allow_similar_sizes = request.POST.get('allow_similar_sizes', None)
    if boot_size and allow_similar_sizes and (not boot_size == ''):
        query_params['min_boot_size'] = \
            float(boot_size) - boot_size_difference
        query_params['max_boot_size'] = \
            float(boot_size) + boot_size_difference
    elif boot_size and (not boot_size == ''):
        query_params['boot_size'] = boot_size

    params = urlencode(query_params)
    return redirect(reverse('home') + '?' + params)


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
                          boot_size=form.cleaned_data['boot_size'],
                          user_type=form.cleaned_data['user_type'])
    new_profile.save()
    return render(request, 'skieasy_app/home-listing.html', {})


@login_required
def manage(request):
    return render(request, 'skieasy_app/manage.html', {})


@login_required
def equipment_details(request, id):
    e = Equipment.objects.get(id=id)
    context = {}
    equip = {
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "price": e.price,
            "equipment_product_name": e.equipment_product_name,
            "bindings_product_name": e.bindings_product_name,
            "boots_product_name": e.boots_product_name,
            "skill_level": e.skill_level,
            "equipment_height": e.equipment_height,
            "boot_size": e.boot_size,
            "wear_status": e.wear_status,
            "equipment_type": e.equipment_type
    }
    context["equip"] = equip
    return render(request, 'skieasy_app/equip_details.html', context)


@login_required
def display_equipment(request):
    profile = Profile.objects.get(id=request.user.id)
    equip = Equipment.objects.filter(profile_id=profile.id)
    context = {}
    items = []
    for e in equip:
        item = {
            "id": e.id,
            "title": e.title,
            "description": e.description,
            "price": e.price,
            "equipment_product_name": e.equipment_product_name,
            "bindings_product_name": e.bindings_product_name,
            "boots_product_name": e.boots_product_name,
            "skill_level": e.skill_level,
            "equipment_height": e.equipment_height,
            "boot_size": e.boot_size,
            "wear_status": e.wear_status,
            "equipment_type": e.equipment_type
        }
        items.append(item)
    context["items"] = items
    return render(request, 'skieasy_app/display_equipment.html', context)


@login_required
def display_listing(request, id):
    equip = Equipment.objects.get(id=id)
    listing = EquipmentListing.objects.filter(equipment_id=id)
    context = {}
    context["title"] = equip.title
    listings = []
    for lis in listing:
        item = {
            "start_date": lis.start_date,
            "end_date": lis.end_date,
        }
        listings.append(item)
    context["listings"] = listings
    return render(request, 'skieasy_app/display_listings.html', context)


@login_required
def create_equipment(request):
    context = {}
    if (request.method == 'GET'):
        context['form'] = EquipmentForm()
        return render(request, 'skieasy_app/create_equipment.html', context)

    form = EquipmentForm(request.POST)
    context['form'] = form

    if (not form.is_valid()):
        return render(request, 'skieasy_app/create_equipment.html', context)

    new_equip = Equipment(profile_id=Profile.objects.get(id=request.user.id),
                          title=form.cleaned_data["title"],
                          description=form.cleaned_data["description"],
                          price=form.cleaned_data["price"],
                          equipment_product_name=form.cleaned_data
                          ["equipment_product_name"],
                          bindings_product_name=form.cleaned_data
                          ["bindings_product_name"],
                          boots_product_name=form.cleaned_data
                          ["boots_product_name"],
                          skill_level=form.cleaned_data["skill_level"],
                          equipment_height=form.cleaned_data
                          ["equipment_height"],
                          boot_size=form.cleaned_data["boot_size"],
                          wear_status=form.cleaned_data["wear_status"],
                          equipment_type=form.cleaned_data["equipment_type"])

    new_equip.save()

    return redirect(display_equipment)


@login_required
def create_listing(request, id):
    context = {}
    equip = Equipment.objects.get(id=id)
    context['title'] = equip.title
    context['equip_id'] = id
    if (request.method == 'GET'):
        context['form'] = EquipmentListingForm()
        return render(request, 'skieasy_app/create_listing.html', context)

    form = EquipmentListingForm(request.POST)
    context['form'] = form

    if (not form.is_valid()):
        return render(request, 'skieasy_app/create_listing.html', context)

    new_listing = EquipmentListing(
        profile_id=Profile.objects.get(id=request.user.id),
        equipment_id=equip,
        start_date=form.cleaned_data["start_date"],
        end_date=form.cleaned_data["end_date"])

    new_listing.save()

    return redirect(display_listing, id=id)


@login_required
def update_equipment(request, id):
    equip = Equipment.objects.get(id=id)
    context = {}
    context['equip_id'] = id
    if (request.method == 'GET'):
        context['form'] = EquipmentForm(instance=equip)
        return render(request, 'skieasy_app/update_equipment.html', context)

    form = EquipmentForm(request.POST, instance=equip)
    context['form'] = form

    if (not form.is_valid()):
        return render(request, 'skieasy_app/update_equipment.html', context)

    form.save()

    return redirect(display_equipment)
