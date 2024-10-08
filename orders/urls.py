from django.urls import path
from .views import *
app_name = 'orders'

urlpatterns = [
    path('current/', CurrentOrderDetailView.as_view(), name='current_order_detail'),
    path('current/<int:table_id>/', CurrentOrderDetailView.as_view(), name='current_order_detail_with_id'),
    
    path('delete_order/<int:table_id>/', CurrentOrderDeleteView.as_view(), name='current_order_delete'),
    
    path('update/<int:pk>/', OrderUpdateView.as_view(), name='order_detail_update'),
    path('delete/<int:pk>/', OrderDeleteView.as_view(), name='order_detail_delete'),
    
    path('confirm/', confirm_order_view, name='confirm_order'),
    path('conclude_evening/', conclude_evening_view, name='conclude_evening'),
    path('confirm/<int:table_id>/', confirm_order_view, name='confirm_order_with_id'),
    path('conclude_evening/<int:table_id>/', conclude_evening_view, name='conclude_evening_with_id'),

    path('update_order_detail_status/<int:order_detail_id>/', update_order_detail_status, name='update_order_detail_status'),
    
    path('recommendations/<int:pk>/', order_recommendations_view, name='order_recommendations'),

    path('statistics/', orders_statistics, name='statistics'),



]
