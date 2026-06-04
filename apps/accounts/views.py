from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .forms import LoginForm, RegisterForm, UserAdminForm
from .models import CustomUser
from .decorators import admin_required

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'accounts/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Bienvenido, {user.get_full_name() or user.username}!')
            return redirect(request.GET.get('next', 'dashboard'))
        return render(request, 'accounts/login.html', {'form': form})

class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register.html', {'form': RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('catalog')
        return render(request, 'accounts/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@admin_required
def user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})

@admin_required
def user_create(request):
    form = UserAdminForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario creado.')
        return redirect('user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Crear Usuario'})

@admin_required
def user_edit(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    form = UserAdminForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Usuario actualizado.')
        return redirect('user_list')
    return render(request, 'accounts/user_form.html', {'form': form, 'title': 'Editar Usuario'})

@admin_required
def user_delete(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Usuario eliminado.')
        return redirect('user_list')
    return render(request, 'accounts/user_confirm_delete.html', {'user': user})
