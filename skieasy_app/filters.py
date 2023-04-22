import django_filters
from .models import Equipment


class EquipmentFilter(django_filters.FilterSet):
    # pass min-max price query params to request equipment in a range of prices 
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    # pass min-max_boot_size query params to request equipment in a range of sizes
    min_boot_size = django_filters.NumberFilter(field_name='boot_size', lookup_expr='gte')
    max_boot_size = django_filters.NumberFilter(field_name='boot_size', lookup_expr='lte')

    # pass min-max_equipment_height query params to request equipment in a range of heights
    min_equipment_height = django_filters.NumberFilter(field_name='equipment_height', lookup_expr='gte')
    max_equipment_height = django_filters.NumberFilter(field_name='equipment_height', lookup_expr='lte')

    # pass acceptable neighborhoods query params to request equipment that resides in those neighborhoods
    # passed in like so 'neighborhoods=Downtown,Shadyside,Southside'
    neighborhoods = django_filters.CharFilter(method='filter_neighborhood')

    # TODO -> add filter to find equipment provided start_date, end_date & using intervals algo

    class Meta:
        model = Equipment
        fields = [
            'equipment_type', # default for field will match 'exact' filter
            'wear_status', 
            'boot_size', 
            'equipment_height',
        ]

    def filter_neighborhood(self, queryset, name, value):
        neighborhoods = value.split(',')
        return queryset.filter(profile_id__neighborhood__in=neighborhoods)
