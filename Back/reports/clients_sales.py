from Back.database_connector import get_connector
from Back.reports.date_binary_search import data_binary_search
from datetime import datetime
from Back.reports.data_clasess import Product, Client


def make_client_sales_reposts(period) -> list:
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

    sales_query = """SELECT Sales.SaleDate, Sales.Products_ProductArticle, Sales.ProductCount, 
    Clients.DiscountCardNumber, Clients.DiscountPercentage 
    FROM Sales 
    INNER JOIN ClientSales ON Sales.ID = ClientSales.Sales_ID 
    INNER JOIN Clients ON ClientSales.Clients_DiscountCardNumber = Clients.DiscountCardNumber
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


    client_query = """SELECT DiscountCardNumber, FirstName, LastName FROM Clients;"""
    cursor.execute(client_query)
    clients_data = cursor.fetchall()
    connector.close()

    product_hash = dict()
    client_hash = dict()
    for product_record in product_data:
        article, name, buy_price, sel_price = product_record
        new_product = Product(article, name, actual_buying_price=buy_price, actual_selling_price=sel_price)
        product_hash[article] = new_product

    for client_record in clients_data:
        card_number, first_name, last_name = client_record
        new_client = Client(card_number, f"{first_name} {last_name}", 0, 0.0, 0.0)
        client_hash[card_number] = new_client

    for change_buy_price_record in product_buying_price_data:
        date_of_change, old_price, article = change_buy_price_record
        product_hash[article].buying_cost_list.append([date_of_change, old_price])

    for change_sel_price_record in product_selling_price_data:
        date_of_change, old_price, article = change_sel_price_record
        product_hash[article].selling_cost_list.append([date_of_change, old_price])

    for sal_record in sales_records:
        date, article, count, client_card, discount = sal_record

        buying_cost = data_binary_search(date, product_hash[article].buying_cost_list)
        selling_cost = data_binary_search(date, product_hash[article].selling_cost_list)

        full_discount = (100 - discount) / 100 if discount is not None else 1

        sale_cost = count * float(buying_cost)
        sale_revenue = count * float(selling_cost) * full_discount
        profit = sale_revenue - sale_cost

        client_hash[client_card].sales_count += count
        client_hash[client_card].sales_summ += sale_revenue
        client_hash[client_card].profit += profit

    return list(
        map(
            lambda current_client: (current_client.card_number, current_client.full_name, current_client.sales_count, round(current_client.sales_summ, 2), round(current_client.profit, 2)),
            filter(lambda current_client: current_client.sales_count > 0, client_hash.values())
        )
    )