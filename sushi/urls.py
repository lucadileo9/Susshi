"""
URL configuration for sushi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import *
# from .initcmds import erase_dish_db, erase_ingredient_db, init_ingredient_db, init_dish_db
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from orders.reccomendation import create_similarity_matrix, populate_initial_cooccurrence_matrix


urlpatterns = [
    path('', include('restaurant.urls')),  
    
    path('admin/', admin.site.urls, name='admin'),
    
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", TableCreateView.as_view(), name="register"),
    path("register_chef/",ChefCreateView.as_view(), name="register_chef"),
    
    path('menu/', include('menu.urls')),

    path('tables/', include('tables.urls')),
    
    path('orders/', include('orders.urls')),
    
]
create_similarity_matrix()
populate_initial_cooccurrence_matrix()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
