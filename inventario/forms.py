from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'})
    )
    descripcion = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Descripción del producto'})
    )
    precio = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio'})
    )

    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio']

    def clean_precio(self):
        precio = self.cleaned_data['precio']
        if precio < 0:
            raise forms.ValidationError("El precio debe ser mayor o igual a 0")
        return precio
