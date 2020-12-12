import json
from django.conf import settings
import os
from mainapp.models import Products, ProductCategory


def load_content_from_file(file: str) -> dict:
    with open(os.path.join(settings.BASE_DIR, 'mainapp', 'content', file), 'rt', encoding='utf-8') as content_file:
        content_json = json.load(content_file)

    return content_json


def load_product_to_db(content: dict, AnyClass):
    fields = AnyClass._meta.fields

    for obj in content['objects_list']:
        new_obj = {}
        for field in fields:
            if field.name in obj.keys():
                print(obj[field.name])
                new_obj.setdefault(field.name, obj[field.name])
        AnyClass.objects.create(**new_obj)
            # if obj[field.name]:
                # product = Products()



