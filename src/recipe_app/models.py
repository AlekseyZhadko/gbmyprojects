import datetime
import os

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


# Create your models here.
def get_upload_path_category(instance, filename):
    """ Возвращает путь по которому необходимо сохрнаить документ () """
    return "category/{file}".format(file=filename)


'''Модель категория рецептов'''


class CategoryRecipe(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название категории', blank=True, null=True)
    description = models.TextField(verbose_name='Описание категории', blank=True, null=True)
    picture = models.ImageField(verbose_name='Изображение', upload_to=get_upload_path_category, blank=True, null=True)
    is_deleted = models.BooleanField(default=False, verbose_name='Не отображать')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория рецептов'
        verbose_name_plural = 'Категории рецептов'


def get_upload_path(instance, filename):
    """ Возвращает путь по которому необходимо сохрнаить документ () """
    return "recipe/{year}/{category_id}/{file}".format(category_id=instance.category.pk,
                                                       year=datetime.datetime.now().year,
                                                       file=filename)


'''Модель рецепты'''


class Recipe(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название рецепта')
    description = RichTextUploadingField(verbose_name='Описание рецепта', blank=True, null=True)
    cooking_steps = models.TextField(verbose_name='Шаги приготовления', blank=True, null=True)
    cooking_time = models.TimeField(verbose_name='Время приготовления ', blank=True, null=True)
    picture = models.ImageField(verbose_name='Изображение', upload_to=get_upload_path)
    autor = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, blank=True, null=True)
    create_date = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    category = models.ForeignKey(CategoryRecipe, verbose_name='Категория рецепта', on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False, verbose_name='Не отображать')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


@receiver(models.signals.post_delete, sender=Recipe)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.picture:
        if os.path.isfile(instance.picture.path):
            os.remove(instance.picture.path)


@receiver(models.signals.pre_save, sender=Recipe)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Recipe.objects.get(pk=instance.pk).picture
    except Recipe.DoesNotExist:
        return False

    new_file = instance.picture
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
