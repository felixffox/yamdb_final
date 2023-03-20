import csv

from django.core.management import BaseCommand

from reviews.models import Genre


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Genre.objects.exists():
            print("Данные из файла уже были записаны, либо удалите "
                  "db.sqlite3 и загрузите по новой "
                  "либо оставьте всё как есть")
            return

        csv_file = "./static/data/genre.csv"
        try:
            with open(csv_file, encoding="utf-8") as open_csv:
                reader_csv = csv.reader(open_csv)
                next(reader_csv)

                for value in reader_csv:
                    Genre.objects.create(
                        id=value[0],
                        name=value[1],
                        slug=value[2],
                    )
                print("Загрузка genre.csv успешна завершена!")
        except FileNotFoundError:
            print("genre.csv не найден")
