from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.logout_view, name='logout'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/buscar/', views.buscar_categorias, name='buscar_categorias'),
    path('categorias/<int:categoria_id>/', views.productos_por_categoria, name='productos_por_categoria'),
    path('categorias/<int:categoria_id>/buscar/', views.buscar_productos_categoria, name='buscar_productos_categoria'),
]