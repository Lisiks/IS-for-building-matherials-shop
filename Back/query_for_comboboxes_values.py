from Back.database_connector import get_connector


def get_product_types() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM ProductTypes;"
    cursor.execute(selection_query)

    record_list = cursor.fetchall()

    return list(map(lambda record: record[0], record_list))


def get_product_units() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM MeasurmentUnits;"
    cursor.execute(selection_query)

    record_list = cursor.fetchall()

    return list(map(lambda record: record[0], record_list))


def get_products_articles() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT ProductArticle, ProductName FROM Products;"
    cursor.execute(selection_query)

    record_list = cursor.fetchall()

    return list(map(lambda record: f"{record[0]} | {record[1]}", record_list))


def get_suppliers_inn() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT INN, SupplierCompany FROM Suppliers;"
    cursor.execute(selection_query)

    record_list = cursor.fetchall()

    return list(map(lambda record: f"{record[0]} | {record[1]}", record_list))


def get_client_cards() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT DiscountCardNumber, FirstName, LastName FROM Clients;"
    cursor.execute(selection_query)

    record_list = cursor.fetchall()

    return list(map(lambda record: f"{record[0]} | {record[1]} {record[2]}", record_list))