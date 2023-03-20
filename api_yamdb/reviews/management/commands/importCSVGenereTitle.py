import csv

from django.core.management import BaseCommand
from reviews.models import Genre, GenreTitle, Title


class Command(BaseCommand):
    def handle(self, *args, **options):
        if GenreTitle.objects.exists():
            print("Данные из файла уже были записаны, либо удалите "
                  "db.sqlite3 и загрузите по новой "
                  "либо оставьте всё как есть")
            return

        csv_file = "./static/data/genre_title.csv"
        try:
            with open(csv_file, encoding="utf-8") as open_csv:
                reader_csv = csv.reader(open_csv)
                next(reader_csv)

                for value in reader_csv:
                    title = Title.objects.get(pk=value[1])
                    genre = Genre.objects.get(pk=value[2])
                    GenreTitle.objects.create(
                        id=value[0],
                        title=title,
                        genre=genre,

                    )
                print("Загрузка genre_title.csv успешна завершена!")
        except FileNotFoundError:
            print("genre_title.csv не найден")
