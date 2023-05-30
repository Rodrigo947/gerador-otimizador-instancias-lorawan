import time

import pandas as pd

from api.utils.random_utils import RandomUtils
from db.repository import Cursor


class CreateClients:
  def create(areas, seed, quant_clients):
    table_name = str(time.time()).replace('.', '')

    Cursor.create_tables(table_name)

    for area in areas:
      Cursor.insert_area(table_name, area['str_coordinates'], area['percent'])

    ru = RandomUtils(seed)
    ru.randomizeLocationClients(table_name, quant_clients)

    clients = Cursor.getClients(table_name)

    Cursor.delete_tables(table_name)

    return pd.DataFrame.from_dict(clients)
