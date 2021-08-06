from datetime import datetime, timezone

import requests
from social_core.exceptions import AuthForbidden

from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = f"https://api.vk.com/method/users.get?fields=bday,sex,about&access_token={response['access_token']}&v=5.92"
    response = requests.get(api_url)
    if response.status_code != 200:
        return
    data = response.json()['response'][0]
    print(data)
    if data['sex']:
        print(data['sex'])
        if data['sex'] == 2:
            user.userprofile.gender = UserProfile.MALE
        elif data['sex']==1:
            user.userprofile.gender = UserProfile.FEMALE
    if 'about' in data:
        user.userprofile.about_me = data['about']

    if 'bdate' in data:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    user.save()
