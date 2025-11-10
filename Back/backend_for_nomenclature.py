from Back.database_connector import get_connector
from Back.validators import article_validation, float_validation


def get_nomenclature() -> list:
    connector = get_connector()
    cursor = connector.cursor()

    selection_query = "SELECT * FROM Products"
    cursor.execute(selection_query)

    connector.close()

    return cursor.fetchall()


def add_product(article, name, buy_price, sel_price, prod_type, prod_unit):
    if not article_validation(article):
        raise TypeError("Incorrect length")

    if not (3 <= len(name) <= 30):
        raise TypeError("Incorrect name length")

    float_buy_price = round(float(buy_price), 2)
    if not (0.01 <= float_buy_price <= 99999999.99):
        raise TypeError("Incorrect buy price value")

    float_sel_price = round(float(sel_price), 2)
    if not (0.01 <= float_sel_price <= 99999999.99):
        raise TypeError("Incorrect sel price value")

    if prod_type == "" or prod_unit == "":
        raise TypeError("Type or unit is empy")

    connector = get_connector()
    cursor = connector.cursor()

    check_article_query = """SELECT count(*) FROM Products WHERE ProductArticle = %s;"""
    cursor.execute(check_article_query, (article,))
    if cursor.fetchall()[0][0] != 0:
        raise TypeError("Existing article")

    add_product_query = """INSERT INTO Products(ProductArticle, ProductName, BuyingPrice, SellingPrice, 
    ProductTypes_ProductType, MeasurmentUnits_MeasurmentUnitsName)
    VALUES (%s, %s, %s, %s, %s, %s);"""
    cursor.execute(add_product_query, (article, name, buy_price, sel_price, prod_type, prod_unit))

    connector.commit()
    connector.close()


def update_product(old_article, article, name, buy_price, sel_price, prod_type, prod_unit):
    if not article_validation(article):
        raise TypeError("Incorrect length")

    if not (3 <= len(name) <= 30):
        raise TypeError("Incorrect name length")

    float_buy_price = round(float(buy_price), 2)
    if not (0.01 <= float_buy_price <= 99999999.99):
        raise TypeError("Incorrect buy price value")

    float_sel_price = round(float(sel_price), 2)
    if not (0.01 <= float_sel_price <= 99999999.99):
        raise TypeError("Incorrect sel price value")

    if prod_type == "" or prod_unit == "":
        raise TypeError("Type or unit is empy")

    connector = get_connector()
    cursor = connector.cursor()

    check_article_query = """SELECT count(*) FROM Products WHERE ProductArticle = %s;"""
    cursor.execute(check_article_query, (article,))
    if cursor.fetchall()[0][0] != 0 and old_article != article:
        raise TypeError("Existing article")

    update_product_query = """UPDATE Products
    SET ProductArticle = %s, ProductName = %s, BuyingPrice = %s, SellingPrice = %s, 
    ProductTypes_ProductType = %s, MeasurmentUnits_MeasurmentUnitsName = %s
    WHERE ProductArticle = %s;"""
    cursor.execute(update_product_query, (article, name, buy_price, sel_price, prod_type, prod_unit, old_article))

    connector.commit()
    connector.close()


def del_product(article):
    connector = get_connector()
    cursor = connector.cursor()

    add_product_query = "DELETE FROM Products WHERE ProductArticle = %s"
    cursor.execute(add_product_query, (article,))

    connector.commit()
    connector.close()


def get_finding_products(attribute) -> list:
    connector = get_connector()
    cursor = connector.cursor()

    liked_attribute = f"%{attribute}%"

    if attribute.isdigit():
        selection_query = """SELECT * FROM Products 
        WHERE ProductArticle LIKE %s OR Count = %s OR BuyingPrice = %s OR SellingPrice = %s OR
        ProductName LIKE %s OR ProductTypes_ProductType LIKE %s OR MeasurmentUnits_MeasurmentUnitsName LIKE %s;"""
        cursor.execute(
            selection_query,
            (liked_attribute,
             int(attribute),
             float(attribute),
             float(attribute),
             liked_attribute,
             liked_attribute,
             liked_attribute)
        )

    elif float_validation(attribute):
        selection_query = """SELECT * FROM Products 
        WHERE BuyingPrice = %s OR SellingPrice = %s OR ProductName LIKE %s OR ProductTypes_ProductType LIKE %s 
        OR MeasurmentUnits_MeasurmentUnitsName LIKE %s;"""
        cursor.execute(
            selection_query,
            (float(attribute), float(attribute), liked_attribute, liked_attribute, liked_attribute)
        )
    else:
        selection_query = """SELECT * FROM Products 
        WHERE ProductName LIKE %s OR ProductTypes_ProductType LIKE %s OR MeasurmentUnits_MeasurmentUnitsName LIKE %s;"""
        cursor.execute(selection_query, (liked_attribute, liked_attribute, liked_attribute))

    connector.close()
    return cursor.fetchall()

