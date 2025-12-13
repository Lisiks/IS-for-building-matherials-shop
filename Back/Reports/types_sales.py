from Back.database_connector import get_connector
from Back.Reports.date_binary_search import data_binary_search
from Back.Reports.calculate_date import calculate_start_end_date_from_period
from Back.Reports.data_clasess import Product, Type


def make_type_sales_reposts(period) -> list:
    start_date, end_date = calculate_start_end_date_from_period(period)

    connector = get_connector()
    cursor = connector.cursor()

    sales_query = """SELECT ALL SaleProducts.fk_product_article, Sales.SaleDate, SaleProducts.ProductCount, Clients.DiscountPercentage
    FROM SaleProducts 
    JOIN Sales ON SaleProducts.fk_sale_id = Sales.Id 
    LEFT JOIN ClientSales ON Sales.Id = ClientSales.fk_sale_id 
    LEFT JOIN Clients ON ClientSales.fk_client_card_number = Clients.DiscountCardNumber
    WHERE Sales.SaleDate >= %s AND Sales.SaleDate < %s;"""
    cursor.execute(sales_query, (start_date, end_date))
    sales_records = cursor.fetchall()

    product_query = """SELECT Products.ProductArticle, Products.ProductName, ProductTypes_ProductType
    FROM Products;"""
    cursor.execute(product_query)
    product_data = cursor.fetchall()

    type_query = """SELECT ProductType FROM ProductTypes;"""
    cursor.execute(type_query)
    type_data = cursor.fetchall()

    product_buying_price_story_query = """SELECT * FROM ProductsBuyingPriceChanges 
    WHERE DateOfChange >= %s AND DateOfChange < %s
    ORDER BY ProductsBuyingPriceChanges.DateOfChange ASC;"""
    cursor.execute(product_buying_price_story_query, (start_date, end_date))
    product_buying_price_data = cursor.fetchall()

    product_selling_price_query = """SELECT * FROM ProductsSellingPriceChanges 
    WHERE DateOfChange >= %s AND DateOfChange < %s
    ORDER BY ProductsSellingPriceChanges.DateOfChange ASC;"""
    cursor.execute(product_selling_price_query, (start_date, end_date))
    product_selling_price_data = cursor.fetchall()

    product_hash = dict()
    type_hash = dict()
    for product_record in product_data:
        article, name, prod_type = product_record
        new_product = Product(article, name, product_type=prod_type)
        product_hash[article] = new_product

    for type_record in type_data:
        name, *_ = type_record
        new_type = Type(name, 0, 0.0, 0, 0.0, 0.0)
        type_hash[name] = new_type

    for change_buy_price_record in product_buying_price_data:
        date_of_change, buy_price, article = change_buy_price_record
        product_hash[article].buying_cost_list.append([date_of_change, buy_price])

    for change_sel_price_record in product_selling_price_data:
        date_of_change, sel_price, article = change_sel_price_record
        product_hash[article].selling_cost_list.append([date_of_change, sel_price])

    for sal_record in sales_records:
        article, date, count, discount = sal_record

        buying_cost = data_binary_search(date, product_hash[article].buying_cost_list)
        selling_cost = data_binary_search(date, product_hash[article].selling_cost_list)

        full_discount = (100 - discount) / 100 if discount is not None else 1

        sale_cost = count * float(buying_cost)
        sale_revenue = count * float(selling_cost) * full_discount
        profit = sale_revenue - sale_cost

        type_hash[product_hash[article].product_type].sales_count += count
        type_hash[product_hash[article].product_type].sales_summ += sale_revenue
        type_hash[product_hash[article].product_type].profit += profit

    return list(
        map(
            lambda current_type: (current_type.name, current_type.sales_count, round(current_type.sales_summ, 2), round(current_type.profit, 2)),
            filter(lambda current_type: current_type.sales_count > 0, type_hash.values())
        )
    )