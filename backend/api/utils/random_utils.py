import random

from db.repository import Cursor


class RandomUtils:

  def __init__(self, seed):
    random.seed(seed)
    self.seed = seed

  def generateRandomNumber(self):
    return random.randint(0, 99)

  def generateDictPossibilities(self, tb_name):
    results = Cursor.fetchall(f"SELECT * FROM tb_{tb_name}_areas")
    dictNumberIdArea = {}

    rangeStart = 0
    for result in results:
      for n in range(rangeStart, rangeStart + result['weight']):
        dictNumberIdArea[n] = result['id']
      rangeStart = rangeStart + result['weight']

    return dictNumberIdArea

  def randomizeLocationClients(self, tb_name, quant_clients):
    dictNumberIdArea = self.generateDictPossibilities(tb_name)

    quantClientsByArea = {}
    n = 0
    while (n < int(quant_clients)):
      idArea = dictNumberIdArea[self.generateRandomNumber()]
      quantClientsByArea[idArea] = quantClientsByArea[idArea] + 1 if idArea in quantClientsByArea else 1
      n = n + 1

    for idArea, quant in quantClientsByArea.items():
      Cursor.createClientsInArea(idArea, quant, self.seed, tb_name)
