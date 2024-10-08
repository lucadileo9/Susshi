import os
import shutil
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Carica immagini per i piatti nella cartella dish_images'

    def add_arguments(self, parser):
        parser.add_argument('images_folder', type=str, help='Il percorso della cartella che contiene le immagini')

    def handle(self, *args, **kwargs):
        images_folder = kwargs['images_folder']
        destination_folder = os.path.join('media', 'dish_images')

        # Controllo se la cartella delle immagini esiste
        if not os.path.isdir(images_folder):
            self.stdout.write(self.style.ERROR(f'{images_folder} non è una directory valida'))
            return

        # Controllo se la cartella di destinazione esiste, altrimenti la creo
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Copio le immagini dalla cartella sorgente a quella di destinazione
        for filename in os.listdir(images_folder):
            source_path = os.path.join(images_folder, filename)
            destination_path = os.path.join(destination_folder, filename)
            shutil.copy(source_path, destination_path)
            self.stdout.write(self.style.SUCCESS(f'Immagine {filename} caricata con successo'))
