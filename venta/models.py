from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=120, db_index=True)
    sku = models.CharField(max_length=50, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.nombre} ({self.sku})"

class Cliente(models.Model):
    nombre = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.nombre

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha = models.DateTimeField(auto_now_add=True)
    anulada = models.BooleanField(default=False)
    
    @property
    def total(self):
        return sum(d.subtotal for d in self.detalles.all())
    
    def __str__(self):
        return f"Venta #{self.pk} — {self.cliente}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, related_name='detalles', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1)  # ← Agregué default
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ← Agregué default
    
    @property
    def subtotal(self):
        # Versión segura que evita el error None * None
        if self.cantidad is not None and self.precio_unitario is not None:
            return self.cantidad * self.precio_unitario
        return 0
    
    def __str__(self):
        return f"{self.producto} x{self.cantidad}"