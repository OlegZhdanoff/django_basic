import json
from django.conf import settings
import os
from django.db import models, IntegrityError
from mainapp.models import Products, ProductCategory


def load_content_from_file(file: str) -> dict:
    with open(os.path.join(settings.BASE_DIR, 'mainapp', 'content', file), 'rt', encoding='utf-8') as content_file:
        content_json = json.load(content_file)

    return content_json


def create_new_obj(obj: dict, AnyModel: models.Model) -> dict:
    fields = AnyModel._meta.fields
    new_obj = {}
    for field in fields:
        if field.name in obj.keys():
            new_obj.setdefault(field.name, obj[field.name])
    return new_obj


def load_product_to_db(content: dict, AnyModel: models.Model, CategoriesClass: models.Model):
    for obj in content['categories']:
        try:
            CategoriesClass.objects.create(**create_new_obj(obj, CategoriesClass))
        except IntegrityError:
            continue
    for obj in content['objects_list']:
        new_obj = create_new_obj(obj, AnyModel)
        new_obj['category'] = CategoriesClass.objects.get(title=new_obj['category'])
        try:
            AnyModel.objects.create(**new_obj)
        except IntegrityError:
            continue


