from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Categoria, Producto, Cliente, Venta, DetalleVenta
from .serializers import (
    CategoriaSerializer, 
    ProductoSerializer, 
    ClienteSerializer, 
    VentaSerializer, 
    DetalleVentaSerializer
)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre']

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    filterset_fields = ['categoria', 'precio']
    ordering_fields = ['precio', 'stock', 'fecha_creacion']

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['nombre', 'email']

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['cliente', 'fecha_venta']
    ordering_fields = ['fecha_venta', 'total']

class DetalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all()
    serializer_class = DetalleVentaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['venta', 'producto']

