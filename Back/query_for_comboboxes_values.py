from Back.database_connector import get_connector


def get_product_types() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM ProductTypes;"
    cursor.execute(selection_query)

    record_list = cursor.fetchall()
    connector.close()

    return list(map(lambda record: record[0], record_list))


def get_product_units() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM MeasurmentUnits;"
    cursor.execute(selection_query)

    record_list = cursor.fetchall()
    connector.close()

    return list(map(lambda record: record[0], record_list))


def get_products_articles() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT ProductArticle FROM Products;"
    cursor.execute(selection_query)

    record_list = cursor.fetchall()
    connector.close()

    return list(map(lambda record: record[0], record_list))


def get_suppliers_inn() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT INN FROM Suppliers;"
    cursor.execute(selection_query)

    record_list = cursor.fetchall()
    connector.close()

    return list(map(lambda record: record[0], record_list))