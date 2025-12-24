from Back.database_connector import get_connector
from Back.validators import inn_validation, telephone_validation, email_validation


def get_suppliers_data() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM Suppliers;"
    cursor.execute(selection_query)

    return cursor.fetchall()


def add_supplier(inn, name, address, telephone, email):
    if not inn_validation(inn):
        raise TypeError("Incorrect inn")

    if not 3 <= len(name) <= 30:
        raise TypeError("Incorrect name")

    if address != "" and not len(address) <= 100:
        raise TypeError("Incorrect address")

    if not telephone_validation(telephone):
        raise TypeError("Incorrect telephone")

    if email != "" and not email_validation(email):
        raise TypeError("Incorrect email")

    connector = get_connector()
    cursor = connector.cursor()

    check_inn_query = """SELECT count(*) FROM Suppliers WHERE INN = %s;"""
    cursor.execute(check_inn_query, (inn,))
    if cursor.fetchall()[0][0] != 0:
        raise TypeError("Existing inn")

    add_supplier_query = "INSERT INTO Suppliers VALUES(%s, %s, %s, %s, %s);"
    cursor.execute(add_supplier_query, (inn, name, address, telephone, email))
    connector.commit()


def update_supplier(old_inn, inn, name, address, telephone, email):
    if not inn_validation(inn):
        raise TypeError("Incorrect inn")

    if not 3 <= len(name) <= 30:
        raise TypeError("Incorrect name")

    if address != "" and not len(address) <= 100:
        raise TypeError("Incorrect address")

    if not telephone_validation(telephone):
        raise TypeError("Incorrect telephone")

    if email != "" and not email_validation(email):
        raise TypeError("Incorrect email")

    connector = get_connector()
    cursor = connector.cursor()

    check_inn_query = """SELECT count(*) FROM Suppliers WHERE INN = %s;"""
    cursor.execute(check_inn_query, (inn,))
    if cursor.fetchall()[0][0] != 0 and old_inn != inn:
        raise TypeError("Existing inn")

    update_supplier_query = """UPDATE Suppliers
    Set INN = %s, SupplierCompany = %s, Address = %s, TelephoneNumber = %s, Email = %s
    WHERE INN = %s;"""
    cursor.execute(update_supplier_query, (inn, name, address, telephone, email, old_inn))
    connector.commit()


def del_supplier(inn):
    connector = get_connector()
    cursor = connector.cursor()

    del_supplier_query = "DELETE FROM Suppliers WHERE INN = %s"
    cursor.execute(del_supplier_query, (inn,))

    connector.commit()


def get_finding_suppliers(attribute) -> list:
    connector = get_connector()
    cursor = connector.cursor()

    liked_attribute = f"%{attribute}%"

    if attribute.isdigit():
        selection_query = """SELECT * FROM Suppliers 
        WHERE INN LIKE %s OR SupplierCompany LIKE %s OR Address LIKE %s OR TelephoneNumber LIKE %s OR Email LIKE %s;"""
        cursor.execute(selection_query, (attribute, liked_attribute, liked_attribute, liked_attribute, liked_attribute))

    else:
        selection_query = """SELECT * FROM Suppliers 
        WHERE SupplierCompany LIKE %s OR Address LIKE %s OR TelephoneNumber LIKE %s OR Email LIKE %s;"""
        cursor.execute(selection_query, (liked_attribute, liked_attribute, liked_attribute, liked_attribute))

    return cursor.fetchall()






