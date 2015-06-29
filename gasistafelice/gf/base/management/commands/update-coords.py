from django.core.management.base import BaseCommand, CommandError
from gf.base.models import Place

class Command(BaseCommand):
    help = 'Update coords from OSM for Place entries in db'
    
    def handle(self, *args, **options):
        self.stdout.write("Updating coords...")
        for place in Place.objects.all():
            place.update_coords()
            place.save()
        self.stdout.write("Done!")
