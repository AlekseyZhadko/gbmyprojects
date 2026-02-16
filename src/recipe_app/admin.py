from django.contrib import admin

from recipe_app.models import CategoryRecipe, Recipe

# Register your models here.
admin.site.register(CategoryRecipe)
admin.site.register(Recipe)
