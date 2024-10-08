# menu/urls.py
from django.urls import path
from .views import *
app_name = 'menu'

urlpatterns = [
    # path per la lista dei piatti
    path('', MenuListView.as_view(), name='menu'),
    
    # path per operazioni CRUD sui piatti
    path('new_dish/', DishCreateView.as_view(), name='dish_create'),
    path('edit_dish/<pk>', DishUpdateView.as_view(), name='dish_edit'),
    path('delete_dish/<pk>', DishDeleteView.as_view(), name='dish_delete'),
    path('detail_dish/<pk>', DishDetailView.as_view(), name='dish_detail'),
    
    # path per la lista degli ingredienti
    path('ingredient_list/', IngredientListView.as_view(), name='ingredient_list'),
    
    # path per operazioni CRUD sugli ingredienti
    path('new_ingredient/', IngredientCreateView.as_view(), name='ingredient_create'),
    path('edit_ingredient/<pk>', IngredientUpdateView.as_view(), name='ingredient_edit'),
    path('delete_ingredient/<pk>', IngredientDeleteView.as_view(), name='ingredient_delete'),
    path('detail_ingredient/<pk>', IngredientDetailView.as_view(), name='ingredient_detail'),
    
    # path per eseeguire una ricerca
    path ('search/', dish_search, name='dish_search'),
    path ('search_results/', SearchResultsList.as_view(), name='search_results'),
    
    path('dish/<int:dish_id>/', dish_statistics, name='dish_statistics'),


]
