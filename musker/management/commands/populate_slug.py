from django.core.management.base import BaseCommand
from musker.models import Meep


class Command(BaseCommand):
    help = 'Create slug for meeps without one.'

    def handle(self, *args, **options):
        meeps = Meep.objects.filter(slug='2')

        print(f'Updating a total of {len(meeps)} meeps.')

        [Meep.objects.create(slug=meep) for meep in meeps]
