from django.urls import path

from . import views

urlpatterns = [
    path('add/', views.add_order, name='add_order'),
    path('management/', views.OrderListView.as_view(), name='orders_management'),
    path('delete/<pk>/', views.delete_order, name='delete_order'),
    path('income/', views.IncomeCalculationListView.as_view(), name='income_calculation'),
]
