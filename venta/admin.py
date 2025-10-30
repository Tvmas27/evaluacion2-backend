from django.contrib import admin
from .models import Producto, Cliente, Venta, DetalleVenta

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sku", "precio", "stock", "activo")
    search_fields = ("nombre", "sku")  # texto rápido
    list_filter = ("activo",)  # filtros laterales
    ordering = ("nombre",)
    list_per_page = 25
    autocomplete_fields = ()  # ej.: ("categoria",) si existiera FK grande

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email")
    search_fields = ("nombre", "email")

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    autocomplete_fields = ("producto",)
    readonly_fields = ("subtotal",)

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    date_hierarchy = "fecha"
    list_display = ("id", "cliente", "fecha", "anulada", "total_display")
    search_fields = ("cliente__nombre", "id")  # lookups a relacionadas
    list_filter = ("anulada",)
    inlines = [DetalleVentaInline]
    
    @admin.display(description="Total", ordering="id")
    def total_display(self, obj):
        return f"${obj.total:,.0f}"