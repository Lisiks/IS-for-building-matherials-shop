from Back.database_connector import get_connector
from Back.Reports.calculate_date import calculate_start_end_date_from_period


def make_product_selling_price_report(period, article):
    start_date, end_date = calculate_start_end_date_from_period(period)

    connector = get_connector()
    cursor = connector.cursor()

    check_article_query = """SELECT * FROM Products WHERE ProductArticle = %s;"""
    cursor.execute(check_article_query, (article,))
    product_query_result = cursor.fetchall()

    if len(product_query_result) == 0:
        raise TypeError("Article doesnt exist")

    selling_price_query = """SELECT DateOfChange, NewPrice FROM ProductsSellingPriceChanges
    WHERE Products_ProductArticle = %s AND DateOfChange >= %s AND DateOfChange < %s
    ORDER BY DateOfChange;"""
    cursor.execute(selling_price_query, (article, start_date, end_date))
    selling_price_data = cursor.fetchall()

    date_list = [str(change_data[0]).replace(" ", "\n") for change_data in selling_price_data]
    price_list = [float(change_data[1]) for change_data in selling_price_data]

    return date_list, price_list
