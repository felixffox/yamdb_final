from csv import reader

from django.core.management import BaseCommand
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        if User.objects.exists():
            print("Данные из файла уже были записаны, либо удалите "
                  "db.sqlite3 и загрузите по новой "
                  "либо оставьте всё как есть")
            return

        csv_file = "./static/data/users.csv"
        try:
            with open(csv_file, encoding="utf-8") as open_csv:
                reader_csv = reader(open_csv)
                next(reader_csv)

                for value in reader_csv:
                    User.objects.create(
                        id=value[0],
                        username=value[1],
                        email=value[2],
                        role=value[3],
                        bio=value[4],
                        first_name=value[5],
                        last_name=value[6]
                    )
                print("Загрузка users.csv успешна завершена!")
        except FileNotFoundError:
            print("users.csv не найден")
