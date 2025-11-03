import json
from Back.database_connector import get_connector
from os.path import abspath


def get_organization_data() -> dict:
    organization_data_file_path = abspath("../JSON/organization_data.json")

    with open(organization_data_file_path, "r", encoding="utf-8") as org_data_file:
        org_data = json.loads(json.load(org_data_file))



    return org_data


def set_organization_data(org_name, org_inn, org_ogrn, org_telephone, org_address):
    org_data = dict()
    org_data["organization_name"] = org_name
    org_data["organization_inn"] = org_inn
    org_data["organization_ogrn"] = org_ogrn
    org_data["organization_telephone"] = org_telephone
    org_data["organization_address"] = org_address

    organization_data_file_path = abspath("../JSON/organization_data.json")
    with open(organization_data_file_path, "w", encoding="utf-8") as org_data_file:
        json.dump(json.dumps(org_data, indent=4), org_data_file)


def get_product_types() -> tuple:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM ProductTypes;"
    cursor.execute(selection_query)

    record_list = cursor.fetchall()
    connector.close()

    return tuple(map(lambda record: record[0], record_list))


def get_product_units() -> tuple:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM MeasurmentUnits;"
    cursor.execute(selection_query)

    record_list = cursor.fetchall()
    connector.close()

    return tuple(map(lambda record: record[0], record_list))


def add_product_type(product_type):
    if not (3 <= len(product_type) <= 30):
        raise AttributeError

    connector = get_connector()
    cursor = connector.cursor()

    add_query = "INSERT INTO ProductTypes VALUES(%s);"
    cursor.execute(add_query, (product_type,))

    connector.commit()
    connector.close()


def add_product_unit(product_unit):
    if not (1 <= len(product_unit) <= 30):
        raise AttributeError
    connector = get_connector()
    cursor = connector.cursor()

    add_query = "INSERT INTO MeasurmentUnits VALUES(%s);"
    cursor.execute(add_query, (product_unit,))

    connector.commit()
    connector.close()


def del_product_type(product_type):
    connector = get_connector()
    cursor = connector.cursor()

    control_query = "SELECT count(*) FROM ProductTypes WHERE ProductType = %s;"
    cursor.execute(control_query, (product_type,))

    if cursor.fetchall()[0][0] == 0:
        raise AttributeError

    add_query = "DELETE FROM ProductTypes WHERE ProductType = %s;"
    cursor.execute(add_query, (product_type,))

    connector.commit()
    connector.close()


def del_product_unit(product_unit):
    connector = get_connector()
    cursor = connector.cursor()

    control_query = "SELECT count(*) FROM MeasurmentUnits WHERE MeasurmentUnitName = %s;"
    cursor.execute(control_query, (product_unit,))
    if cursor.fetchall()[0][0] == 0:
        raise AttributeError

    add_query = "DELETE FROM MeasurmentUnits WHERE MeasurmentUnitName = %s;"
    cursor.execute(add_query, (product_unit,))

    connector.commit()
    connector.close()


