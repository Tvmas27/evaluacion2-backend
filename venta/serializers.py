from  rest_framework import serializers
from .models import Venta
from .models import Cliente
from .models import DetalleVenta
from .models import Producto

class VentaSerializer(serializers.ModelSerializer): 
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Venta
        fields = ['nombre', 
                  'sku', 
                  'precio', 
                  'stock', 
                  'activo']
        

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['nombre',
                   'email']
        

class DetalleVentaSerializer(serializers.ModelSerializer):
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = DetalleVenta
        fields = ['producto',
                  'cantidad',
                  'precio_unitario',
                  'subtotal']
        
class VentaDetailSerializer(serializers.ModelSerializer):  
    cliente = ClienteSerializer()
    detalles = DetalleVentaSerializer(many=True)
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Venta
        fields = ['cliente',
                  'fecha',
                  'anulada',
                  'detalles',
                  'total']