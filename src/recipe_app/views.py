from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from .models import CategoryRecipe, Recipe

from .forms import RecipeForm, SignupForm, LoginForm

''' Главная страница '''


# Create your views here.
def index(request):
    new_recipes = Recipe.objects.filter(is_deleted=False).order_by('-id')[:6]
    category_recipe = CategoryRecipe.objects.filter(is_deleted=False)[:3]
    return render(request, 'recipe_app/index.html',
                  {
                      'category_recipe': category_recipe,
                      'new_recipes': new_recipes,
                  })


''' Страница рецептов определенной категории '''


def recipe(request, category_id, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    return render(request, 'recipe_app/recipe.html',
                  {
                      'recipe': recipe,
                  })


''' Страница рецептов определенной категории '''


def category(request, category_id):
    new_recipes = Recipe.objects.filter(category__id=category_id, is_deleted=False)
    category_name = CategoryRecipe.objects.get(id=category_id)

    paginator = Paginator(new_recipes, 9)  # Show 9 contacts per page.
    page_number = request.GET.get("page")
    new_recipes = paginator.get_page(page_number)

    return render(request, 'recipe_app/category_recipes.html',
                  {
                      'new_recipes': new_recipes,
                      'category_name': category_name,
                  })


''' Страница новые рецепты '''


def new_recipe(request):
    new_recipes = Recipe.objects.filter(is_deleted=False)

    paginator = Paginator(new_recipes, 9)  # Show 9 contacts per page.
    page_number = request.GET.get("page")
    new_recipes = paginator.get_page(page_number)

    return render(request, 'recipe_app/new_recipe.html',
                  {
                      'new_recipes': new_recipes,
                  })


''' Страница все категории '''


def category_all(request):
    category_recipe = CategoryRecipe.objects.filter(is_deleted=False)
    return render(request, 'recipe_app/category_all.html',
                  {
                      'category_recipe': category_recipe,
                  })


''' Страница о нас '''


def about(request):
    return render(request, 'recipe_app/about.html',
                  {})


''' Форма редактирования рецепта '''


@login_required(login_url='/')
def recipe_form_edit(request, pk):
    recipe = get_object_or_404(Recipe, id=pk)
    if request.method == 'GET':
        context = {'form': RecipeForm(instance=recipe), 'id': pk, 'recipe': Recipe.objects.get(pk=pk)}
        return render(request, 'recipe_app/recipe_edit.html', context)
    elif request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.instance.autor = request.user
            picture = form.cleaned_data['picture']
            form.save()
            return redirect('/recipe/user/' + str(request.user.pk))


''' Форма создания рецепта '''


@login_required(login_url='/')
def recipe_form(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.autor = request.user
            picture = form.cleaned_data['picture']
            form.save()
            return redirect('/recipe/add')
    else:
        form = RecipeForm()
    return render(request, 'recipe_app/recipe_add.html', {'form': form})


''' Страница рецептов пользователя '''


@login_required(login_url='/')
def recipe_user(request, pk):
    recipe_user = Recipe.objects.filter(autor__pk=pk, is_deleted=False).order_by('-id')
    return render(request, 'recipe_app/recipe_user.html', {'recipe_user': recipe_user})


''' Форма регистрации на сайте'''


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()  # Сохраняем нового пользователя
            login(request, user)  # Выполняем вход
            return redirect('/')  # Перенаправляем на главную страницу
    else:
        form = SignupForm()
    return render(request, 'includes/signup.html', {'form': form})


''' Форма входа на сайт'''


def signin(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)  # Проверяем учетные данные
            if user is not None:
                login(request, user)  # Выполняем вход
                return redirect('/')  # Перенаправляем на главную страницу
    return render(request, 'includes/signin.html', {'form': form})
