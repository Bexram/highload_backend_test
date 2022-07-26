import asyncio
import json

from asgiref.sync import sync_to_async
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from rest_framework import status

from config import settings
from groups import redis
from services.vk import get_data_from_vk

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from groups.models import Group
from groups.serializers import GroupSerializer


async def get_groups(request, pk):
    group = await redis.get(pk)
    if group is not None:
        await redis.close()
        return JsonResponse(json.loads(group))
    else:
        try:
            queryset = await _get_queryset(pk)
        except ObjectDoesNotExist:
            queryset = await get_data_from_vk(pk)
        serializer = GroupSerializer(queryset)
        await redis.set(serializer.data['id'], json.dumps(serializer.data))
        await redis.close()
        return JsonResponse(serializer.data)


@sync_to_async
def _get_queryset(pk):
    return Group.objects.get(id=pk)


@sync_to_async
def _create_new_group(group):
    Group.objects.create(id=int(group['response'][0]['id']),
                         title=group['response'][0]['name'],
                         users_count=group['response'][0]['members_count']
                         )


@sync_to_async
def _get_groups_ids():
    ids = []
    groups = Group.objects.all()
    for group in groups:
        ids.append(group.id)
    return ids


async def update_db_api(request):
    groups = await _get_groups_ids()
    queue = asyncio.Queue()
    task_list = []
    for group in groups:
        task = asyncio.create_task(get_data_from_vk(group, 'update'))
        task_list.append(task)
    await queue.join()
    await asyncio.gather(*task_list, return_exceptions=True)
    return HttpResponse(status=status.HTTP_200_OK)
