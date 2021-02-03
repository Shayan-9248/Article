from django import forms
import django_filters
from .models import *


class ProductFilter(django_filters.FilterSet):
    CHOICE_1 = {
        ('most_visit', 'most'),
        ('fewer', 'fewer')
    }

    brand = django_filters.ModelMultipleChoiceFilter(queryset=Brand.objects.all(), widget=forms.CheckboxSelectMultiple())
    visit_count = django_filters.ChoiceFilter(choices=CHOICE_1, method='visit_filter')


    def visit_filter(self, queryset, name, value):
        data = '-visit_count' if value == 'fewer' else 'visit_count'
        return queryset.order_by(data)