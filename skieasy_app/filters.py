import django_filters
from django.db.models import Q, Case, When, Value, CharField


from .models import Equipment, EquipmentListing


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

    '''
    Pass gender query params to request equipment for a specific
    gender.
    Ex:
    <url>?gender=Female => equipment that is for females
    '''
    gender = django_filters.CharFilter(
        field_name='profile_id__gender'
    )

    class Meta:
        model = Equipment
        fields = [
            'equipment_type',
            'wear_status',
            'boot_size',
            'equipment_height',
        ]

    def filter_neighborhood(self, queryset, name, value):
        neighborhoods = value.split(',')
        return queryset.filter(profile_id__neighborhood__in=neighborhoods)

    def filter_queryset(self, queryset):
        '''
        Pass start-end_date params to request equipment that has
        availability within a range of dates. This requires a cross-table
        join with listings to check for overlapping intervals.
        Ex:
        <url>?start_date=2023-10-24&end_date=2023-12-24

        TODO => Will eventually need to also account for reservations
        '''

        queryset = super().filter_queryset(queryset)

        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date and end_date:
            queryset = queryset.filter(
                Q(equipment_listings__start_date__lte=end_date) &
                Q(equipment_listings__end_date__gte=start_date)
            )
            queryset = queryset.annotate(
                overlap_start_date=Case(
                    When(
                        equipment_listings__start_date__gte=start_date,
                        equipment_listings__start_date__lte=end_date,
                        then='equipment_listings__start_date'
                    ),
                    When(
                        equipment_listings__start_date__lte=start_date,
                        then=Value(start_date)
                    ),
                    output_field=CharField()
                ),
                overlap_end_date=Case(
                    When(
                        equipment_listings__end_date__gte=start_date,
                        then=Value(end_date)
                    ),
                    When(
                        equipment_listings__end_date__lte=end_date,
                        then='equipment_listings__end_date'
                    ),
                    output_field=CharField()
                )
            )
        return queryset
