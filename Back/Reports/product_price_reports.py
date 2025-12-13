from Back.database_connector import get_connector
from Back.Reports.calculate_date import calculate_start_end_date_from_period


def make_product_buying_price_report(period, article):
    start_date, end_date = calculate_start_end_date_from_period(period)

    connector = get_connector()
    cursor = connector.cursor()

    check_article_query = """SELECT ProductName FROM Products WHERE ProductArticle = %s;"""
    cursor.execute(check_article_query, (article,))
    product_query_result = cursor.fetchall()

    if len(product_query_result) == 0:
        raise TypeError("Article doesnt exist")

    product_name = product_query_result[0][0]

    buying_price_query = """SELECT DateOfChange, NewPrice FROM ProductsBuyingPriceChanges
    WHERE Products_ProductArticle = %s AND DateOfChange >= %s AND DateOfChange < %s
    ORDER BY DateOfChange;"""
    cursor.execute(buying_price_query, (article, start_date, end_date))
    buying_price_data = cursor.fetchall()

    date_list = [str(change_data[0]).replace(" ", "\n") for change_data in buying_price_data]
    price_list = [float(change_data[1]) for change_data in buying_price_data]

    return product_name, date_list, price_list


def make_product_selling_price_report(period, article):
    start_date, end_date = calculate_start_end_date_from_period(period)

    connector = get_connector()
    cursor = connector.cursor()

    check_article_query = """SELECT ProductName FROM Products WHERE ProductArticle = %s;"""
    cursor.execute(check_article_query, (article,))
    product_query_result = cursor.fetchall()

    if len(product_query_result) == 0:
        raise TypeError("Article doesnt exist")

    product_name = product_query_result[0][0]

    selling_price_query = """SELECT DateOfChange, NewPrice FROM ProductsSellingPriceChanges
    WHERE Products_ProductArticle = %s AND DateOfChange >= %s AND DateOfChange < %s
    ORDER BY DateOfChange;"""
    cursor.execute(selling_price_query, (article, start_date, end_date))
    selling_price_data = cursor.fetchall()

    date_list = [str(change_data[0]).replace(" ", "\n") for change_data in selling_price_data]
    price_list = [float(change_data[1]) for change_data in selling_price_data]

    return product_name, date_list, price_list
