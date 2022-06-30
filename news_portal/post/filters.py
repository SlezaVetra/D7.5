import django_filters
from django import forms

from .models import Post


class PostFilter(django_filters.FilterSet):
    """Фильтр для поиска по записям Post."""
    created_at = django_filters.DateFilter(
        label="created_at",
        lookup_expr="lte",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = {
            'title': ['contains'],
            'text': ['contains'],
        }
