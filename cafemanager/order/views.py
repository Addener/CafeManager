from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView

from .forms import OrderForm, OrderFilterForm, OrderStatusForm
from .models import Order

def add_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Заказ успешно добавлен!')
            return redirect('add_order')
    else:
        form = OrderForm()
    return render(request, 'order/add_order.html', {'form': form})


class OrderListView(ListView):
    model = Order
    template_name = 'order/orders_management.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderFilterForm()
        context['STATUS_CHOISES'] = Order.STATUS_CHOISES
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        form = OrderFilterForm(self.request.GET)
        if form.is_valid():
            order_id = form.cleaned_data['order_id']
            table_number = form.cleaned_data['table_number']
            status = form.cleaned_data['status']
            if order_id:
                queryset = queryset.filter(id=order_id)
            if table_number:
                queryset = queryset.filter(table_number=table_number)
            if status and status != 'Все':
                queryset = queryset.filter(status=status)
        return queryset
    
    def post(self, request, *args, **kwargs):
        status_form = OrderStatusForm(request.POST)
        if status_form.is_valid():
            table_number = request.POST.get('table_number')
            order = Order.objects.get(table_number=table_number)
            order.status = status_form.cleaned_data['status']
            order.save()
            return redirect('orders_management')
        return redirect('orders_management')

def delete_order(request, pk):
    order = Order.objects.get(pk=pk)
    order.delete()
    return redirect('orders_management')


class IncomeCalculationListView(ListView):
    model = Order
    template_name = 'order/income_calculation.html'
    
    def get_queryset(self):
        return Order.objects.filter(status='Оплачено')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_price'] = sum(order.total_price for order in self.get_queryset())
        return context
