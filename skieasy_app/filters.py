import django_filters
from .models import Equipment


class EquipmentFilter(django_filters.FilterSet):
    '''
    Pass min-max price query params to request equipment within a 
    range of prices.
    Ex:
    <url>?min_price=10&max_price=20 => equipment within [$10, $20]
    '''
    min_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte'
    )
    max_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='lte'
    )

    '''
    Pass min-max boot_size query params to request equipment within a
    range of boot sizes.
    Ex:
    <url>?min_boot_size=9&max_boot_size=10 => equipment with boots
    within [9,10]
    '''
    min_boot_size = django_filters.NumberFilter(
        field_name='boot_size', lookup_expr='gte'
    )
    max_boot_size = django_filters.NumberFilter(
        field_name='boot_size', lookup_expr='lte'
    )

    '''
    Pass min-max equipment_height params to request equipment within a
    range of heights.
    Ex:
    <url>?min_equipment_height=70&max_equipment_height=80 => equipment
    with a height within [70,80]
    '''
    min_equipment_height = django_filters.NumberFilter(
        field_name='equipment_height', lookup_expr='gte'
    )
    max_equipment_height = django_filters.NumberFilter(
        field_name='equipment_height', lookup_expr='lte'
    )

    '''
    Pass neighborhoods query params to request equipment that resides
    within one of the neighborhoods.
    Ex:
    <url>?neighborhoods=Downtown,Shadyside => equipment that is located
    within (Downtown, Shadyside)
    '''
    neighborhoods = django_filters.CharFilter(
        method='filter_neighborhood'
    )

    # TODO -> add filter to find equipment with [start_date, end_date]
    # & using intervals algo

    class Meta:
        model = Equipment
        fields = [
            # default filter for a field will match 'exact'
            'equipment_type',
            'wear_status', 
            'boot_size', 
            'equipment_height',
        ]

    def filter_neighborhood(self, queryset, name, value):
        neighborhoods = value.split(',')
        return queryset.filter(profile_id__neighborhood__in=neighborhoods)
