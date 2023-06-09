import csv
import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Comment, Genre, Review, Title, User

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    format='%(asctime)s, %(levelname)s, %(name)s, %(message)s',
    filemode='w',
    encoding='utf-8'
)

FOREIGN_KEY_FIELDS = ('category', 'author')

FILES = {
    User: 'users.csv',
    Genre: 'genre.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Review: 'review.csv',
    Comment: 'comments.csv'
}


def csv_serializer(csv_data, model):
    objs = []
    for row in csv_data:
        for field in FOREIGN_KEY_FIELDS:
            if field in row:
                row[f'{field}_id'] = row[field]
                del row[field]
        objs.append(model(**row))
    model.objects.bulk_create(objs)


class Command(BaseCommand):
    help = 'Загружает данные из csv файла в бд'

    def handle(self, *args, **kwargs):
        for model in FILES:
            try:
                with open(
                    os.path.join
                    (settings.BASE_DIR, 'static/data/', + FILES[model]),
                    newline='',
                    encoding='utf8'
                ) as csv_file:
                    csv_serializer(csv.DictReader(csv_file), model)
            except Exception as error:
                CommandError(error)
        logging.info('Данные успешно загрузились в бд')
