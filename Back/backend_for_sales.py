from Back.database_connector import get_connector
from Back.validators import client_card_validation
from dataclasses import dataclass
@dataclass
class SaleInfo:
    sale_id: int
    sale_date: str
    client_card_number: str
    client_name: str
    client_discount: int
    product_list: list



def get_sales() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = """SELECT Sales.Id, Sales.SaleDate, ClientSales.fk_client_card_number
    FROM Sales LEFT JOIN ClientSales ON Sales.Id = ClientSales.fk_sale_id ORDER BY Sales.SaleDate DESC;"""
    cursor.execute(selection_query)

    return cursor.fetchall()


def add_sale(client_card_number, product_list) -> int:
    if client_card_number != "" and not client_card_validation(client_card_number):
        raise TypeError("Incorrect card")

    connector = get_connector()
    cursor = connector.cursor()

    if client_card_number != "":
        checking_client = "SELECT count(*) FROM Clients WHERE DiscountCardNumber = %s;"
        cursor.execute(checking_client, (client_card_number,))
        if cursor.fetchall()[0][0] == 0:
            raise TypeError("Client doesnt exist")

    for product_line in product_list:
        article, count = product_line
        check_product_query = """SELECT ProductArticle, Count FROM Products WHERE ProductArticle = %s;"""
        cursor.execute(check_product_query, (article,))

        product_data = cursor.fetchall()
        if len(product_data) == 0:
            raise TypeError("Article doesnt exist", article)
        if product_data[0][1] < int(count):
            raise TypeError("Big product count", article, count, product_data[0][1])

    add_sale_query = """INSERT INTO Sales VALUES();"""
    cursor.execute(add_sale_query)

    cursor.execute("""SELECT LAST_INSERT_ID();""")
    new_record_id = cursor.fetchall()[0][0]

    if client_card_number != "":
        add_sale_client_query = """INSERT INTO ClientSales VALUES(%s, %s)"""
        cursor.execute(add_sale_client_query, (new_record_id, client_card_number))

    for product_line in product_list:
        article, count = product_line
        adding_product_query = """INSERT INTO SaleProducts VALUES(%s, %s, %s);"""
        cursor.execute(adding_product_query, (new_record_id, article, int(count)))

        changing_product_count_query = "UPDATE Products SET Count = Count - %s WHERE ProductArticle = %s;"
        cursor.execute(changing_product_count_query, (int(count), article))

    connector.commit()

    current_record_query = """SELECT Sales.Id, Sales.SaleDate, ClientSales.fk_client_card_number
    FROM Sales LEFT JOIN ClientSales ON Sales.Id = ClientSales.fk_sale_id
    WHERE Sales.id = %s;"""
    cursor.execute(current_record_query, (new_record_id,))

    current_record = cursor.fetchall()[0]
    return current_record


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

    selection_query = """SELECT Sales.ID, Sales.SaleDate, ClientSales.fk_client_card_number
    FROM Sales LEFT JOIN ClientSales ON Sales.ID = ClientSales.fk_sale_id
    WHERE Sales.SaleDate LIKE %s OR ClientSales.fk_client_card_number LIKE %s
    ORDER BY Sales.SaleDate DESC;"""
    cursor.execute(selection_query, (liked_attribute, liked_attribute))

    return cursor.fetchall()

def get_sale_information(sale_id) -> SaleInfo:
    connector = get_connector()
    cursor = connector.cursor()

    sale_record_query = """SELECT Sales.Id, Sales.SaleDate, ClientSales.fk_client_card_number, Clients.FirstName, Clients.LastName, Clients.DiscountPercentage
    FROM Sales LEFT JOIN ClientSales ON Sales.Id = ClientSales.fk_sale_id LEFT JOIN Clients ON ClientSales.fk_client_card_number = Clients.DiscountCardNumber
    WHERE Sales.Id = %s;
    """

    cursor.execute(sale_record_query, (sale_id,))
    sale_id, sale_date, client_card_number, client_fam, client_name, client_discount = cursor.fetchall()[0]

    client_full_name = "" if client_card_number is None else f"{client_fam} {client_name}"

    sale_products = """SELECT SaleProducts.fk_product_article, Products.ProductName, SaleProducts.ProductCount
    FROM SaleProducts JOIN Products ON SaleProducts.fk_product_article = Products.ProductArticle
    WHERE SaleProducts.fk_sale_id = %s;"""
    cursor.execute(sale_products, (sale_id,))

    product_list = cursor.fetchall()

    for idx, products_info in enumerate(product_list):
        article, product_name, count = products_info
        product_price_query = """SELECT NewPrice FROM ProductsSellingPriceChanges
            WHERE Products_ProductArticle = %s AND DateOfChange <= %s
            ORDER BY DateOfChange DESC
            LIMIT 1;"""
        cursor.execute(product_price_query, (article, sale_date))
        price = cursor.fetchall()[0][0]

        product_list[idx] = [article, product_name, count, count * price]

    return SaleInfo(sale_id, sale_date, client_card_number, client_full_name, client_discount, product_list)