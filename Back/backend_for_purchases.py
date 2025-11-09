from Back.database_connector import get_connector
from Back.validators import inn_validation, article_validation


def get_purchases() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM Purchases;"
    cursor.execute(selection_query)

    connector.close()
    return cursor.fetchall()


def add_purchase(date, suppliers_inn, document, product_article, product_count) -> int:
    if not inn_validation(suppliers_inn):
        raise TypeError("Incorrect inn")
    if not 1 <= len(document) <= 30:
        raise TypeError("Incorrect document")
    if not article_validation(product_article):
        raise TypeError("Incorrect article")
    if not product_count.isdigit() or int(product_count) < 1:
        raise TypeError("Incorrect count")

    connector = get_connector()
    cursor = connector.cursor()

    check_inn_query = "SELECT count(*) FROM Suppliers WHERE INN = %s;"
    cursor.execute(check_inn_query, (suppliers_inn,))
    if cursor.fetchall()[0][0] != 1:
        raise TypeError("Suppliers doesnt exist")

    check_article_query = "SELECT count(*) FROM Products WHERE ProductArticle = %s;"
    cursor.execute(check_article_query, (product_article,))
    if cursor.fetchall()[0][0] != 1:
        raise TypeError("Article doesnt exist")

    add_purchases_query = """INSERT INTO Purchases 
    (PurchaseDate, Suppliers_INN, LandingBillNumber, Products_ProductArticle, ProductCount)
    VALUES(%s, %s, %s, %s, %s)"""
    cursor.execute(add_purchases_query, (date, suppliers_inn, document, product_article, int(product_count)))
    connector.commit()

    cursor.execute("""SELECT LAST_INSERT_ID();""")
    new_record_id = cursor.fetchall()[0][0]

    update_product_count_query = """UPDATE Products SET Count = Count + %s WHERE ProductArticle = %s;"""
    cursor.execute(update_product_count_query, (product_count, product_article))
    connector.commit()

    connector.close()
    return new_record_id


def del_purchase(purchases_id):
    connector = get_connector()
    cursor = connector.cursor()

    delete_purcahse_query = """DELETE FROM Purchases WHERE ID = %s"""
    cursor.execute(delete_purcahse_query, (purchases_id,))
    connector.commit()
    connector.close()


def get_finding_purchases(attribute) -> list:
    connector = get_connector()
    cursor = connector.cursor()

    liked_attribute = f"%{attribute}%"

    if attribute.isdigit():
        selection_query = """SELECT * FROM Purchases 
        WHERE PurchaseDate LIKE %s OR Suppliers_INN LIKE %s OR LandingBillNumber LIKE %s OR Products_ProductArticle LIKE %s OR ProductCount = %s;"""
        cursor.execute(selection_query, (liked_attribute, liked_attribute, liked_attribute, liked_attribute, int(attribute)))
    else:
        selection_query = """SELECT * FROM Purchases 
        WHERE PurchaseDate LIKE %s OR LandingBillNumber LIKE %s;"""
        cursor.execute(selection_query,(liked_attribute, liked_attribute))
    connector.close()
    return cursor.fetchall()
