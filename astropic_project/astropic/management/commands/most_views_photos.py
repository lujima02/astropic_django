from django.core.management.base import BaseCommand
from astropic.models import Photo

class Command(BaseCommand):

    def handle(self, *args, **options):
        most_views = Photo.objects.order_by('-visits')[:10]

        if most_views:
            self.stdout.write(self.style.SUCCESS('Fotos más vistas:'))
            for photo in most_views:
                self.stdout.write(f'- {photo.title}  ({photo.visits} visitas)')
        else:
            self.stdout.write(self.style.WARNING('No hay fotos disponibles.'))