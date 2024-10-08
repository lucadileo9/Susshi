from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Dish

# Questo signal si occupa di eliminare l'immagine di un piatto quando questo viene eliminato
@receiver(post_delete, sender=Dish)
def delete_dish_image_on_delete(sender, instance, **kwargs):
    if instance.image: # se il piatto ha un'immagine
        instance.image.delete(save=False) # elimina l'immagine
        # save=False serve per evitare un loop infinito, cioè per non risalvare il model

# Questo signal si occupa di eliminare l'immagine di un piatto quando questa viene modificato
@receiver(pre_save, sender=Dish)
def delete_dish_image_on_change(sender, instance, **kwargs):
    if not instance.pk: # se il piatto non esiste ancora
        return False # non fare nulla

    try:
        old_image = Dish.objects.get(pk=instance.pk).image # cerca l'immagine del piatto
    except Dish.DoesNotExist:
        return False

    new_image = instance.image # prendi la nuova immagine
    if old_image and old_image != new_image: # se l'immagine vecchia esiste e non è uguale a quella nuova
        old_image.delete(save=False) # elimina l'immagine vecchia
