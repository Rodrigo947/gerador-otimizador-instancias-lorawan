import math

import geopy.distance
import pandas as pd


class ValidateGateway:

  def __init__(self, power, transmissionAntennaGain, receiveAntennaGain, frequency, sf):
    """
      power(mW) | 
      transmissionAntennaGain(dBi) |
      receiveAntennaGain(dBi) |
      frequency(MHz) |
    """
    self.power = power
    self.transmissionAntennaGain = transmissionAntennaGain
    self.receiveAntennaGain = receiveAntennaGain
    self.frequency = frequency
    self.sf = sf
    self.PI = 3.14159265358979323846
    self.SFs = [7, 8, 9, 10, 11, 12]
    self.SFNoiseLimits = {
        7: -7.5,
        8: -10,
        9: -12.5,
        10: -15,
        11: -17.5,
        12: -20
    }
    self.SFDistanceLimits = {
        7: 3500,
        8: 4000,
        9: 5000,
        10: 6000,
        11: 7500,
        12: 9000
    }

  def calcPr(self, distance):
    """
      distance(meters)
    """
    divisor = 4*self.PI*distance*self.frequency
    if divisor == 0:
      return 0

    return self.power*self.transmissionAntennaGain*self.receiveAntennaGain*pow(300/divisor, 2)

  def snr(self, totalNoise, noisePoint):
    divisor = totalNoise-noisePoint
    if divisor == 0:
      return 0
    return 20*math.log10(self.power/divisor)

  def distance(self, coords_1, coords_2):
    """
    coords = (lat, long)
    """

    distance = geopy.distance.geodesic(coords_1, coords_2).meters

    return distance

  def isValidGateway(self, gateway, clients: pd.DataFrame):
    coords_gateway = (gateway[1], gateway[0])

    for index, row in clients.iterrows():
      distance = self.distance(coords_gateway, tuple(row[['latitude', 'longitude']]))

      if distance > self.SFDistanceLimits[self.sf]:
        return False, False

      pr = self.calcPr(distance)
      clients.at[index, 'distance_to_gateway'] = distance
      clients.at[index, 'pr'] = pr

    totalNoise = clients['pr'].sum()
    for index, row in clients.iterrows():
      snr = self.snr(totalNoise, row['pr'])

      if snr < self.SFNoiseLimits[self.sf]:
        return False, False

    return True, clients
