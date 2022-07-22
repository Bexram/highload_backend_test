from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

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
        cache.set(queryset.id, serializer.data, timeout=CACHE_TTL)
        return JsonResponse(serializer.data)


@sync_to_async
def _get_queryset(pk):
    return Group.objects.get(id=pk)
