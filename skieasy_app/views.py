
from skieasy_app.forms import ProfileForm, EquipmentListingForm, EquipmentForm
from skieasy_app.models import Profile, Equipment, EquipmentListing
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView


def welcome(request):
    return render(request, 'skieasy_app/welcome.html', {})


@login_required
def home(request):
    return render(request, 'skieasy_app/home-listing.html', {})


# class HomeView(LoginRequiredMixin, generic.ListView):
#     model = Equipment
#     template_name = "skieasy_app/home.html"
#     context_object_name = "listings"
#     paginate_by = 12
#
#     def get_queryset(self):
#         return Equipment.objects.prefetch_related('equipment_listings').all()


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
