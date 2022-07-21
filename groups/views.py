from asgiref.sync import sync_to_async
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from config import settings

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
        queryset = Group.objects.get(id=pk)
        serializer = GroupSerializer(queryset)
        cache.set(queryset.id, serializer.data, timeout=CACHE_TTL)
    return Response(serializer.data, status=status.HTTP_200_OK)

#TODO: получение данных с вк если не найдено в БД
#TODO: переодическая актуализация данных с ВК