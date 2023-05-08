from django.db import connections


class Cursor:

  def create_tables(tb_name):
    with connections['default'].cursor() as cur:
      query = f"""
        CREATE TABLE tb_{tb_name}_areas (
          id bigserial PRIMARY KEY,
          area_coordinates geometry(polygon,4326),
          weight integer
        )
      """

      cur.execute(query)

      query = f"""
        CREATE TABLE tb_{tb_name}_clients (
          id bigserial PRIMARY KEY,
          id_area bigint,
          point_coordinates geometry(point,4326),
          FOREIGN KEY (id_area)
              REFERENCES tb_{tb_name}_areas (id) MATCH SIMPLE
              ON UPDATE NO ACTION
              ON DELETE NO ACTION
              NOT VALID
        )
      """

      cur.execute(query)

  def delete_tables(tb_name):
    with connections['default'].cursor() as cur:
      cur.execute(f'DROP TABLE tb_{tb_name}_clients')
      cur.execute(f'DROP TABLE tb_{tb_name}_areas')

  def isValidArea(str_coordinates):
    query = f"""SELECT 
      ST_IsValid('POLYGON (({str_coordinates}))'
    )"""

    with connections['default'].cursor() as cur:
      cur.execute(query)

      row = cur.fetchone()

      columns = [col[0] for col in cur.description]
      result = dict(zip(columns, row))

      return result['st_isvalid']

  def insert_area(tb_name, area_coordinates, weight):
    query = f"""
    INSERT INTO tb_{tb_name}_areas(area_coordinates, weight)
      VALUES ('POLYGON(({area_coordinates}))', {weight});
    """

    with connections['default'].cursor() as cur:
      cur.execute(query)

  def fetchall(query):
    with connections['default'].cursor() as cur:
      cur.execute(query)

      columns = [col[0] for col in cur.description]

      return [
          dict(zip(columns, row))
          for row in cur.fetchall()
      ]

  def createClientsInArea(id_area, quant_clients, seed, tb_name):
    query = f"""
    INSERT INTO public.tb_{tb_name}_clients(id_area, point_coordinates)
    SELECT {id_area}, geom
      FROM (
      SELECT (ST_Dump(
        ST_GeneratePoints(
          (SELECT 
            area_coordinates 
          FROM tb_{tb_name}_areas 
          WHERE id = {id_area}), {quant_clients}, {seed})
        )).geom as geom
      ) AS points;
    """
    with connections['default'].cursor() as cur:
      cur.execute(query)
