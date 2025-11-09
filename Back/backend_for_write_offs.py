from Back.database_connector import get_connector
from Back.validators import article_validation


def get_write_offs() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM WriteOffs;"
    cursor.execute(selection_query)

    connector.close()
    return cursor.fetchall()


def add_write_off(date, product_article, product_count, reason) -> int:
    if not article_validation(product_article):
        raise TypeError("Incorrect article")
    if not product_count.isdigit() or int(product_count) < 1:
        raise TypeError("Incorrect count")
    if len(reason) > 100:
        raise TypeError("Incorrect reason")

    connector = get_connector()
    cursor = connector.cursor()

    check_article_query = "SELECT Count FROM Products WHERE ProductArticle = %s;"
    cursor.execute(check_article_query, (product_article,))
    query_result = cursor.fetchall()
    if len(query_result) != 1:
        raise TypeError("Article doesnt exist")
    elif query_result[0][0] < int(product_count):
        raise TypeError("Product count is very big")

    add_write_off_query = """INSERT INTO WriteOffs 
    (WriteOffDate, Products_ProductArticle, ProductCount, OperationReason)
    VALUES(%s, %s, %s, %s)"""
    cursor.execute(add_write_off_query, (date, product_article, int(product_count), reason))
    connector.commit()

    cursor.execute("""SELECT LAST_INSERT_ID();""")
    new_record_id = cursor.fetchall()[0][0]

    update_product_count_query = """UPDATE Products SET Count = Count - %s WHERE ProductArticle = %s;"""
    cursor.execute(update_product_count_query, (product_count, product_article))
    connector.commit()

    connector.close()
    return new_record_id


def del_write_off(write_off_id):
    connector = get_connector()
    cursor = connector.cursor()

    delete_write_off_query = """DELETE FROM WriteOffs WHERE ID = %s"""
    cursor.execute(delete_write_off_query, (write_off_id,))
    connector.commit()
    connector.close()


def get_finding_write_off(attribute) -> list:
    connector = get_connector()
    cursor = connector.cursor()

    liked_attribute = f"%{attribute}%"

    if attribute.isdigit():
        selection_query = """SELECT * FROM WriteOffs 
        WHERE WriteOffDate LIKE %s OR Products_ProductArticle LIKE %s OR ProductCount = %s OR OperationReason LIKE %s;"""
        cursor.execute(selection_query, (liked_attribute, liked_attribute, int(attribute), liked_attribute))
    else:
        selection_query = """SELECT * FROM WriteOffs 
        WHERE WriteOffDate LIKE %s OR OperationReason LIKE %s;"""
        cursor.execute(selection_query,(liked_attribute, liked_attribute))
    connector.close()
    return cursor.fetchall()