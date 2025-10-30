from django.contrib import admin
from django.http import HttpResponse
import csv
from django.utils import timezone
from .models import Producto, Cliente, Venta, DetalleVenta

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sku", "precio", "stock", "activo")
    search_fields = ("nombre", "sku")
    list_filter = ("activo",)
    ordering = ("nombre",)
    list_per_page = 25
    autocomplete_fields = ()

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "email")
    search_fields = ("nombre", "email")

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1
    autocomplete_fields = ("producto",)
    readonly_fields = ("subtotal_display",)
    
    def subtotal_display(self, obj):
        return f"${obj.subtotal:,.0f}" if obj.subtotal else "$0"
    subtotal_display.short_description = "Subtotal"

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    date_hierarchy = "fecha"
    list_display = ("id", "cliente", "fecha", "anulada", "total_display")
    search_fields = ("cliente__nombre", "id")
    list_filter = ("anulada", "fecha")
    inlines = [DetalleVentaInline]
    actions = ["exportar_ventas_csv"]
    
    @admin.display(description="Total", ordering="id")
    def total_display(self, obj):
        return f"${obj.total:,.0f}" if obj.total else "$0"
    
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('detalles__producto')
    
    @admin.action(description="Exportar ventas a CSV (por rango de fechas)")
    def exportar_ventas_csv(self, request, queryset):
        if not queryset:
            queryset = Venta.objects.all()
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte_ventas.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'ID Venta', 
            'Cliente', 
            'Fecha', 
            'Estado', 
            'Total Venta',
            'Productos',
            'Cantidad Total'
        ])
        
        for venta in queryset:
            productos = ", ".join([
                f"{detalle.producto.nombre} (x{detalle.cantidad})" 
                for detalle in venta.detalles.all()
            ])
            
            cantidad_total = sum(
                detalle.cantidad for detalle in venta.detalles.all()
            )
            
            writer.writerow([
                venta.id,
                venta.cliente.nombre,
                venta.fecha.strftime("%Y-%m-%d %H:%M"),
                "ANULADA" if venta.anulada else "ACTIVA",
                f"${venta.total:,.0f}" if venta.total else "$0",
                productos,
                cantidad_total
            ])
        
        return response
    
    def get_list_filter(self, request):
        base_filters = super().get_list_filter(request)
        return base_filters + (FechaRangoFilter,)

class FechaRangoFilter(admin.SimpleListFilter):
    title = 'rango de fechas'
    parameter_name = 'fecha_rango'
    
    def lookups(self, request, model_admin):
        return (
            ('hoy', 'Hoy'),
            ('esta_semana', 'Esta semana'),
            ('este_mes', 'Este mes'),
            ('ultimos_7_dias', 'Últimos 7 días'),
            ('ultimos_30_dias', 'Últimos 30 días'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'hoy':
            hoy = timezone.now().date()
            return queryset.filter(fecha__date=hoy)
        
        elif self.value() == 'esta_semana':
            hoy = timezone.now().date()
            inicio_semana = hoy - timezone.timedelta(days=hoy.weekday())
            return queryset.filter(fecha__date__gte=inicio_semana)
        
        elif self.value() == 'este_mes':
            hoy = timezone.now().date()
            inicio_mes = hoy.replace(day=1)
            return queryset.filter(fecha__date__gte=inicio_mes)
        
        elif self.value() == 'ultimos_7_dias':
            hoy = timezone.now().date()
            hace_7_dias = hoy - timezone.timedelta(days=7)
            return queryset.filter(fecha__date__gte=hace_7_dias)
        
        elif self.value() == 'ultimos_30_dias':
            hoy = timezone.now().date()
            hace_30_dias = hoy - timezone.timedelta(days=30)
            return queryset.filter(fecha__date__gte=hace_30_dias)
        
        return queryset