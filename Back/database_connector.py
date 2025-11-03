import mysql.connector
import json
from os.path import abspath

database_connector = mysql.connector.connect()


def connect_to_database(*args):
    global database_connector

    config_file_path = abspath("../JSON/database_connect_config.json")

    with open(config_file_path, "r", encoding="utf-8") as config_file:
        config_data = json.load(config_file)

    database_connector = mysql.connector.connect(
        host=config_data["hst"],
        db=config_data["database"],
        user=config_data["user"],
        password=config_data["password"]
    )


def close_connection(*args):
    if database_connector.is_connected():
        database_connector.commit()
        database_connector.close()

