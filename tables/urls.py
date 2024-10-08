# menu/urls.py
from django.urls import path
from .views import *
app_name = 'tables'

urlpatterns = [
    path('', TableListView.as_view(), name='table_list'),
    path('<int:pk>/', TableDetailView.as_view(), name='table_detail'),
    path('my_table/', user_table_redirect, name='my_table'),
    path('update/<int:pk>/', TableUpdateView.as_view(), name='table_update'),
    path('delete/<int:pk>/', TableDeleteView.as_view(), name='table_delete'),

   
]

