from braces.views import GroupRequiredMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from orders.models import Order
from .models import Table
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserIsTableOwnerMixin, TableUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect



class TableListView(LoginRequiredMixin, ListView):
    model = Table
    template_name = 'tables/table_list.html'
    context_object_name = 'tables'

class TableDetailView(LoginRequiredMixin, UserIsTableOwnerMixin, DetailView):
    model = Table
    template_name = 'tables/table_detail.html'
    context_object_name = 'table'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # recupera tutti gli ordini per il tavolo corrente
        orders = Order.objects.filter(table=self.object)
        context['orders'] = orders
        
        # controlla se ci sono ordini in sospeso per il tavolo corrente
        context['has_pending_order'] = orders.filter(status="da confermare").exists()
        
        # calcola il totale degli ordini, ma solo quelli confermati
        context['total_price'] = sum(order.total_price for order in orders.filter(status="confermato"))
        
        return context
    
class TableUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ["Chef"]
    model = Table
    form_class = TableUpdateForm
    template_name = 'tables/table_update.html'
    success_url = reverse_lazy('tables:table_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Aggiornamento del tavolo avvenuta con successo!!!')
        return response    
    
    # Questo metodo serve per passare l'istanza del tavolo al form
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['table_instance'] = self.get_object()
        return kwargs


class TableDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ["Chef"]
    model = Table
    template_name = 'tables/table_delete.html'
    success_url = reverse_lazy('tables:table_list')
    
    def post (self, request, *args, **kwargs):
        messages.success(self.request, 'Eliminazione del tavolo avvenuta con successo!!!')
        return super().post(request, *args, **kwargs)

def has_group(user):
    return user.groups.filter(name='Tavolo').exists()

@user_passes_test(has_group)  
def user_table_redirect(request):
    # Ottieni il tavolo associato all'utente loggato
    table = get_object_or_404(Table, user=request.user)
    # Reindirizza alla view del dettaglio del tavolo
    return redirect('tables:table_detail', pk=table.pk)
