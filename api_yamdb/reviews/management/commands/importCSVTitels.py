import csv

from django.core.management import BaseCommand
from reviews.models import Category, Title


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Title.objects.exists():
            print("Данные из файла уже были записаны, либо удалите "
                  "db.sqlite3 и загрузите по новой "
                  "либо оставьте всё как есть")
            return

        csv_file = "./static/data/titles.csv"
        try:
            with open(csv_file, encoding="utf-8") as open_csv:
                reader_csv = csv.reader(open_csv)
                next(reader_csv)

                for value in reader_csv:
                    category = Category.objects.get(pk=value[3])
                    Title.objects.create(
                        id=value[0],
                        name=value[1],
                        year=value[2],
                        category=category
                    )
                print("Загрузка titles.csv успешна завершена!")
        except FileNotFoundError:
            print("titles.csv не найден")
