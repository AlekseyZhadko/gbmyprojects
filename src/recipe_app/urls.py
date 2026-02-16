from django.urls import path
from .views import (index, recipe, category, new_recipe, category_all, recipe_form, signin, signup,
                    recipe_user, recipe_form_edit, about)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  path('', index, name='index'),
                  path('signup/', signup, name='signup'),
                  path('signin/', signin, name='signin'),
                  path('about/', about, name='about'),
                  path('new_recipe/', new_recipe, name='new_recipe'),
                  path('recipe/user/<int:pk>', recipe_user, name='recipe_user'),
                  path('recipe/add/', recipe_form, name='recipe_form'),
                  path('recipe/edit/<int:pk>', recipe_form_edit, name='recipe_form_edit'),
                  path('category_all/', category_all, name='category_all'),
                  path('category/<int:category_id>/', category, name='category'),
                  path('category/<int:category_id>/recipe/<int:recipe_id>/', recipe, name='recipe'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
