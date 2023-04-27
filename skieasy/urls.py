"""skieasy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from skieasy_app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.welcome, name='welcome'),
    path('register', views.register, name='register'),
    path('home', views.HomeView.as_view(), name='home'),
    path('home_query_generator', views.home_query_generator, name='home_query_generator'),
    path('equipment-details/<int:id>', views.equipment_details, name="equipment-details"),
    path('manage', views.manage, name='manage'),
    path('listing', views.listing, name='listing'),
    path('create-equipment', views.create_equipment, name='create-equipment'),
    path('display-equipment', views.display_equipment, name='display-equipment'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('logout', auth_views.logout_then_login, name='logout'),
    path('create-listing/<int:id>', views.create_listing, name='create-listing'),
    path('display-listing/<int:id>', views.display_listing, name='display-listing'),
    path('update-equipment/<int:id>', views.update_equipment, name='update-equipment')
]
