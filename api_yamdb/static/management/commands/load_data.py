import os
import csv
from django.core.management.base import BaseCommand
from reviews.models import (
    Category, GenreTitle, Comment, Genre, Review, Title, User)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        data_dir = os.path.join('static', 'data')

        self.load_data_from_csv(
            Category, os.path.join(data_dir, 'category.csv'))
        self.load_data_from_csv(
            Comment, os.path.join(data_dir, 'comments.csv'))
        self.load_data_from_csv(
            GenreTitle, os.path.join(data_dir, 'genre_title.csv'))
        self.load_data_from_csv(Genre, os.path.join(data_dir, 'genre.csv'))
        self.load_data_from_csv(Review, os.path.join(data_dir, 'review.csv'))
        self.load_data_from_csv(Title, os.path.join(data_dir, 'titles.csv'))
        self.load_data_from_csv(User, os.path.join(data_dir, 'users.csv'))

    def load_data_from_csv(self, model, file_path):
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            model.objects.bulk_create(
                [model(**row) for row in reader]
            )
        self.stdout.write(self.style.SUCCESS(
            f'{file_path}'))
