from Back.database_connector import get_connector
from Back.Reports.date_binary_search import data_binary_search
from Back.Reports.calculate_date import calculate_start_end_date_from_period
from Back.Reports.data_clasess import Product


def make_product_sales_reposts(period) -> list:
    start_date, end_date = calculate_start_end_date_from_period(period)

    connector = get_connector()
    cursor = connector.cursor()

    sales_query = """SELECT Sales.SaleDate, Sales.Products_ProductArticle, Sales.ProductCount, Clients.DiscountPercentage 
    FROM Sales 
    LEFT JOIN ClientSales ON Sales.ID = ClientSales.Sales_ID 
    LEFT JOIN Clients ON ClientSales.Clients_DiscountCardNumber = Clients.DiscountCardNumber
    WHERE SaleDate >= %s AND SaleDate < %s;"""
    cursor.execute(sales_query, (start_date, end_date))
    sales_records = cursor.fetchall()

    product_query = """SELECT Products.ProductArticle, Products.ProductName, BuyingPrice,  SellingPrice FROM Products;"""
    cursor.execute(product_query)
    product_data = cursor.fetchall()

    product_buying_price_story_query = """SELECT * FROM ProductsBuyingPriceChanges 
    WHERE DateOfChange >= %s AND DateOfChange < %s
    ORDER BY ProductsBuyingPriceChanges.DateOfChange DESC;"""
    cursor.execute(product_buying_price_story_query, (start_date, end_date))
    product_buying_price_data = cursor.fetchall()

    product_selling_price_query = """SELECT * FROM ProductsSellingPriceChanges 
    WHERE DateOfChange >= %s AND DateOfChange < %s
    ORDER BY ProductsSellingPriceChanges.DateOfChange DESC;"""
    cursor.execute(product_selling_price_query, (start_date, end_date))
    product_selling_price_data = cursor.fetchall()
    connector.close()

    product_hash = dict()
    for product_record in product_data:
        article, name, buy_price, sel_price = product_record
        new_product = Product(article, name, actual_buying_price=buy_price, actual_selling_price=sel_price)
        product_hash[article] = new_product

    for change_buy_price_record in product_buying_price_data:
        date_of_change, old_price, article = change_buy_price_record
        product_hash[article].buying_cost_list.append([date_of_change, old_price])

    for change_sel_price_record in product_selling_price_data:
        date_of_change, old_price, article = change_sel_price_record
        product_hash[article].selling_cost_list.append([date_of_change, old_price])

    for sal_record in sales_records:
        date, article, count, discount = sal_record

        buying_cost = data_binary_search(date, product_hash[article].buying_cost_list)
        selling_cost = data_binary_search(date, product_hash[article].selling_cost_list)

        full_discount = (100 - discount) / 100 if discount is not None else 1

        sale_cost = count * float(buying_cost)
        sale_revenue = count * float(selling_cost) * full_discount
        profit = sale_revenue - sale_cost

        product_hash[article].sales_count += count
        product_hash[article].sales_summ += sale_revenue
        product_hash[article].profit += profit

    return list(
        map(
            lambda current_product: (current_product.article, current_product.name, current_product.sales_count, round(current_product.sales_summ, 2), round(current_product.profit, 2)),
            filter(lambda current_product: current_product.sales_count > 0, product_hash.values())
        )
    )
