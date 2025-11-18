from django.contrib import admin
from .models import Categoria, Producto, Cliente, Venta, DetalleVenta

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion']
    list_display_links = ['id', 'nombre']
    search_fields = ['nombre']
    list_per_page = 20

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'precio', 'stock', 'categoria', 'fecha_creacion']
    list_display_links = ['id', 'nombre']
    list_filter = ['categoria', 'fecha_creacion']
    search_fields = ['nombre', 'descripcion']
    list_editable = ['precio', 'stock']
    list_per_page = 20

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'email', 'telefono', 'fecha_registro']
    list_display_links = ['id', 'nombre']
    search_fields = ['nombre', 'email']
    list_per_page = 20

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    readonly_fields = ['subtotal']

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'fecha_venta', 'total']
    list_display_links = ['id']
    list_filter = ['fecha_venta', 'cliente']
    search_fields = ['cliente__nombre', 'id']
    readonly_fields = ['total', 'fecha_venta']
    inlines = [DetalleVentaInline]
    list_per_page = 20

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ['cliente']
        return self.readonly_fields

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['id', 'venta', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_display_links = ['id']
    list_filter = ['producto', 'venta']
    search_fields = ['producto__nombre', 'venta__id']
    readonly_fields = ['subtotal']
    list_per_page = 20