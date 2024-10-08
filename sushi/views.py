from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import *
from django.contrib.auth.mixins import PermissionRequiredMixin
from braces.views import GroupRequiredMixin
from django.contrib import messages

class ChefCreateView(PermissionRequiredMixin,CreateView):
    permission_required = "is_staff"
    form_class = ChefCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("restaurant:homepage")

class TableCreateView(GroupRequiredMixin, CreateView):
    group_required = ["Chef"]
    form_class = TableCreationForm
    template_name = "user_create.html"
    success_url = reverse_lazy("tables:table_list")
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Creazione del tavolo avvenuta con successo!!!')
        return response
    
