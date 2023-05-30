import numpy as np
import pandas as pd
from sklearn.cluster import KMeans

from api.utils.validate_gateway import ValidateGateway


class CreateGateways:

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
    self.valid_gateways = []
    self.vg = ValidateGateway(power, transmissionAntennaGain, receiveAntennaGain, frequency, sf)

  def clustering(self, df_clients: pd.DataFrame, clusters):
    kmeans = KMeans(n_clusters=clusters, init='k-means++')
    kmeans.fit(df_clients)  # Compute k-means clustering.
    df_clients['gateway_index'] = kmeans.fit_predict(df_clients)
    centers = kmeans.cluster_centers_  # Coordinates of cluster centers.

    return centers, df_clients

  def create(self, df_clients: pd.DataFrame, clusters=1):

    possible_gateways, clients_and_labels = self.clustering(df_clients, clusters)

    for index, gateway in enumerate(possible_gateways):
      clients_of_gateway = clients_and_labels[clients_and_labels['gateway_index'] == index]
      isValid, clients = self.vg.isValidGateway(gateway, clients_of_gateway)
      if isValid:
        self.valid_gateways.append({
            "gateway": {"longitude": gateway[0], "latitude": gateway[1]},
            "clients": clients.to_dict(orient='records')
        })
      else:
        self.create(clients_of_gateway[['longitude', 'latitude']], 2)

  def getValidGateways(self):
    return self.valid_gateways
