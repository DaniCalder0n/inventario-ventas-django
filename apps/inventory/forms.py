from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'name', 'description', 'stock', 'min_stock', 'expiry_date',
                  'cost_price', 'sale_price', 'image', 'is_featured', 'is_active']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field.widget, (forms.CheckboxInput, forms.FileInput)):
                field.widget.attrs.setdefault('class', 'form-control')

class StockUpdateForm(forms.Form):
    quantity = forms.IntegerField(label='Cantidad', min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    movement_type = forms.ChoiceField(choices=[('in', 'Entrada'), ('out', 'Salida'), ('adjustment', 'Ajuste')], widget=forms.Select(attrs={'class': 'form-select'}))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}))

class ProductSearchForm(forms.Form):
    q = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar productos...'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False, empty_label='Todas las categorías', widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(choices=[('', 'Todos'), ('active', 'Activos'), ('low', 'Stock bajo'), ('out', 'Agotados')], required=False, widget=forms.Select(attrs={'class': 'form-select'}))
