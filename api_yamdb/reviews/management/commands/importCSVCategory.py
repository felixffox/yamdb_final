import csv

from django.core.management import BaseCommand
from reviews.models import Category


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Category.objects.exists():
            print("Данные из файла уже были записаны, либо удалите "
                  "db.sqlite3 и загрузите по новой "
                  "либо оставьте всё как есть")
            return

        csv_file = "./static/data/category.csv"
        try:
            with open(csv_file, encoding="utf-8") as open_csv:
                reader_csv = csv.reader(open_csv)
                next(reader_csv)

                for value in reader_csv:
                    Category.objects.create(
                        id=value[0],
                        name=value[1],
                        slug=value[2],
                    )
                print("Загрузка category.csv успешна завершена!")
        except FileNotFoundError:
            print("category.csv не найден")
