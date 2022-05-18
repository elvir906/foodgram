from django.contrib import admin

from .models import Ingredients
from .models import Tags
from .models import Recipes
from .models import Favorite
from .models import Cart

admin.site.register(Ingredients)
admin.site.register(Tags)
admin.site.register(Recipes)
admin.site.register(Cart)
admin.site.register(Favorite)
