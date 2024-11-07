from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, EditProfileForm
from .models import Profile, Producto, TipoProducto
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Vista para mostrar todas las categorías (tipos de productos)
def lista_categorias(request):
    categorias = TipoProducto.objects.all()
    return render(request, 'productos/lista_categorias.html', {'categorias': categorias})

# Vista para mostrar los productos de una categoría específica
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(TipoProducto, id=categoria_id)
    productos = Producto.objects.filter(tipo=categoria)
    return render(request, 'productos/lista_productos.html', {'productos': productos, 'categoria': categoria})

# Vistas existentes
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                messages.success(request, 'Inicio de sesión exitoso.')
                return redirect('productos:lista_categorias')  # Redirige a la lista de categorías después de iniciar sesión
    else:
        form = AuthenticationForm()
    return render(request, 'productos/login.html', {'form': form})

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista_productos.html', {'productos': productos})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro exitoso.')
            return redirect('productos:login')
    else:
        form = UserRegistrationForm()
    return render(request, 'productos/register.html', {'form': form})

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'productos/user_profile.html', {
        'username': request.user.username,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'email': request.user.email,
        'phone_number': profile.phone_number if profile else "No disponible",
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado con éxito.')
            return redirect('productos:user_profile')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'productos/edit_profile.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión.')
    return redirect('productos:login')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Mantiene al usuario conectado
            messages.success(request, 'Contraseña cambiada con éxito.')
            return redirect('productos:user_profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'productos/change_password.html', {'form': form})


# Vista para mostrar todas las categorías
def lista_categorias(request):
    categorias = TipoProducto.objects.all()
    return render(request, 'productos/lista_categorias.html', {'categorias': categorias})

# Vista para manejar la búsqueda de categorías en tiempo real
def buscar_categorias(request):
    query = request.GET.get('q', '')
    categorias = TipoProducto.objects.filter(nombre__icontains=query)
    categorias_data = [{'id': c.id, 'nombre': c.nombre} for c in categorias]

    return JsonResponse({'categorias': categorias_data, 'resultado': len(categorias_data) > 0})

# Vista para mostrar productos por categoría
def productos_por_categoria(request, categoria_id):
    categoria = get_object_or_404(TipoProducto, id=categoria_id)
    productos = Producto.objects.filter(tipo=categoria)
    return render(request, 'productos/productos_por_categoria.html', {
        'categoria': categoria,
        'productos': productos
    })

# Vista AJAX para la búsqueda de productos dentro de una categoría
def buscar_productos_categoria(request, categoria_id):
    query = request.GET.get('q', '')
    categoria = get_object_or_404(TipoProducto, id=categoria_id)
    productos = Producto.objects.filter(tipo=categoria, nombre__icontains=query)
    productos_data = [{'nombre': p.nombre, 'precio': str(p.precio), 'imagen': p.imagen.url, 'descripcion': p.descripcion} for p in productos]

    return JsonResponse({'productos': productos_data, 'resultado': len(productos_data) > 0})