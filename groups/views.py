import asyncio

from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from rest_framework import status

from config import settings
from services.vk import get_data_from_vk

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from groups.models import Group
from groups.serializers import GroupSerializer


async def get_groups(request, pk):
    group = cache.get(pk)
    if group is not None:
        return JsonResponse(group)
    else:
        try:
            queryset = await _get_queryset(pk)
        except ObjectDoesNotExist:
            queryset = await get_data_from_vk(pk)
        serializer = GroupSerializer(queryset)
        cache.set(serializer.data['id'], serializer.data, timeout=CACHE_TTL)
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
def _get_groups_list():
    return Group.objects.all()


# async def update_db_api(request):
#     groups = await _get_groups_list()
#     queue = asyncio.Queue()
#     task_list = []
#     for group in groups:
#         task = asyncio.create_task(get_data_from_vk(group.id, 'update'))
#         task_list.append(task)
#     await queue.join()
#     await asyncio.gather(*task_list, return_exceptions=True)
#     return HttpResponse(status=status.HTTP_200_OK)
