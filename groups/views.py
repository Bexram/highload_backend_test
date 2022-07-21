from asgiref.sync import sync_to_async
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from groups.models import Group
from groups.serializers import GroupSerializer


@sync_to_async
@api_view(["GET"])
def get_groups(request, pk):
    queryset = Group.objects.get(id=pk)
    serializer = GroupSerializer(queryset)
    return Response(serializer.data, status=status.HTTP_200_OK)
