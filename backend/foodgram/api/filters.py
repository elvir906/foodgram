from django.contrib.auth import get_user_model
from django_filters.rest_framework import FilterSet, filters
from rest_framework.filters import SearchFilter

from recipes.models import Recipes

User = get_user_model()


class IngredientsSearchFilter(SearchFilter):
    search_param = 'name'


class AuthorAndTagSearchFilter(FilterSet):
    tags = filters.AllValuesMultipleFilter(field_name='tags__slug')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorite = filters.BooleanFilter(method='is_favorite_filter')
    is_in_shopping_cart = filters.BooleanFilter(
        method='is_in_cart_filter')

    def is_favorite_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(favorite__user=self.request.user)
        return queryset

    def is_in_cart_filter(self, queryset, name, value):
        if value and not self.request.user.is_anonymous:
            return queryset.filter(cart__user=self.request.user)
        return queryset

    class Meta:
        model = Recipes
        fields = ('tags', 'author')
