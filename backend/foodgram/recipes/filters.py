from django_filters.rest_framework import FilterSet, filters
from django_filters.widgets import CSVWidget

from .models import Recipe


class RecipeFilterSet(FilterSet):
    tags = filters.CharFilter(
        distinct=True, widget=CSVWidget, method='filter_tags'
    )
    name = filters.CharFilter()

    class Meta:
        model = Recipe
        fields = ['name', 'tags']

    def filter_tags(self, queryset, name, value):
        return queryset.filter(tags__name__in=value)
