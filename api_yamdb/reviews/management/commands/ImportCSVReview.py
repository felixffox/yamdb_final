import csv

from django.core.management import BaseCommand

from reviews.models import Review
from reviews.models import Title
from reviews.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Review.objects.exists():
            print("Данные из файла уже были записаны, либо удалите "
                  "db.sqlite3 и загрузите по новой "
                  "либо оставьте всё как есть")
            return

        csv_file = "./static/data/review.csv"
        try:
            with open(csv_file, encoding="utf-8") as open_csv:
                reader_csv = csv.reader(open_csv)
                next(reader_csv)

                for value in reader_csv:
                    title = Title.objects.get(pk=value[1])
                    author = User.objects.get(pk=value[3])
                    Review.objects.create(
                        id=value[0],
                        title=title,
                        text=value[2],
                        author=author,
                        score=value[4],
                        pub_date=value[5]
                    )
                print("Загрузка review.csv успешна завершена!")
        except FileNotFoundError:
            print("review.csv не найден")
