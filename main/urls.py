from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, api_root
from django.contrib import admin
from venta.views import (
    CategoriaViewSet, 
    ProductoViewSet, 
    ClienteViewSet, 
    VentaViewSet, 
    DetalleVentaViewSet
)

# Configurar el router para las viewsets
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'ventas', VentaViewSet)
router.register(r'detalles-venta', DetalleVentaViewSet)

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls), 
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls')),
]