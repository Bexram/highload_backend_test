import json

import requests
from asgiref.sync import sync_to_async

from groups.models import Group

key = ''

@sync_to_async
def get_data_from_vk(id, action='create'):
    response = requests.post(
        url=f'https://api.vk.com/method/groups.getById?group_id={id}&access_token={key}&v=5.81&fields=name&fields=members_count'
    )
    group = json.loads(response.text)
    if action == 'create':
        new_group = Group.objects.create(id=int(group['response'][0]['id']),
                                         title=group['response'][0]['name'],
                                         users_count=group['response'][0]['members_count']
                                         )
        return new_group
    else:
        existed_group = Group.objects.get(id=id)
        existed_group.title = group['response'][0]['name']
        existed_group.users_count = group['response'][0]['members_count']
        existed_group.save()
        return existed_group
