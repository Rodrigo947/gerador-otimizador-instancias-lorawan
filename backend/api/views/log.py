from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Logs


class Log(APIView):

  def get(self, request):
    usedAt = Logs.objects.last()
    totalUse = Logs.objects.count()

    if (usedAt is None):
      return Response({'usedAt': 'No use yet', 'totalUse': totalUse})

    usedAt = usedAt.used_at.strftime('%Y-%m-%d %H:%M:%S')
    return Response({'usedAt': usedAt, 'totalUse': totalUse})
