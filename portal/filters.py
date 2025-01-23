from django_filters import FilterSet
from .models import *
import django_filters

class PostFilter(FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains')
    author = django_filters.CharFilter(field_name='author', lookup_expr='exact')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    conjoined=True
    class Meta:
        model = Post
        fields = [
            'title',
            'author',
            'created_at',
        ]
