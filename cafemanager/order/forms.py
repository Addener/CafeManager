import json
from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('id', 'table_number', 'items')
        labels = {
            'id': 'Заказ №',
            'table_number': 'Стол №',
            'items': 'Блюдо/Стоимость (через запятую)',
        }
        widgets = {
            'items': forms.Textarea(attrs={'rows': 5}),
        }
       
    def clean_items(self):
        items_str = self.cleaned_data['items']
        try:
            items = Order.parse_items(items_str)
            self.cleaned_data['items'] = json.dumps(items)
        except ValueError as e:
            raise forms.ValidationError(str(e))
        return self.cleaned_data['items']
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.total_price = sum(item['price'] for item in json.loads(self.cleaned_data['items']))

        if commit:
            instance.save()
        return instance
    
    
class OrderFilterForm(forms.Form):
    order_id = forms.IntegerField(label='Заказ №', required=False) 
    table_number = forms.IntegerField(label='Стол №', required=False)
    status = forms.ChoiceField(label='Статус', choices=[('Все', 'Все')] + Order.STATUS_CHOISES, required=False)
    
    
class OrderStatusForm(forms.Form):
    status = forms.ChoiceField(label='Статус', choices=Order.STATUS_CHOISES, required=True)
