import random
import time
from _decimal import Decimal

from django.core.management.base import BaseCommand

from api.models import Stock


class Command(BaseCommand):
    help = 'Start randomising the stock price'

    def handle(self, *args, **options):
        while True:
            stocks = Stock.objects.all()
            for stock in stocks:
                change_direction = random.choice([-1, 0, 1])
                change_amount = Decimal(random.uniform(0, 1))
                new_price = stock.price + change_direction * change_amount

                # Update the stock with the new price
                stock.price = new_price
                stock.save()

            # Wait for 5 seconds before the next update
            time.sleep(5)

