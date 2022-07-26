import json

import httpx

key = ''

async def get_data_from_vk(id, action='create'):
    from groups.views import _create_new_group, _get_queryset
    group = {}
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f'https://api.vk.com/method/groups.getById?group_id={id}&access_token={key}&v=5.81&fields=name&fields=members_count'
        )
        print(f'get {id} {r}')
        group = json.loads(r.text)
    if action == 'create':
        await _create_new_group(group)
        new_group = {
            'id': group['response'][0]['id'],
            'title': group['response'][0]['name'],
            'users_count': group['response'][0]['members_count']
        }
        return new_group
    else:
        existed_group = await _get_queryset(id)
        existed_group.title = group['response'][0]['name']
        existed_group.users_count = group['response'][0]['members_count']
        existed_group.save()
        print(f'update {id}')
        return existed_group
