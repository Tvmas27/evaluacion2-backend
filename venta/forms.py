from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa el nombre del producto',
                'required': True
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'placeholder': '0.00',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe las características del producto (opcional)'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0',
                'placeholder': '0',
                'value': '0'
            }),
        }
        labels = {
            'nombre': 'Nombre del Producto',
            'precio': 'Precio',
            'descripcion': 'Descripción',
            'stock': 'Stock'
        }
        help_texts = {
            'nombre': 'Máximo 200 caracteres.',
            'precio': 'Ingresa el precio del producto (puede incluir centavos).',
            'descripcion': 'Campo opcional. Proporciona una descripción detallada del producto.',
            'stock': 'Cantidad disponible en inventario.'
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio and precio <= 0:
            raise forms.ValidationError('El precio debe ser mayor a 0.')
        return precio

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock and stock < 0:
            raise forms.ValidationError('El stock no puede ser negativo.')
        return stock