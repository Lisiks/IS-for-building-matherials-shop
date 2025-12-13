from Back.database_connector import get_connector
from Back.validators import article_validation, client_card_validation


def get_sales() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = """SELECT Sales.Id, Sales.SaleDate, ClientSales.fk_client_card_number
    FROM Sales LEFT JOIN ClientSales ON Sales.Id = ClientSales.fk_sale_id ORDER BY Sales.SaleDate DESC;"""
    cursor.execute(selection_query)

    return cursor.fetchall()


def add_sale(date, client_card, product_article, product_count) -> int:
    if not article_validation(product_article):
        raise TypeError("Incorrect article")
    if not product_count.isdigit() or int(product_count) < 1:
        raise TypeError("Incorrect count")
    if client_card != "" and not client_card_validation(client_card):
        raise TypeError("Incorrect card")

    connector = get_connector()
    cursor = connector.cursor()

    check_article_query = "SELECT Count FROM Products WHERE ProductArticle = %s;"
    cursor.execute(check_article_query, (product_article,))
    query_result = cursor.fetchall()
    if len(query_result) != 1:
        raise TypeError("Article doesnt exist")
    elif query_result[0][0] < int(product_count):
        raise TypeError("Product count is very big")

    if client_card != "":
        checking_client = "SELECT count(*) FROM Clients WHERE DiscountCardNumber = %s;"
        cursor.execute(checking_client, (client_card,))
        if cursor.fetchall()[0][0] != 1:
            raise TypeError("Client doesnt exist")

    add_sale_query = """INSERT INTO Sales 
    (SaleDate, Products_ProductArticle, ProductCount)
    VALUES(%s, %s, %s)"""
    cursor.execute(add_sale_query, (date, product_article, int(product_count)))
    connector.commit()

    cursor.execute("""SELECT LAST_INSERT_ID();""")
    new_record_id = cursor.fetchall()[0][0]

    if client_card != "":
        add_sale_client_query = """INSERT INTO ClientSales VALUES(%s, %s)"""
        cursor.execute(add_sale_client_query, (new_record_id, client_card))

    update_product_count_query = """UPDATE Products SET Count = Count - %s WHERE ProductArticle = %s;"""
    cursor.execute(update_product_count_query, (product_count, product_article))
    connector.commit()

    return new_record_id


def del_sale(sale_id):
    connector = get_connector()
    cursor = connector.cursor()

    delete_sale_query = """DELETE FROM Sales WHERE ID = %s"""
    cursor.execute(delete_sale_query, (sale_id,))
    connector.commit()



def get_finding_sales(attribute) -> list:
    connector = get_connector()
    cursor = connector.cursor()

    liked_attribute = f"%{attribute}%"
    if attribute.isdigit():
        selection_query = """SELECT Sales.ID, Sales.SaleDate, ClientSales.Clients_DiscountCardNumber, Sales.Products_ProductArticle, Sales.ProductCount 
        FROM Sales LEFT JOIN ClientSales ON Sales.ID = ClientSales.Sales_ID
        WHERE Sales.SaleDate LIKE %s OR Sales.Products_ProductArticle LIKE %s OR Sales.ProductCount = %s OR ClientSales.Clients_DiscountCardNumber LIKE %s;"""
        cursor.execute(selection_query, (liked_attribute, liked_attribute, int(attribute), liked_attribute))
    else:
        selection_query = """SELECT Sales.ID, Sales.SaleDate, ClientSales.Clients_DiscountCardNumber, Sales.Products_ProductArticle, Sales.ProductCount 
        FROM Sales LEFT JOIN ClientSales ON Sales.ID = ClientSales.Sales_ID
        WHERE Sales.SaleDate LIKE %s OR Sales.Products_ProductArticle LIKE %s OR ClientSales.Clients_DiscountCardNumber LIKE %s;"""
        cursor.execute(selection_query, (liked_attribute, liked_attribute, liked_attribute))

    return cursor.fetchall()