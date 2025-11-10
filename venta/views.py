from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from .models import Producto , DetalleVenta
from .forms import ProductoForm

from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from .serializers import GroupSerializer, UserSerializer , ProductoSerializer , DetalleVentaSerializer



class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by('nombre')
    serializer_class = ProductoSerializer
    Permission_classes = [permissions.IsAuthenticated]

class groupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('')
    serializer_class = GroupSerializer
    Permission_classes = [permissions.IsAuthenticated]

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('')
    serializer_class = UserSerializer
    Permission_classes = [permissions.IsAuthenticated]


class detalleVentaViewSet(viewsets.ModelViewSet):
    queryset = DetalleVenta.objects.all().order_by('')
    serializer_class = DetalleVentaSerializer
    Permission_classes = [permissions.IsAuthenticated]


