import django_filters

from django_filters.rest_framework import FilterSet

from movie.models import Genre, Movie


class MovieFilter(FilterSet):
    year = django_filters.NumberFilter(lookup_expr='exact')
    language = django_filters.CharFilter(lookup_expr='icontains')
    country = django_filters.CharFilter(lookup_expr='icontains')

    genre = django_filters.CharFilter(
        field_name='genres__genre',
        lookup_expr='exact'
    )

    person = django_filters.CharFilter(
        field_name='persons__name',
        lookup_expr='exact'
    )

    class Meta:
        model = Movie
        fields = ['year', 'language', 'country', 'genre']