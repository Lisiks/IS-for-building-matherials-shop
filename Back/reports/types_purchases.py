from Back.database_connector import get_connector
from Back.reports.date_binary_search import data_binary_search
from datetime import datetime
from Back.reports.data_clasess import Product, Type


def make_type_purchases_reposts(period) -> list:
    if period == "Месяц":
        current_month, current_year = datetime.now().month, datetime.now().year

        end_month = current_month + 1 if current_month != 12 else 1
        end_year = current_year if current_month != 12 else current_year + 1

        start_date = datetime.strptime(
            f"{current_year}-{current_month}-01 00:00:00",
            "%Y-%m-%d %H:%M:%S"

        )

        end_date = datetime.strptime(
            f"{end_year}-{end_month}-1 00:00:00",
            "%Y-%m-%d %H:%M:%S"
        )

    elif period == "Год":
        current_year = datetime.now().year
        end_year = current_year + 1

        start_date = datetime.strptime(
            f"{current_year}-01-01 00:00:00",
            "%Y-%m-%d %H:%M:%S"
        )

        end_date = datetime.strptime(
            f"{end_year}01-01 00:00:00",
            "%Y-%m-%d %H:%M:%S"
        )

    else:
        start_date = datetime.strptime(
            "0001-01-01 00:00:00",
            "%Y-%m-%d %H:%M:%S"
        )

        end_date = datetime.now().replace(microsecond=0)

    connector = get_connector()
    cursor = connector.cursor()

    purchases_query = """SELECT ALL Products_ProductArticle, PurchaseDate, ProductCount FROM Purchases 
    WHERE PurchaseDate >= %s AND PurchaseDate < %s;"""
    cursor.execute(purchases_query, (start_date, end_date))
    purchases_records = cursor.fetchall()

    product_query = """SELECT Products.ProductArticle, Products.ProductName, 
    ProductTypes_ProductType, Products.BuyingPrice FROM Products;"""
    cursor.execute(product_query)
    product_data = cursor.fetchall()

    product_buying_price_story_query = """SELECT * FROM ProductsBuyingPriceChanges 
    WHERE DateOfChange >= %s AND DateOfChange < %s
    ORDER BY ProductsBuyingPriceChanges.DateOfChange DESC;"""
    cursor.execute(product_buying_price_story_query, (start_date, end_date))
    product_buying_price_data = cursor.fetchall()

    types_query = """SELECT * FROM ProductTypes;"""
    cursor.execute(types_query)
    types_records = cursor.fetchall()

    connector.close()

    product_hash = dict()
    types_hash = dict()
    for product_record in product_data:
        article, name, prod_type, actual_buying_price = product_record
        product = Product(article, name, actual_buying_price=actual_buying_price, product_type=prod_type)
        product_hash[article] = product

    for type_record in types_records:
        name, *_ = type_record
        types_hash[name] = Type(name, 0, 0.0)

    for change_record in product_buying_price_data:
        date_of_change, old_price, article = change_record
        product_hash[article].buying_cost_list.append([date_of_change, old_price])

    for purchase_record in purchases_records:
        article, date, count = purchase_record
        cost = data_binary_search(date, product_hash[article].buying_cost_list)

        types_hash[product_hash[article].product_type].purchases_count += count
        types_hash[product_hash[article].product_type].purchases_summ += float(cost) * count

    return list(types_hash.values())