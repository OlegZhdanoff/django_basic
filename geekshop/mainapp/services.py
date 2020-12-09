import json
from django.conf import settings
import os


def load_content_from_file(file):
    with open(os.path.join(settings.BASE_DIR, 'mainapp', 'content', file), 'rt', encoding='utf-8') as content_file:
        content_json = json.load(content_file)

    return content_json
