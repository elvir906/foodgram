from django.contrib import admin

from .models import Ingredients
from .models import Tag
from .models import Recipes

admin.site.register(Ingredients)
admin.site.register(Tag)
admin.site.register(Recipes)
