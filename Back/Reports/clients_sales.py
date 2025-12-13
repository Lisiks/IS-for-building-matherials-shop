from Back.database_connector import get_connector
from Back.Reports.date_binary_search import data_binary_search
from Back.Reports.calculate_date import calculate_start_end_date_from_period
from Back.Reports.data_clasess import Product, Client


def make_client_sales_reposts(period) -> list:
    start_date, end_date = calculate_start_end_date_from_period(period)

    connector = get_connector()
    cursor = connector.cursor()

    sales_query = """SELECT ALL SaleProducts.fk_product_article, Sales.SaleDate, SaleProducts.ProductCount, ClientSales.fk_client_card_number, Clients.DiscountPercentage
    FROM SaleProducts 
    JOIN Sales ON SaleProducts.fk_sale_id = Sales.Id 
    JOIN ClientSales ON Sales.Id = ClientSales.fk_sale_id 
    JOIN Clients ON ClientSales.fk_client_card_number = Clients.DiscountCardNumber
    WHERE Sales.SaleDate >= %s AND Sales.SaleDate < %s;"""
    cursor.execute(sales_query, (start_date, end_date))
    sales_records = cursor.fetchall()

    product_query = """SELECT Products.ProductArticle, Products.ProductName FROM Products;"""
    cursor.execute(product_query)
    product_data = cursor.fetchall()

    product_buying_price_story_query = """SELECT * FROM ProductsBuyingPriceChanges 
    ORDER BY ProductsBuyingPriceChanges.DateOfChange ASC;"""
    cursor.execute(product_buying_price_story_query)
    product_buying_price_data = cursor.fetchall()

    product_selling_price_query = """SELECT * FROM ProductsSellingPriceChanges 
    ORDER BY ProductsSellingPriceChanges.DateOfChange ASC;"""
    cursor.execute(product_selling_price_query)
    product_selling_price_data = cursor.fetchall()

    client_query = """SELECT DiscountCardNumber, FirstName, LastName FROM Clients;"""
    cursor.execute(client_query)
    clients_data = cursor.fetchall()


    product_hash = dict()
    client_hash = dict()
    for product_record in product_data:
        article, name = product_record
        new_product = Product(article, name)
        product_hash[article] = new_product

    for client_record in clients_data:
        card_number, first_name, last_name = client_record
        new_client = Client(card_number, f"{first_name} {last_name}", 0, 0.0, 0.0)
        client_hash[card_number] = new_client

    for change_buy_price_record in product_buying_price_data:
        date_of_change, buy_price, article = change_buy_price_record
        product_hash[article].buying_cost_list.append([date_of_change, buy_price])

    for change_sel_price_record in product_selling_price_data:
        date_of_change, sel_price, article = change_sel_price_record
        product_hash[article].selling_cost_list.append([date_of_change, sel_price])

    for sal_record in sales_records:
        article, date, count, client_card, discount = sal_record

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