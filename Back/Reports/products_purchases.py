from Back.database_connector import get_connector
from Back.Reports.date_binary_search import data_binary_search
from Back.Reports.calculate_date import calculate_start_end_date_from_period
from Back.Reports.data_clasess import Product


def make_product_purchases_reposts(period) -> list:
    start_date, end_date = calculate_start_end_date_from_period(period)

    connector = get_connector()
    cursor = connector.cursor()

    purchases_query = """SELECT ALL Products_ProductArticle, PurchaseDate, ProductCount FROM Purchases 
    WHERE PurchaseDate >= %s AND PurchaseDate < %s;"""
    cursor.execute(purchases_query, (start_date, end_date))
    purchase_records = cursor.fetchall()

    product_query = """SELECT Products.ProductArticle, Products.ProductName FROM Products;"""
    cursor.execute(product_query)
    product_data = cursor.fetchall()

    product_buying_price_story_query = """SELECT * FROM ProductsBuyingPriceChanges 
    WHERE DateOfChange >= %s AND DateOfChange < %s
    ORDER BY ProductsBuyingPriceChanges.DateOfChange ASC;"""
    cursor.execute(product_buying_price_story_query, (start_date, end_date))
    product_buying_price_data = cursor.fetchall()

    product_hash = dict()
    for product_record in product_data:
        article, name = product_record
        product = Product(article, name)
        product_hash[article] = product

    for change_record in product_buying_price_data:
        date_of_change, price, article = change_record
        product_hash[article].buying_cost_list.append([date_of_change, price])

    for purchase_record in purchase_records:
        article, date, count = purchase_record
        cost = data_binary_search(date, product_hash[article].buying_cost_list)

        product_hash[article].purchase_count += count
        product_hash[article].purchase_summ += count * float(cost)

    return list(
        map(
            lambda current_product: (current_product.article, current_product.name, current_product.purchase_count, round(current_product.purchase_summ, 2)),
            filter(lambda current_product: current_product.purchase_count > 0, product_hash.values())
            )
        )








