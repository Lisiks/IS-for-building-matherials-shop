from Back.database_connector import get_connector
from Back.validators import inn_validation
from dataclasses import dataclass


@dataclass
class PurchaseInfo:
    purchase_id: int
    purchase_date: str
    supplier_inn: str
    supplier_name: str
    landing_bill_number: str
    product_list: list


def get_purchases() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM Purchases;"
    cursor.execute(selection_query)

    return cursor.fetchall()


def add_purchase(suppliers_inn, document, product_list) -> int:
    if not inn_validation(suppliers_inn):
        raise TypeError("Incorrect inn")
    if not 1 <= len(document) <= 30:
        raise TypeError("Incorrect document")

    connector = get_connector()
    cursor = connector.cursor()

    check_inn_query = "SELECT count(*) FROM Suppliers WHERE INN = %s;"
    cursor.execute(check_inn_query, (suppliers_inn,))
    if cursor.fetchall()[0][0] != 1:
        raise TypeError("Suppliers doesnt exist")

    for product_line in product_list:
        article, count = product_line
        check_article_query = "SELECT * FROM Products WHERE ProductArticle = %s;"
        cursor.execute(check_article_query, (article,))
        if len(cursor.fetchall()) == 0:
            raise TypeError("Article doesnt exist")

    add_purchase_query = "INSERT INTO Purchases(LandingBillNumber, fk_supplier_inn) VALUES (%s, %s);"
    cursor.execute(add_purchase_query, (document, suppliers_inn))

    current_record_query = "SELECT * FROM Purchases WHERE Id = LAST_INSERT_ID();"
    cursor.execute(current_record_query)

    current_record = cursor.fetchall()[0]
    for product_line in product_list:
        article, count = product_line
        adding_product_query = "INSERT INTO PurchaseProducts VALUES(%s, %s, %s);"
        cursor.execute(adding_product_query, (current_record[0], article, int(count)))
        changing_product_count_query = "UPDATE Products SET Count = Count + %s WHERE ProductArticle = %s;"
        cursor.execute(changing_product_count_query, (count, article))

    connector.commit()
    return current_record


def del_purchase(purchases_id):
    connector = get_connector()
    cursor = connector.cursor()

    delete_purchase_query = """DELETE FROM Purchases WHERE Id = %s"""
    cursor.execute(delete_purchase_query, (purchases_id,))
    connector.commit()


def get_finding_purchases(attribute) -> list:
    connector = get_connector()
    cursor = connector.cursor()

    liked_attribute = f"%{attribute}%"

    selection_query = """SELECT * FROM Purchases 
    WHERE PurchaseDate LIKE %s OR fk_supplier_inn LIKE %s OR LandingBillNumber LIKE %s;"""
    cursor.execute(selection_query, (liked_attribute, liked_attribute, liked_attribute))

    return cursor.fetchall()


def get_purchase_information(purchase_id) -> PurchaseInfo:
    connector = get_connector()
    cursor = connector.cursor()

    purchase_record_query = """SELECT Purchases.Id, Purchases.fk_supplier_inn, Suppliers.SupplierCompany, Purchases.LandingBillNumber, Purchases.PurchaseDate
    FROM Purchases INNER JOIN Suppliers ON Purchases.fk_supplier_inn = Suppliers.INN
    WHERE Purchases.Id = %s;
    """
    cursor.execute(purchase_record_query, (purchase_id,))
    purchase_id, supplier_inn, supplier_company, landing_bill_number, purchase_date = cursor.fetchall()[0]


    purchase_products = """SELECT PurchaseProducts.fk_product_article, Products.ProductName, PurchaseProducts.ProductCount
    FROM PurchaseProducts JOIN Products ON PurchaseProducts.fk_product_article = Products.ProductArticle
    WHERE PurchaseProducts.fk_purchase_id = %s;"""
    cursor.execute(purchase_products, (purchase_id,))

    product_list = cursor.fetchall()

    for idx, products_info in enumerate(product_list):
        article, product_name, count = products_info
        product_price_query = """SELECT NewPrice FROM ProductsBuyingPriceChanges
        WHERE Products_ProductArticle = %s AND DateOfChange <= %s
        ORDER BY DateOfChange DESC
        LIMIT 1;"""
        cursor.execute(product_price_query, (article, purchase_date))
        price = cursor.fetchall()[0][0]

        product_list[idx] = [article, product_name, count, count*price]

    return PurchaseInfo(purchase_id, str(purchase_date), supplier_inn, supplier_company, landing_bill_number, product_list)





