from django.core.management.base import BaseCommand, CommandError
from stripe_api.models import Item
import random
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Generate users and items'

    def handle(self, *args, **options):
        Item.objects.all().delete()
        User.objects.all().delete()
        items = [Item(name=f"Item{index}", description=f"Desc{index}", price=random.randint(50, 1500))
                 for index in range(1, 15)]
        Item.objects.bulk_create(items)
        user = User.objects.create_superuser('user', 'lennon@thebeatles.com', 'user')
