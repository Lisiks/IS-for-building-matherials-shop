import mysql.connector
import json
from os.path import abspath

database_connector = None


def get_connector() -> mysql.connector.connect:
    global database_connector
    if database_connector is None or not database_connector.is_connected():
        config_file_path = abspath("JSON/database_connect_config.json")
        print(1)

        with open(config_file_path, "r", encoding="utf-8") as config_file:
            config_data = json.load(config_file)

        database_connector = mysql.connector.connect(
            host=config_data["host"],
            db=config_data["database"],
            user=config_data["user"],
            password=config_data["password"]
        )

    return database_connector





