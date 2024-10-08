from django.views.generic import DetailView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy 
from .models import Order, OrderDetail
from tables.models import Table
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from .reccomendation import get_reccomendations, update_cooccurrence_matrix
from django.db.models import Sum

def has_group(user):
    return user.groups.filter(name='Chef').exists()

@user_passes_test(has_group)  
def orders_statistics(request):
    # Filtra gli ordini confermati
    confirmed_orders = Order.objects.filter(status='confermato')

    # Inizializza le variabili per i calcoli
    total_cashed = 0
    total_earned = 0
    total_quantity = 0
    total_order_details = 0

    # Itera sugli ordini confermati per calcolare i totali
    for order in confirmed_orders:
        for order_detail in order.order_details.all():
            total_cashed += order_detail.total_price # Totale incassato
            total_earned += order_detail.total_earned # Totale guadagnato
            total_order_details += 1 # Totale dettagli ordini
            total_quantity += order_detail.quantity # Totale quantità piatti

    # Calcola il numero totale di ordini
    total_orders = confirmed_orders.count()
    
    # Media dettagli ordini per ordine
    
    avg_order_details_per_order = round(total_order_details / total_orders, 2) if total_orders > 0 else 0
    # Media quantità per ordine
    avg_quantity_per_order = round(total_quantity / total_orders, 2) if total_orders > 0 else 0
    
    top_3_dishes = OrderDetail.objects.values('dish__name').annotate(total_ordered=Sum('quantity')).order_by('-total_ordered')[:3]
    bottom_3_dishes = OrderDetail.objects.values('dish__name').annotate(total_ordered=Sum('quantity')).order_by('total_ordered')[:3]

    context = {
        'total_cashed': total_cashed,
        'total_earned': total_earned,
        'total_orders': total_orders,
        'total_quantity': total_quantity,
        'total_order_details': total_order_details, 
        'avg_order_details_per_order': avg_order_details_per_order,
        'avg_quantity_per_order': avg_quantity_per_order,
        'top_3_dishes': top_3_dishes,
        'bottom_3_dishes': bottom_3_dishes,
    }

    return render(request, 'orders/statistics.html', context)

class CurrentOrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/current_order.html'
    context_object_name = 'order'
    
    def get_object(self):
        # Controlla se table_id è presente nei kwargs
        table_id = self.kwargs.get('table_id')
        if table_id:
            # Ottieni il tavolo dal parametro URL
            table = get_object_or_404(Table, id=table_id)
        else:
            # Ottieni il tavolo dall'utente loggato
            table = self.request.user.table

        try:
            # Cerca un ordine associato al tavolo con stato 'da confermare'
            return Order.objects.get(table=table, status='da confermare')
        except Order.DoesNotExist:
            # Se non esiste un ordine con stato 'da confermare', ritorna None
            return None

class CurrentOrderDeleteView(LoginRequiredMixin, DeleteView):
    model = Order
    template_name = 'orders/current_order_delete.html'
    context_object_name = 'order'
    success_url = reverse_lazy('menu:menu')
    
    def get_object(self, queryset=None):
        table = get_object_or_404(Table, id=self.kwargs['table_id'])
        return get_object_or_404(Order, table=table, status='da confermare')

    #inserire un messaggio di successo col metodo post
    def post(self, request, *args, **kwargs):
        messages.success(request, "Ordine cancellato con successo!!!")
        return super().post(request, *args, **kwargs)    
     
class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = OrderDetail
    template_name = 'orders/order_detail_update.html'
    fields = ['quantity']
    context_object_name = 'order_detail'
    success_url = reverse_lazy('orders:current_order_detail')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Aggiornamento dell\'ordine avvenuto con successo!!!')
        return response

class OrderDeleteView(LoginRequiredMixin, DeleteView):
    model = OrderDetail
    template_name = 'orders/order_detail_delete.html'
    context_object_name = 'order_detail'
    success_url = reverse_lazy('orders:current_order_detail')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Eliminazione dell piatto avvenuta con successo!!!')
        return response

# @deprecated
# class ConfirmOrderView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         # Controlla se table_id è presente nei kwargs
#         table_id = self.kwargs.get('table_id')
#         if table_id:
#             # Ottieni il tavolo dal parametro URL
#             table = get_object_or_404(Table, id=table_id)
#         else:
#             # Ottieni il tavolo dall'utente loggato
#             table = request.user.table
#         order = get_object_or_404(Order, table=table, status='da confermare')
#         # Cambio lo stato dell'ordine in 'confermato'
#         order.status = 'confermato'
#         order.save()
#         return redirect('menu:menu')
    
@login_required
def confirm_order_view(request, table_id=None):
    if table_id:
        table = get_object_or_404(Table, id=table_id)
    else:
        table = request.user.table

    order = get_object_or_404(Order, table=table, status='da confermare')
    
    if not order.order_details.exists():
        order.delete()
        messages.warning(request, "L'ordine è vuoto, quindi è stato eliminato, nice try ;-)")
        return redirect('tables:table_detail', pk=table.id)

    order.status = 'confermato'
    order.save()
    
    update_cooccurrence_matrix(order)
    
    return redirect('orders:order_recommendations', pk=order.pk)

# @deprecated
# class ConcludeEveningView(LoginRequiredMixin,  View):
#     def post(self, request, *args, **kwargs):
#         # Controlla se table_id è presente nei kwargs
#         table_id = self.kwargs.get('table_id')
#         if table_id:
#             # Ottieni il tavolo dal parametro URL
#             table = get_object_or_404(Table, id=table_id)
#         else:
#             # Ottieni il tavolo dall'utente loggato
#             table = request.user.table
            
#         # Filtra gli ordini associati al tavolo corrente
#         orders = Order.objects.filter(table=table)
#         for order in orders:
#             # Verifica se ci sono ordini non pronti
#             # print(order)
#             # print (order.order_details.all())
#             # print(order.order_details.all().filter(status='In attesa'or 'In preparazione'))
#             if( order.order_details.all().filter(status='In attesa' )):
#                 # Ci sono ordini non pronti, restituisci un messaggio di avviso
#                 print("Mascalzone")
#                 messages.error(request, "Gli ordini devono essere tutti pronti per poter concludere la serata.")
#                 return redirect('tables:table_detail' , pk=table.id)
                
#         # Calcola il totale complessivo degli ordini
#         total_price = sum(order.total_price for order in orders)
#         # Dissocia gli ordini dal tavolo corrente
#         orders.update(table=None)
#         # Reindirizza alla pagina di conferma serata con il totale complessivo
#         return render(request, 'orders/conclude_evening.html', {'total_price': total_price})
    
@login_required
def conclude_evening_view(request, table_id=None):
    if request.method == 'POST':
        if table_id:
            # Ottieni il tavolo dal parametro URL
            table = get_object_or_404(Table, id=table_id)
        else:
            # Ottieni il tavolo dall'utente loggato
            table = request.user.table
            
        # Filtra gli ordini associati al tavolo corrente
        orders = Order.objects.filter(table=table)
        for order in orders:
            # Verifica se ci sono ordini non pronti
            if order.order_details.all().filter(status='In attesa') or order.order_details.all().filter(status='In preparazione') :
                print("Mascalzone")
                # Ci sono ordini non pronti, restituisci un messaggio di avviso
                messages.error(request, "Gli ordini devono essere tutti pronti per poter concludere la serata.")
                return redirect('tables:table_detail', pk=table.id)
                
        # Calcola il totale complessivo degli ordini
        total_price = sum(order.total_price for order in orders)
        # Dissocia gli ordini dal tavolo corrente
        orders.update(table=None)
        # Reindirizza alla pagina di conferma serata con il totale complessivo
        return render(request, 'orders/conclude_evening.html', {'total_price': total_price})
    else:
        # Se il metodo non è POST, reindirizza alla homepage o mostra un messaggio di errore
        messages.error(request, "Richiesta non valida.")
        return redirect('home')

# DEPRECATO
# class UpdateOrderDetailStatus(GroupRequiredMixin, View):
#     group_required = 'Chef'
#     def post(self, request, *args, **kwargs):
#         order_detail_id=self.kwargs['order_detail_id']
#         order_detail=get_object_or_404(OrderDetail, id=order_detail_id)
#         order_detail.move_to_next_status
#         order_detail.save()
#         return redirect('tables:table_detail', order_detail.order.table.id)

from django.http import JsonResponse

@user_passes_test(has_group)  
def update_order_detail_status(request, order_detail_id):
    if request.method == 'POST':
        order_detail = get_object_or_404(OrderDetail, id=order_detail_id)
        order_detail.move_to_next_status 
        order_detail.save()
        return JsonResponse({'status': order_detail.status}, status=200)
    else:
        return JsonResponse({'status': order_detail.status}, status=200)
# @user_passes_test(has_group)  
# def update_order_detail_status(request, order_detail_id):
#     if request.method == 'POST':
#         order_detail = get_object_or_404(OrderDetail, id=order_detail_id)
#         order_detail.move_to_next_status 
#         order_detail.save()
#         return redirect('tables:table_detail', order_detail.order.table.id)
#     else:
#         # Se il metodo non è POST, mostra un messaggio di errore o reindirizza
#         print("Mascalzone")
#         messages.error(request, "Richiesta non valida.")
#         return redirect('home')


@login_required
def order_recommendations_view(request, pk):
    # Ottengo l'ordine corrente
    order = get_object_or_404(Order, pk=pk)
    # Ottengo una lista di piatti raccomandati
    recommended_dishes = get_reccomendations(order)
    # Li mando al template che li mostrerà all'utente
    return render(request, 'orders/order_recommendations.html', {
        'recommended_dishes': recommended_dishes,
    })