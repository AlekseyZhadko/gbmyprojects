from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from recipe_app.models import CategoryRecipe
from recipe_app.forms import LoginForm, SignupForm


def base(request):
    form_login_view = LoginForm(data=request.POST or None)
    if 'button_form_login_view' in request.POST:
        if form_login_view.is_valid():
            username = form_login_view.cleaned_data['username']
            password = form_login_view.cleaned_data['password']
            user = authenticate(username=username, password=password)  # Проверяем учетные данные
            if user is not None:
                login(request, user)  # Выполняем вход
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    category_recipes = CategoryRecipe.objects.filter(is_deleted=False)
    return {
        'category_recipes': category_recipes,
        # 'form_signup_view': form_signup_view,
        'form_login_view': form_login_view,
    }

    # form = LoginForm(data=request.POST or None)
    # if request.method == 'POST':
    #     if form.is_valid():
    #         username = form.cleaned_data['username']
    #         password = form.cleaned_data['password']
    #         user = authenticate(username=username, password=password)  # Проверяем учетные данные
    #         if user is not None:
    #             login(request, user)  # Выполняем вход
    #             return redirect('home')  # Перенаправляем на главную страницу
    # return render(request, 'login.html', {'form': form})