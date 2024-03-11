import csv

from django.core.management import BaseCommand
from main.models import Collect, Payment
from users.models import User

CSVMODEL = {
    User: 'users.csv',
    Collect: 'collect.csv',
    Payment: 'genre.csv',
}


class Command(BaseCommand):
    help = "Loads data from csv"

    def handle(self, *args, **options):
        self.stdout.write("Loading data")
        for model, filename in CSVMODEL.items():
            model.objects.all().delete()
            with open(f'static/data/{filename}', encoding='utf-8') as opencvs:
                dictreadercvs = csv.DictReader(opencvs)
                bulk_list = []
                for row in dictreadercvs:
                    bulk_list.append(model(**row))
            model.objects.bulk_create(bulk_list)
        print("Loading database is complete")
