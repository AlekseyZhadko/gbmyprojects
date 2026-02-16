from django.apps import AppConfig


class RecipeAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipe_app'
    verbose_name = 'Сайт рецептов'
    verbose_name_plural = 'Сайт рецептов'
