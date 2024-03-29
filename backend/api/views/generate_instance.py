from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Logs
from api.serializers import DataInstanceSerializer
from api.utils.create_clients import CreateClients
from api.utils.create_gateways import CreateGateways


class GenerateInstance(APIView):
  serializer_class = DataInstanceSerializer

  def post(self, request):
    serializer = DataInstanceSerializer(data=request.data)

    if (serializer.is_valid()):
      areas = serializer.data['areas']
      seed = serializer.data['configs']['seed']
      quant_clients = serializer.data['configs']['clients']
      power = serializer.data['configs']['transmissionPower']
      antennaGain = serializer.data['configs']['antennaGain']
      frequency = serializer.data['configs']['frequency']
      sf = serializer.data['configs']['sf']

      clients = CreateClients.create(areas, seed, quant_clients)

      cg = CreateGateways(power, antennaGain, antennaGain, frequency, sf)
      cg.create(clients)

      gateways = cg.getValidGateways()

      log = Logs()
      log.save()

      return Response({'data': gateways})
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
