from django.db.models import Count
from skieasy_app.models import EquipmentImage
from skieasy_app.forms import ProfileForm, EquipmentListingForm, EquipmentForm
from skieasy_app.models import Profile, Equipment, EquipmentListing
from skieasy_app.models import EquipmentReservation, User
from skieasy_app.models import NEIGHBORHOOD_CHOICES
from skieasy_app.filters import EquipmentFilter
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, reverse, get_object_or_404
from urllib.parse import urlencode
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.template import loader
from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView


def __profile_check(action_function):
    def my_wrapper_function(request, *args, **kwargs):
        try:
            user = User.objects.get(id=request.user.id)
            if (Profile.objects.filter(user=user).exists()):
                return action_function(request, *args, **kwargs)
            else:
                raise ValueError("Please Register")
        except Exception as e:
            return redirect(reverse('register'))
    return my_wrapper_function


def welcome(request):
    return render(request, 'skieasy_app/welcome.html', {})


class HomeView(LoginRequiredMixin, FilterView):
    model = Equipment
    filterset_class = EquipmentFilter
    template_name = "skieasy_app/home.html"
    context_object_name = "listings"
    paginate_by = 12
    ordering = ['profile_id']

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = (
            queryset
            .annotate(listing_count=Count('equipment_listings'))
            .filter(listing_count__gt=0)
        )
        return queryset


@login_required
@__profile_check
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
    not_empty = (not equipment_height == '')
    if equipment_height and allow_similar_heights and not_empty:
        query_params['min_equipment_height'] \
            = float(equipment_height) - equipment_height_difference
        query_params['max_equipment_height'] \
            = float(equipment_height) + equipment_height_difference
    elif equipment_height and not_empty:
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
                          first_name=form.cleaned_data['first_name'],
                          last_name=form.cleaned_data['last_name'],
                          phone_number=form.cleaned_data['phone_number'],
                          neighborhood=form.cleaned_data['neighborhood'],
                          height=form.cleaned_data['height'],
                          gender=form.cleaned_data['gender'],
                          boot_size=form.cleaned_data['boot_size'],
                          user_type=form.cleaned_data['user_type'])
    new_profile.save()
    return render(request, 'skieasy_app/home.html', {})


@login_required
@__profile_check
def manage(request):
    return render(request, 'skieasy_app/manage.html', {})


@login_required
@__profile_check
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
@__profile_check
def listing(request, id):
    template = loader.get_template('skieasy_app/listing.html')
    equip = Equipment.objects.get(id=id)
    equip_images = EquipmentImage.objects.filter(equipment_id=1)
    lists = EquipmentListing.objects.filter(equipment_id=equip)

    context = {'listing': {
                "id": equip.id,
                "title": equip.title,
                "description": equip.description,
                "price": equip.price,
                "equipment_product_name": equip.equipment_product_name,
                "bindings_product_name": equip.bindings_product_name,
                "boots_product_name": equip.boots_product_name,
                "skill_level": equip.skill_level,
                "equipment_height": equip.equipment_height,
                "boot_size": equip.boot_size,
                "wear_status": equip.wear_status,
                "equipment_type": equip.equipment_type,
                "profile_id": equip.profile_id,
                "equipment_listings": equip.equipment_listings,
                "current_user": request.user.id}}
    if (len(lists) < 1):
        context["bool_lists"] = 0
    else:
        listings = []
        for lis in lists:
            item = {
                "id": lis.id,
                "start_date": lis.start_date,
                "end_date": lis.end_date,
            }
            listings.append(item)
        context["listings"] = listings
    return HttpResponse(template.render(context, request))


@login_required
@__profile_check
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
@__profile_check
def display_listing(request, id):
    equip = Equipment.objects.get(id=id)
    listing = EquipmentListing.objects.filter(equipment_id=id)
    context = {}
    context["title"] = equip.title
    listings = []
    for lis in listing:
        item = {
            "id": lis.id,
            "start_date": lis.start_date,
            "end_date": lis.end_date,
        }
        listings.append(item)
    context["listings"] = listings
    return render(request, 'skieasy_app/display_listings.html', context)


@login_required
@__profile_check
def create_equipment(request):
    context = {}
    if (request.method == 'GET'):
        context['form'] = EquipmentForm()
        return render(request, 'skieasy_app/create_equipment.html', context)

    form = EquipmentForm(request.POST, request.FILES)
    context['form'] = form

    if (not form.is_valid()):
        return render(request, 'skieasy_app/create_equipment.html', context)

    if (form.cleaned_data["picture"] == 'default.png'):
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
                          equipment_type=form.cleaned_data["equipment_type"],
                          picture=form.cleaned_data["picture"],
                          content_type=form.cleaned_data["picture"]
                          .content_type)

    new_equip.save()

    return redirect(display_equipment)


@login_required
@__profile_check
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
@__profile_check
def update_equipment(request, id):
    equip = Equipment.objects.get(id=id)
    context = {}
    context['equip_id'] = id
    if (request.method == 'GET'):
        context['form'] = EquipmentForm(instance=equip)
        return render(request, 'skieasy_app/update_equipment.html', context)

    form = EquipmentForm(request.POST, request.FILES, instance=equip)
    context['form'] = form

    if (not form.is_valid()):
        return render(request, 'skieasy_app/update_equipment.html', context)

    equip.profile_id = Profile.objects.get(id=request.user.id)
    equip.title = form.cleaned_data["title"]
    equip.description = form.cleaned_data["description"]
    equip.price = form.cleaned_data["price"]
    equip.equipment_product_name = form.cleaned_data["equipment_product_name"]
    equip.bindings_product_name = form.cleaned_data["bindings_product_name"]
    equip.boots_product_name = form.cleaned_data["boots_product_name"]
    equip.skill_level = form.cleaned_data["skill_level"]
    equip.equipment_height = form.cleaned_data["equipment_height"]
    equip.boot_size = form.cleaned_data["boot_size"]
    equip.wear_status = form.cleaned_data["wear_status"]
    equip.equipment_type = form.cleaned_data["equipment_type"]
    equip.picture = form.cleaned_data["picture"]
    equip.content_type = form.cleaned_data["picture"].content_type

    equip.save()

    return redirect(equipment_details, id=id)


@login_required
@__profile_check
def update_listing(request, id):
    context = {}
    li = EquipmentListing.objects.get(id=id)
    context['title'] = li.equipment_id.title
    context['list_id'] = id
    context['form'] = EquipmentListingForm()

    if (request.method == "GET"):
        return render(request, 'skieasy_app/update_listing.html', context)

    form = EquipmentListingForm(request.POST)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'skieasy_app/update_listing.html', context)

    setattr(li, "start_date", form.cleaned_data['start_date'])
    setattr(li, "end_date", form.cleaned_data['end_date'])
    li.save()

    return redirect(display_listing, id=id)


@login_required
@__profile_check
def rent_listing(request, id):
    context = {}
    listing = EquipmentListing.objects.get(id=id)
    context["title"] = listing.equipment_id.title
    context["f_name"] = listing.profile_id.first_name
    context["l_name"] = listing.profile_id.last_name
    context["phone"] = listing.profile_id.phone_number

    new_res = EquipmentReservation(
        equipment_id=listing.equipment_id,
        profile_id=Profile.objects.get(user=request.user),
        start_date=listing.start_date,
        end_date=listing.end_date
    )

    new_res.save()
    listing.delete()

    return render(request, 'skieasy_app/rented.html', context)


@login_required
@__profile_check
def delete_equipment(request, id):
    equipment = Equipment.objects.filter(id=id)
    equipment_listings = EquipmentListing.objects.filter(equipment_id=id)
    equipment_listings.delete()
    equipment.delete()
    return redirect(display_equipment)


@login_required
@__profile_check
def get_photo(request, id):
    equip = get_object_or_404(Equipment, id=id)

    if not equip.picture:
        raise Http404

    return HttpResponse(equip.picture, content_type=equip.content_type)
