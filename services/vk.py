import json

import requests

from groups.models import Group

key = ''


def get_data_from_vk(id):
    response = requests.post(
        url=f'https://api.vk.com/method/groups.getById?group_id={id}&access_token={key}v=5.81&fields=name&fields=members_count'
    )
    group = json.loads(response.text)
    new_group = Group.objects.create(id=int(group['response'][0]['id']),
                                     title=group['response'][0]['name'],
                                     users_count=group['response'][0]['members_count']
                                     )
    return new_group
