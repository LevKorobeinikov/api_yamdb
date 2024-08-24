from csv import DictReader
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import ProjectUser

MAPPING_DATA = {
    ProjectUser: 'users.csv',
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}
STATIC_DATA_PATH = Path(settings.BASE_DIR) / 'static/data/'


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model, data in MAPPING_DATA.items():
            csv_path = STATIC_DATA_PATH / data
            with open(csv_path, 'r', encoding='utf-8') as csvfile:
                reader = DictReader(csvfile)
                for row in reader:
                    try:
                        if model == Title:
                            row['category'] = Category.objects.get(
                                id=row['category'])
                        elif model in (Review, Comment):
                            row['author'] = ProjectUser.objects.get(
                                id=row['author'])
                        model.objects.get_or_create(**row)
                    except (ValueError, KeyError, model.DoesNotExist) as e:
                        self.stdout.write(self.style.ERROR(
                            f'Ошибка при загрузке {data}: {e}'
                        ))
                self.stdout.write(self.style.SUCCESS(
                    f'Файл {data} успешно загружен'))
