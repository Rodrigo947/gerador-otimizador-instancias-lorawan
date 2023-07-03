from rest_framework import serializers

from db.repository import Cursor


class DataInstanceSerializer(serializers.Serializer):
  configs = serializers.DictField(allow_empty=False)
  areas = serializers.ListField(child=serializers.DictField(allow_empty=False), allow_empty=False)

  def validate_configs(self, configs):
    try:
      configs['clients'] = int(configs['clients'])
    except:
      raise serializers.ValidationError("Value of clients isn't a number.")

    if configs['clients'] <= 0:
      raise serializers.ValidationError("Value of clients must be greater than 0.")

    try:
      configs['seed'] = int(configs['seed'])
    except:
      raise serializers.ValidationError("Value of seed isn't a number.")

    if configs['seed'] <= 0:
      raise serializers.ValidationError("Value of seed must be greater than 0.")

    try:
      configs['transmissionPower'] = int(configs['transmissionPower'])
    except:
      raise serializers.ValidationError("Value of transmission power isn't a number.")

    if configs['transmissionPower'] not in [5, 20, 50, 100]:
      raise serializers.ValidationError("Value of transmission power invalid. Only accept 5, 20, 50 or 100.")

    try:
      configs['antennaGain'] = float(configs['antennaGain'])
    except:
      raise serializers.ValidationError("Value of antenna gain power isn't a number.")

    if configs['antennaGain'] < 0.01:
      raise serializers.ValidationError("Value of antenna gain must be greater or equal than 0.01.")

    try:
      configs['frequency'] = int(configs['frequency'])
    except:
      raise serializers.ValidationError("Value of frequency isn't a number.")

    if configs['frequency'] not in [433, 915]:
      raise serializers.ValidationError("Value of frequency invalid. Only accept 433 or 915.")

    try:
      configs['sf'] = int(configs['sf'])
    except:
      raise serializers.ValidationError("Value of SF isn't a number.")

    if configs['sf'] not in [7, 8, 9, 10, 11, 12]:
      raise serializers.ValidationError("Value of SF invalid. Only accept 7, 8, 9, 10, 11 or 12.")

    return configs

  def validate_areas(self, areas):
    totalPercent = 0

    for area in areas:
      try:
        totalPercent = totalPercent + int(area['percent'])
      except:
        raise serializers.ValidationError("Value of percent isn't a number")

      if type(area['coordinates']) is not list:
        raise serializers.ValidationError("Invalid coordinates")

      str_coordinates = []
      for coordinate in area['coordinates']:
        try:
          float(coordinate[0])
          float(coordinate[1])
          str_coordinates.append(f"{coordinate[0]} {coordinate[1]}")
        except:
          raise serializers.ValidationError("Invalid coordinates")

      try:
        if not Cursor.isValidArea(','.join(str_coordinates)):
          raise serializers.ValidationError("Invalid area")
        area['str_coordinates'] = ','.join(str_coordinates)
      except:
        raise serializers.ValidationError("Invalid area")

    if totalPercent != 100:
      raise serializers.ValidationError("The sum of weights must be 100")

    return areas
