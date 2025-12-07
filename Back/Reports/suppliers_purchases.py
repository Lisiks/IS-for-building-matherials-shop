from Back.database_connector import get_connector
from Back.Reports.date_binary_search import data_binary_search
from Back.Reports.calculate_date import calculate_start_end_date_from_period
from Back.Reports.data_clasess import Product, Supplier


def make_suppliers_purchases_reposts(period) -> list:
    start_date, end_date = calculate_start_end_date_from_period(period)

    connector = get_connector()
    cursor = connector.cursor()

    purchases_query = """SELECT ALL Products_ProductArticle, Suppliers_INN, PurchaseDate, ProductCount FROM Purchases 
    WHERE PurchaseDate >= %s AND PurchaseDate < %s;"""
    cursor.execute(purchases_query, (start_date, end_date))
    purchases_records = cursor.fetchall()

    product_query = """SELECT Products.ProductArticle, Products.ProductName FROM Products;"""
    cursor.execute(product_query)
    product_data = cursor.fetchall()

    product_buying_price_story_query = """SELECT * FROM ProductsBuyingPriceChanges 
    WHERE DateOfChange >= %s AND DateOfChange < %s
    ORDER BY ProductsBuyingPriceChanges.DateOfChange ASC;"""
    cursor.execute(product_buying_price_story_query, (start_date, end_date))
    product_buying_price_data = cursor.fetchall()

    supplier_query = """SELECT INN, SupplierCompany FROM Suppliers;"""
    cursor.execute(supplier_query)
    suppliers_records = cursor.fetchall()

    connector.close()

    product_hash = dict()
    suppliers_hash = dict()
    for product_record in product_data:
        article, name = product_record
        product = Product(article, name)
        product_hash[article] = product

    for supplier_record in suppliers_records:
        inn, company = supplier_record
        suppliers_hash[inn] = Supplier(inn, company, 0, 0.0)

    for change_record in product_buying_price_data:
        date_of_change, price, article = change_record
        product_hash[article].buying_cost_list.append([date_of_change, price])

    for purchase_record in purchases_records:
        article, inn, date, count = purchase_record
        cost = data_binary_search(date, product_hash[article].buying_cost_list)

        suppliers_hash[inn].purchases_count += count
        suppliers_hash[inn].purchases_summ += float(cost) * count

    return list(
        map(
            lambda current_supplier: (current_supplier.inn, current_supplier.name, current_supplier.purchases_count, round(current_supplier.purchases_summ, 2)),
            filter(lambda current_supplier: current_supplier.purchases_count > 0, suppliers_hash.values())
        )
    )