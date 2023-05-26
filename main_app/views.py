from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CreateUserForm

# Create your views here.


def home(request):
    return render(request,
                  'main_app/home.html')


def register_request(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {user}')
            return redirect('main_app:login')

    return render(request, 'main_app/register.html', context={'register_form': form})


def login_request(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main_app:user_view')
        else:
            messages.info(request, 'Wrong username or password')

    return render(request, 'main_app/login.html')


def user_view(request):
    return render(request, 'main_app/user_logged.html')


def logout_request(request):
    logout(request)
    return redirect('main_app:home')
