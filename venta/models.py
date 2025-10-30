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

class Venta(models.Model):  # ← Agregué 'class' que faltaba
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
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"{self.producto} x{self.cantidad}"