from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('order.urls')),
    path('create/', views.OrderCreateView.as_view(), name='order_create'),
]
