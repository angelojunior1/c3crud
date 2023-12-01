import logging
import json
from conexion.mongo_queries import MongoQueries
from conexion.oracle_queries import OracleQueries

LIST_OF_COLLECTIONS = ["pacientes", "profissionais", "agendamentos"]

logger = logging.getLogger(name="Example_CRUD_MongoDB")
logger.setLevel(level=logging.WARNING)
mongo = MongoQueries()

def create_collections(drop_if_exists: bool = False):
    """
    Lista as coleções existentes, verifica se as coleções padrão estão entre as coleções existentes.
    Caso existam e o parâmetro de exclusão esteja configurado como True, irá apagar a coleção e criar novamente.
    Caso não existam, cria a coleção.

    Parâmetro:
              - drop_if_exists: True  -> apaga a coleção existente e recria
                                False -> não faz nada
    """
    mongo.connect()
    existing_collections = mongo.db.list_collection_names()
    for collection in LIST_OF_COLLECTIONS:
        if collection in existing_collections:
            if drop_if_exists:
                mongo.db.drop_collection(collection)
                logger.warning(f"{collection} dropped and recreated!")
        else:
            mongo.db.create_collection(collection)
            logger.warning(f"{collection} created!")
    mongo.close()

def insert_many(data: json, collection: str):
    mongo.connect()
    mongo.db[collection].insert_many(data)
    mongo.close()

def extract_and_insert():
    oracle = OracleQueries()
    oracle.connect()
    sql = "select * from labdatabase.{table}"
    for collection in LIST_OF_COLLECTIONS:
        df = oracle.sql_to_dataframe(sql.format(table=collection))
        if collection == "agendamentos":
            df["data_agendamento"] = df["data_agendamento"].dt.strftime("%m-%d-%Y")
        logger.warning(f"data extracted from Oracle database labdatabase.{collection}")
        records = json.loads(df.T.to_json()).values()
        logger.warning("data converted to json")
        insert_many(data=records, collection=collection)
        logger.warning(f"documents inserted into {collection} collection")

if __name__ == "__main__":
    logging.warning("Starting")
    create_collections(drop_if_exists=True)
    extract_and_insert()
    logging.warning("End")
