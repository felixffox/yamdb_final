import csv

from django.core.management import BaseCommand

from reviews.models import Comment
from reviews.models import Review
from reviews.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if Comment.objects.exists():
            print("Данные из файла уже были записаны, либо удалите "
                  "db.sqlite3 и загрузите по новой "
                  "либо оставьте всё как есть")
            return

        csv_file = "./static/data/comments.csv"
        try:
            with open(csv_file, encoding="utf-8") as open_csv:
                reader_csv = csv.reader(open_csv)
                next(reader_csv)

                for value in reader_csv:
                    review = Review.objects.get(pk=value[1])
                    author = User.objects.get(pk=value[3])
                    Comment.objects.create(
                        id=value[0],
                        rewiew=review,
                        text=value[2],
                        author=author,
                        pub_date=value[4]
                    )
                print("Загрузка comments.csv успешна завершена!")
        except FileNotFoundError:
            print("comments.csv не найден")
