from skieasy_app.forms import ProfileForm
from skieasy_app.models import Profile, Equipment, EquipmentImages, EquipmentListing
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template import loader

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

@login_required
def listing(request):
    template = loader.get_template('skieasy_app/listing.html')
    equipment = Equipment.objects.filter(id=1).values()
    images = EquipmentImages.objects.filter(equipmentId=1).values()[:4]
    # context = {
    #     'title':'The best skis ever',
    #     'description':equipment.description,
    #     'price':equipment.price,
    #     'quantity':'1',
    #     'images': images,
    #     'length': '1',
    # }
    context = {
        'title':'The best skis ever',
        'description':'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam volutpat augue non odio feugiat, in interdum sapien pharetra. Sed vel commodo justo. Vivamus ac lectus suscipit, venenatis tortor nec, bibendum augue. Proin eget gravida risus. Vivamus tempor semper augue, nec consequat sem interdum in.',
        'price':'100',
        'quantity':'1',
        'image': 'https://picsum.photos/id/3/400/400',
        'length': '1',
    }
    return HttpResponse(template.render(context, request))