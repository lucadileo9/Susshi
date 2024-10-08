from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import *
from orders.models import Order
from tables.models import Table
from .forms import *
from orders.forms import AddDishForm
from django.urls import reverse_lazy
from braces.views import GroupRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from orders.models import OrderDetail, Order
from django.contrib.auth.decorators import user_passes_test
from orders.reccomendation import create_similarity_matrix

def has_group(user):
    return user.groups.filter(name='Chef').exists()

@user_passes_test(has_group)  
def dish_statistics(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    # QuerySet che contiene tutti i OrderDetail per il piatto specifico.
    order_details = OrderDetail.objects.filter(dish=dish)

    total_cashed = 0
    total_earned = 0
    total_quantity = 0
    
    for detail in order_details:
        total_cashed += detail.total_price
        total_earned += detail.quantity * detail.dish.profit
        total_quantity += detail.quantity


    # .values('order'): Estrae i valori del campo order da ciascun OrderDetail nel QuerySet., .distinct(): Filtra i risultati per mantenere solo i valori distinti. 
    #  count(): Conta il numero di risultati distinti.
    total_orders = order_details.values('order').distinct().count() # Numero di ordini distinti in cui il piatto è presente.
    
    context = {
        'dish': dish,
        'total_cashed': total_cashed, # Totale incassato per il piatto
        'total_earned': total_earned,
        'total_orders': total_orders,
        'total_quantity': total_quantity,
    }

    return render(request, 'menu/dish_statistics.html', context)

def dish_search(request):
    if request.method == "POST":
        form = DishSearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            ingredients = form.cleaned_data.get('ingredients')
            max_price = form.cleaned_data.get('max_price')
            ingredient_ids = ','.join(str(ingredient.id) for ingredient in ingredients)
            query_params = {
                'name': name or "",
                'ingredients': ingredient_ids or "",
                'max_price': max_price or "",
            }
            print(query_params)
            query_string = '&'.join([f'{key}={value}' for key, value in query_params.items() if value])
            return redirect(f"{reverse('menu:search_results')}?{query_string}")

    else:
        form = DishSearchForm()  
    return render(request,template_name="menu/search_dish.html",context={"form":form})

class SearchResultsList(ListView):
    model = Dish
    template_name = "menu/search_results.html"
    
    def get_queryset(self):
        name = self.request.GET.get('name')
        ingredients = self.request.GET.get("ingredients")
        max_price = self.request.GET.get("max_price")

        if (name or ingredients or max_price):
            dishes= Dish.objects.all()
            if name:
                dishes = dishes & Dish.objects.filter(name__icontains=name) 
            if ingredients:
                ingredient_ids = [int(id) for id in ingredients.split(',') if id]
                for ingredient_id in ingredient_ids:
                    dishes = dishes & Dish.objects.filter(ingredients=ingredient_id)        
            if max_price:
                dishes = dishes & Dish.objects.filter(price__lte=max_price)
            print(dishes)
            return dishes
        else:
            return Dish.objects.none()
   
# View per la lista dei piatti
class MenuListView(ListView):
    model = Dish
    template_name = 'menu/menu.html'
    context_object_name = 'menu'
    #restituire i piatti in ordine alfabetico
    def get_queryset(self):
        return Dish.objects.all().order_by('name')
    
 
# Views per i piatti   
class DishCreateView(GroupRequiredMixin, CreateView):
    group_required = ["Chef"]
    model = Dish
    template_name = 'menu/dish_create.html'
    form_class = DishForm
    success_url = reverse_lazy('menu:menu')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Creazione del piatto avvenuta con successo!!!')
        create_similarity_matrix()
        return response

     
class DishUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ["Chef"]
    model = Dish
    template_name = 'menu/dish_update.html'
    form_class = DishForm
    success_url = reverse_lazy('menu:menu')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Aggiornamento del piatto avvenuto con successo!!!')
        create_similarity_matrix()
        return response
       
class DishDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ["Chef"]
    model = Dish
    template_name = 'menu/dish_delete.html'
    success_url = reverse_lazy('menu:menu')
    
    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Eliminazione del piatto avvenuta con successo!!!")
        create_similarity_matrix()
        return super().delete(request, *args, **kwargs)


class DishDetailView(DetailView):
    model = Dish
    template_name = 'menu/dish_detail.html'
    context_object_name = 'dish'
    # Essendo un detail view non ha una form per aggiungere un piatto all'ordine, quindi bisogna creare un form apposito e aggiungerlo
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddDishForm()
        return context

    # Tutto questo casino serbe per aggiungere un piatto all'ordine
    def post(self, request, *args, **kwargs):
        # Recupera il piatto che l'utente sta visualizzando.
        self.object = self.get_object()

        # Crea un'istanza del form `AddDishForm` con i dati POST.
        form = AddDishForm(request.POST)

        if form.is_valid():
            # Recupera l'utente corrente e il tavolo associato.
            user = request.user
            table = get_object_or_404(Table, user=user)
            
            # Cerca un ordine esistente per il tavolo con lo stato 'da confermare' o ne crea uno nuovo se non esiste.
            order, created= Order.objects.get_or_create(table=table, status='da confermare')
            # Creo l'order_detail con la quantità presa dal form, il piatto ottenuto precedentemente e l'ordine ottenuto precedentemente
            
            order_detail = form.save(commit=False)
            order_detail.order = order
            order_detail.dish = self.object
            
            # Salvataggio
            order_detail.save()
            # Aggiungi un messaggio di successo
            messages.success(request, 'Piatto aggiunto all\'ordine con successo!')

            # Reindirizza l'utente alla vista del dettaglio dell'ordine appena creato o aggiornato.        
            return redirect('menu:menu')

        # se il form non è valido, renderizza di nuovo la pagina con il form
        return self.render_to_response(self.get_context_data(form=form))
    
# Views per gli ingredienti
class IngredientListView(ListView):
    model = Ingredient
    template_name = 'menu/ingredient_list.html'
    context_object_name = 'ingredients'
 
class IngredientCreateView(GroupRequiredMixin, CreateView):
    group_required = ["Chef"]
    model = Ingredient
    template_name = 'menu/ingredient_create.html'
    fields = '__all__'
    success_url = reverse_lazy('menu:ingredient_list')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Creazione dell\'ingrediente avvenuta con successo!!!')
        return response

class IngredientUpdateView(GroupRequiredMixin, UpdateView):
    group_required = ["Chef"]
    model = Ingredient
    template_name = 'menu/ingredient_update.html'
    fields = '__all__'
    success_url = reverse_lazy('menu:ingredient_list')
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Aggiornamento dell\'ingrediente avvenuto con successo!!!')
        return response

class IngredientDeleteView(GroupRequiredMixin, DeleteView):
    group_required = ["Chef"]
    model = Ingredient
    template_name = 'menu/ingredient_delete.html'
    success_url = reverse_lazy('menu:ingredient_list')
    def post(self, request, *args, **kwargs):
        messages.success(self.request, "Eliminazione dell'ingrediente avvenuta con successo!!!")
        return super().delete(request, *args, **kwargs)

class IngredientDetailView(DetailView):
    model = Ingredient
    template_name = 'menu/ingredient_detail.html'
    context_object_name = 'ingredient'