# Qui dovrei inserire la logica per raccomandare un piatto
from itertools import combinations
from menu.models import Dish
from .models import SimilarityMatrix, CoOccurrenceMatrix, Order



def jaccard_similarity(dish1, dish2):
    # Ottengo gli ingredienti dei due piatti (ingredients è un campo ManyToManyField, da quella lista di ingredienti 
    # values_list mi restituisce una lista di id degli ingredienti)
    ingredients1 = set(dish1.ingredients.values_list('id', flat=True))
    ingredients2 = set(dish2.ingredients.values_list('id', flat=True))
    intersection = ingredients1.intersection(ingredients2)
    union = ingredients1.union(ingredients2)
    return len(intersection) / len(union) if union else 0

def create_similarity_matrix():
    # Cancella la matrice esistente
    SimilarityMatrix.objects.all().delete()

    # prendo tutti i piatti dal database
    dishes = Dish.objects.all()
    
    # per ogni coppia di piatti calcolo il punteggio di similarità e lo salvo nel database
    for dish1, dish2 in combinations(dishes, 2):
        similarity_score = jaccard_similarity(dish1, dish2)
        ## inserisco la similarità tra dish1 e dish2
        SimilarityMatrix.objects.update_or_create(
            dish1=dish1, dish2=dish2, defaults={'similarity': similarity_score}
        )
        # che sarà analoga alla similarità tra dish2 e dish1
        SimilarityMatrix.objects.update_or_create(
            dish1=dish2, dish2=dish1, defaults={'similarity': similarity_score}
        )

def get_recommendations_ingredients_based(order):
    # Ottieni i piatti ordinati
    ordered_dishes = order.order_details.values_list('dish', flat=True)
    similarity_scores = {}

    # Calcola i punteggi di similarità di ciascun piatto, basandomi sui piatti presenti nell'ordine
    for dish_id in ordered_dishes:
    # ottengo le righe della matrice, nella forma piatto_corrente piatto_simile punteggio_similarità
        similar_dishes = SimilarityMatrix.objects.filter(dish1_id=dish_id)
        # per ogni riga estratta dalla matrice
        for similar_dish in similar_dishes:
            # se l'id del secondo piatto (piatto_simile) non è presente nel dizionario, lo aggiungo
            if similar_dish.dish2_id not in similarity_scores:
                similarity_scores[similar_dish.dish2_id] = 0
            # incremento il punteggio di similarità del piatto simile
            similarity_scores[similar_dish.dish2_id] += similar_dish.similarity

    # Rimuovi i piatti già presenti nell'ordine dalle raccomandazioni
    for dish_id in ordered_dishes:
        if dish_id in similarity_scores:
            del similarity_scores[dish_id]
    
    print(similarity_scores)      
    # Ordina la lista di id usando come chiave (key) il punteggio di similarità (similarity_scores.get). Prendono i primi 3 piatti
    recommended_dish_ids = sorted(similarity_scores, key=similarity_scores.get, reverse=True)[:3]
    recommended_dishes = Dish.objects.filter(id__in=recommended_dish_ids)
    
    return recommended_dishes


def populate_initial_cooccurrence_matrix():
    # Ottieni tutti gli ordini confermati
    orders = Order.objects.filter(status='confermato')
    
    # Cancella la matrice esistente
    CoOccurrenceMatrix.objects.all().delete()

    # Calcola la co-occurrence
    for order in orders:
        # Ottieni i piatti ordinati in questo ordine
        ordered_dishes = order.order_details.values_list('dish', flat=True)
        for dish1, dish2 in combinations(ordered_dishes, 2):
            # Contiamo ogni coppia una sola volta indipendentemente dall'ordine
            dish1, dish2 = sorted([dish1, dish2])
            obj, created = CoOccurrenceMatrix.objects.get_or_create(dish1_id=dish1, dish2_id=dish2)
            obj.count += 1
            obj.save()
            

def update_cooccurrence_matrix(order):
    # Ottieni i piatti ordinati in questo ordine
    ordered_dishes = order.order_details.values_list('dish', flat=True)
    for dish1, dish2 in combinations(ordered_dishes, 2):
        dish1, dish2 = sorted([dish1, dish2])
        obj, created = CoOccurrenceMatrix.objects.get_or_create(dish1_id=dish1, dish2_id=dish2)
        obj.count += 1
        obj.save()
        
        
def get_recommendations_orders_based(order):
    # Ottieni i piatti ordinati
    ordered_dishes = order.order_details.values_list('dish', flat=True)
    cooccurrence_scores = {}

    for dish_id in ordered_dishes:
        # Ottieni tutti i piatti che sono stati ordinati con questo piatto
        similar_dishes = CoOccurrenceMatrix.objects.filter(dish1_id=dish_id) | CoOccurrenceMatrix.objects.filter(dish2_id=dish_id)
        for similar_dish in similar_dishes:
            other_dish_id = similar_dish.dish2_id if similar_dish.dish1_id == dish_id else similar_dish.dish1_id
            if other_dish_id not in cooccurrence_scores:
                cooccurrence_scores[other_dish_id] = 0
            cooccurrence_scores[other_dish_id] += similar_dish.count

    # Rimuovi i piatti già presenti nell'ordine dalle raccomandazioni
    for dish_id in ordered_dishes:
        if dish_id in cooccurrence_scores:
            del cooccurrence_scores[dish_id]

    # Ordina i piatti per co-occurrence count e prendi i primi 3
    recommended_dish_ids = sorted(cooccurrence_scores, key=cooccurrence_scores.get, reverse=True)[:3]
    recommended_dishes = Dish.objects.filter(id__in=recommended_dish_ids)

    return recommended_dishes

def get_reccomendations(order):
    first_recommendation = get_recommendations_ingredients_based(order)
    second_recommendation = get_recommendations_orders_based(order)
    return first_recommendation.union(second_recommendation)
