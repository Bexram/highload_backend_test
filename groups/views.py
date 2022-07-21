from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config import settings
from services.vk import get_data_from_vk

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
from groups.models import Group
from groups.serializers import GroupSerializer


@sync_to_async
@api_view(["GET"])
def get_groups(request, pk):
    if pk in cache:
        products = cache.get(pk)
        return Response(products, status=status.HTTP_200_OK)
    else:
        try:
            queryset = Group.objects.get(id=pk)
        except ObjectDoesNotExist:
            queryset = get_data_from_vk(pk)
        serializer = GroupSerializer(queryset)
        cache.set(queryset.id, serializer.data, timeout=CACHE_TTL)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO: переодическая актуализация данных с ВК
