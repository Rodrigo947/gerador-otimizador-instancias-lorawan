import time

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import DataInstanceSerializer
from api.utils.random_utils import RandomUtils
from db.repository import Cursor


class GenerateInstance(APIView):
  serializer_class = DataInstanceSerializer

  def post(self, request):
    serializer = DataInstanceSerializer(data=request.data)

    if (serializer.is_valid()):
      table_name = str(time.time()).replace('.', '')

      Cursor.create_tables(table_name)

      for area in serializer.data['areas']:
        Cursor.insert_area(table_name, area['str_coordinates'], area['percent'])

      ru = RandomUtils(serializer.data['configs']['seed'])
      ru.randomizeLocationClients(
          tb_name=table_name, quant_clients=serializer.data['configs']['clients'])

      clients = Cursor.getClients(table_name)

      Cursor.delete_tables(table_name)
      return Response({'data': clients})
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
