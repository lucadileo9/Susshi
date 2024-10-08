from menu.models import Dish
from menu.models import Ingredient
# Questo file in realtà al momento non viene utilizzato, ma è stato creato per inizializzare il database con i piatti e gli ingredienti
def erase_dish_db():
    print("Erasing dish database")
    Dish.objects.all().delete()

def erase_ingredient_db():
    print("Erasing ingredient database")
    Ingredient.objects.all().delete()

def init_ingredient_db():
    print("Initializing ingredient  database")
    Ingredient.objects.create(name="Riso")
    Ingredient.objects.create(name="Salmone")
    Ingredient.objects.create(name="Tonno")
    Ingredient.objects.create(name="Avocado")
    Ingredient.objects.create(name="Cetriolo")
    Ingredient.objects.create(name="Alghe")
    Ingredient.objects.create(name="Wasabi")
    Ingredient.objects.create(name="Zenzero")
    Ingredient.objects.create(name="Branzino")
    Ingredient.objects.create(name="Verdure")
    Ingredient.objects.create(name="Farina")
    Ingredient.objects.create(name="Uova")
    Ingredient.objects.create(name="Olio")
    Ingredient.objects.create(name="Salsa di soia")
    Ingredient.objects.create(name="Salsa teriyaki")
    Ingredient.objects.create(name="Carne")
    Ingredient.objects.create(name="Fagioli")
    Ingredient.objects.create(name="Sale")
    Ingredient.objects.create(name="Miso")
    Ingredient.objects.create(name="Tofu")
    Ingredient.objects.create(name="Cipollotto")
    Ingredient.objects.create(name="Manzo")
    Ingredient.objects.create(name="Pollo")
    Ingredient.objects.create(name="Sake")
    Ingredient.objects.create(name="Soba")
    
def init_dish_db():
    print("Initializing dish database")
    rice, _ = Ingredient.objects.get_or_create(name='Riso')
    salmon, _ = Ingredient.objects.get_or_create(name='Salmone')
    tuna, _ = Ingredient.objects.get_or_create(name='Tonno')
    avocado, _ = Ingredient.objects.get_or_create(name='Avocado')
    cucumber, _ = Ingredient.objects.get_or_create(name='Cetriolo')
    seaweed, _ = Ingredient.objects.get_or_create(name='Alghe')
    wasabi, _ = Ingredient.objects.get_or_create(name='Wasabi')
    ginger, _ = Ingredient.objects.get_or_create(name='Zenzero')

    # Creare il piatto e aggiungere gli ingredienti associati
    sushi_misto = Dish.objects.create(
        name="Sushi Misto",
        description="Assortimento di sushi",
        price=10.00,
        profit=5.00
    )
    sushi_misto.ingredients.add(rice, salmon, tuna, avocado, cucumber, seaweed, wasabi, ginger)

    # Dish.objects.create(name="Sushi Misto", description="Assortimento di sushi", price=10.00, profit=5.00, ingredients="Riso, Salmone, Tonno, Avocado, Cetriolo, Alghe, Wasabi, Zenzero")
    # Dish.objects.create(name="Sashimi", description="Assortimento di sashimi", price=15.00, profit=7.50, ingredients="Salmone, Tonno, Branzino, Wasabi, Zenzero")
    # Dish.objects.create(name="Tempura", description="Tempura di verdure", price=8.00, profit=4.00, ingredients="Verdure, Farina, Uova, Olio, Salsa di soia")
    # Dish.objects.create(name="Uramaki", description="Uramaki con salmone", price=12.00, profit=6.00, ingredients="Riso, Salmone, Avocado, Cetriolo, Alghe, Wasabi, Zenzero")
    # Dish.objects.create(name="Nigiri", description="Nigiri assortiti", price=10.00, profit=5.00, ingredients="Riso, Salmone, Tonno, Branzino, Wasabi, Zenzero")
    # Dish.objects.create(name="Tartare", description="Tartare di tonno", price=18.00, profit=9.00, ingredients="Tonno, Avocado, Cetriolo, Alghe, Wasabi, Zenzero")
    # Dish.objects.create(name="Gyoza", description="Gyoza di carne", price=8.00, profit=4.00, ingredients="Carne, Verdure, Farina, Olio, Salsa di soia")
    # Dish.objects.create(name="Edamame", description="Edamame al sale", price=5.00, profit=2.50, ingredients="Fagioli, Sale, Olio")
    # Dish.objects.create(name="Miso", description="Zuppa di miso", price=4.00, profit=2.00, ingredients="Miso, Alghe, Tofu, Cipollotto")
    # Dish.objects.create(name="Yakitori", description="Yakitori di pollo", price=8.00, profit=4.00, ingredients="Pollo, Salsa teriyaki, Verdure")
    # Dish.objects.create(name="Tataki", description="Tataki di manzo", price=20.00, profit=10.00, ingredients="Manzo, Salsa teriyaki, Verdure")
    # Dish.objects.create(name="Tofu", description="Tofu fritto", price=6.00, profit=3.00, ingredients="Tofu, Farina, Olio, Salsa di soia")
    # Dish.objects.create(name="Sake", description="Sake alla griglia", price=12.00, profit=6.00, ingredients="Salmone, Salsa teriyaki, Verdure")
    # Dish.objects.create(name="Soba", description="Soba con verdure", price=10.00, profit=5.00, ingredients="Soba, Verdure, Salsa di soia")
    
    