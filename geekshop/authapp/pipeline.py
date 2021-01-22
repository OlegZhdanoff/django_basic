from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        print('not VK ', user)
        return
    # api_url = f'https://api.vk.com/methods/users.get/fields=bdate,about,sex&access_token=' \
    #           f'{response["access_token"]}&v="5.92"'

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))
    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if 'sex' in data:
        if data['sex'] == 2:
            print('user sex is MALE')
            user.shopuserprofile.gender = ShopUserProfile.MALE
        elif data['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
    if data['about']:
        user.shopuserprofile.aboutMe = data['about']
    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
        age = timezone.now().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.birthday = bdate
    if response['email']:
        user.email = response['email']
    if response['user_photo']:
        user.avatar = response['user_photo']
    user.save()
    print(user, response)
#     сделать вытягивание аватарки и подстановки в профиль
