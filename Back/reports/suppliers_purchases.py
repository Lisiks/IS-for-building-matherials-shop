from Back.database_connector import get_connector
from Back.reports.date_binary_search import data_binary_search
from datetime import datetime
from Back.reports.data_clasess import Product, Supplier


def make_suppliers_purchases_reposts(period) -> list:
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
            f"{end_year}-01-01 00:00:00",
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

    purchases_query = """SELECT ALL Products_ProductArticle, Suppliers_INN, PurchaseDate, ProductCount FROM Purchases 
    WHERE PurchaseDate >= %s AND PurchaseDate < %s;"""
    cursor.execute(purchases_query, (start_date, end_date))
    sales_records = cursor.fetchall()

    product_query = """SELECT Products.ProductArticle, Products.ProductName, Products.BuyingPrice FROM Products;"""
    cursor.execute(product_query)
    product_data = cursor.fetchall()

    product_buying_price_story_query = """SELECT * FROM ProductsBuyingPriceChanges 
    WHERE DateOfChange >= %s AND DateOfChange < %s
    ORDER BY ProductsBuyingPriceChanges.DateOfChange DESC;"""
    cursor.execute(product_buying_price_story_query, (start_date, end_date))
    product_buying_price_data = cursor.fetchall()

    supplier_query = """SELECT INN, SupplierCompany FROM Suppliers;"""
    cursor.execute(supplier_query)
    suppliers_records = cursor.fetchall()

    connector.close()

    product_hash = dict()
    suppliers_hash = dict()
    for product_record in product_data:
        article, name, actual_buying_price = product_record
        product = Product(article, name, actual_buying_price=actual_buying_price)
        product_hash[article] = product

    for supplier_record in suppliers_records:
        inn, company = supplier_record
        suppliers_hash[inn] = Supplier(inn, company, 0, 0.0)

    for change_record in product_buying_price_data:
        date_of_change, old_price, article = change_record
        product_hash[article].buying_cost_list.append([date_of_change, old_price])

    for sales_record in sales_records:
        article, inn, date, count = sales_record
        cost = data_binary_search(date, product_hash[article].buying_cost_list)

        suppliers_hash[inn].purchases_count += count
        suppliers_hash[inn].purchases_summ += float(cost) * count

    return list(
        map(
            lambda current_supplier: (current_supplier.inn, current_supplier.name, current_supplier.purchases_count, round(current_supplier.purchases_summ, 2)),
            filter(lambda current_supplier: current_supplier.purchases_count > 0, suppliers_hash.values())
        )
    )