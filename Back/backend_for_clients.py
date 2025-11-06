from Back.database_connector import get_connector
from Back.validators import telephone_validation


def get_clients_data() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM Clients;"
    cursor.execute(selection_query)
    connector.close()

    return cursor.fetchall()


def add_client(card, fam, name, telephone, discount) -> list:
    if not (card.isdigit() and len(card) == 10):
        raise TypeError("Incorrect card")

    if not 2 <= len(name) <= 30:
        raise TypeError("Incorrect name")

    if not 2 <= len(fam) <= 30:
        raise TypeError("Incorrect fam")

    if not telephone_validation(telephone):
        raise TypeError("Incorrect telephone")

    if not (discount.isdigit and 1 <= int(discount) <= 100):
        raise TypeError("Incorrect discount")

    connector = get_connector()
    cursor = connector.cursor()

    add_clients_query = "INSERT INTO Clients VALUES(%s, %s, %s, %s, %s);"
    cursor.execute(add_clients_query, (card, fam, name, telephone, discount))
    connector.commit()
    connector.close()

    added_record = [card, fam, name, telephone, discount]

    return added_record


def update_client(old_card, card, fam, name, telephone, discount) -> list:
    if not (card.isdigit() and len(card) == 10):
        raise TypeError("Incorrect card")

    if not 3 <= len(name) <= 30:
        raise TypeError("Incorrect name")

    if not 3 <= len(fam) <= 30:
        raise TypeError("Incorrect fam")

    if not telephone_validation(telephone):
        raise TypeError("Incorrect telephone")

    if not (discount.isdigit and 1 <= int(discount) <= 100):
        raise TypeError("Incorrect discount")

    connector = get_connector()
    cursor = connector.cursor()

    update_client_query = """UPDATE Clients
    Set DiscountCardNumber = %s, FirstName = %s, LastName = %s, TelephoneNumber = %s, DiscountPercentage = %s
    WHERE DiscountCardNumber = %s;"""
    cursor.execute(update_client_query, (card, fam, name, telephone, discount, old_card))
    connector.commit()
    connector.close()

    updated_record = [card, fam, name, telephone, discount]

    return updated_record


def del_client(card):
    connector = get_connector()
    cursor = connector.cursor()

    del_clients_query = "DELETE FROM Clients WHERE DiscountCardNumber = %s"
    cursor.execute(del_clients_query, (card,))

    connector.commit()
    connector.close()


def get_finding_clients(attribute) -> list:
    connector = get_connector()
    cursor = connector.cursor()

    liked_attribute = f"%{attribute}%"
    if attribute.isdigit():
        selection_query = """SELECT * FROM Clients 
        WHERE DiscountCardNumber LIKE %s OR FirstName LIKE %s OR LastName LIKE %s OR TelephoneNumber LIKE %s OR DiscountPercentage LIKE %s;"""
        cursor.execute(selection_query, (liked_attribute, liked_attribute, liked_attribute, liked_attribute, int(attribute)))
    else:
        selection_query = """SELECT * FROM Clients
        WHERE DiscountCardNumber LIKE %s OR FirstName LIKE %s OR LastName LIKE %s OR TelephoneNumber LIKE %s;"""
        cursor.execute(selection_query,(liked_attribute, liked_attribute, liked_attribute, liked_attribute))

    connector.close()
    return cursor.fetchall()