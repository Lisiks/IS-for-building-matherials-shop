from Back.database_connector import get_connector
from Back.Reports.calculate_date import calculate_start_end_date_from_period


def make_product_selling_price_report(period, article):
    start_date, end_date = calculate_start_end_date_from_period(period)

    connector = get_connector()
    cursor = connector.cursor()

    check_article_query = """SELECT ProductArticle, SellingPrice FROM Products WHERE ProductArticle = %s;"""
    cursor.execute(check_article_query, (article,))
    product_query_result = cursor.fetchall()

    if len(product_query_result) == 0:
        raise TypeError("Article doesnt exist")
    else:
        product_actual_sell_price = product_query_result[0][1]

    selling_price_query = """SELECT DateOfChange, OldPrice FROM ProductsSellingPriceChanges
    WHERE Products_ProductArticle = %s AND DateOfChange >= %s AND DateOfChange < %s
    ORDER BY DateOfChange;"""
    cursor.execute(selling_price_query, (article, start_date, end_date))
    selling_price_data = cursor.fetchall()

    last_selling_price = """SELECT DateOfChange, OldPrice FROM ProductsSellingPriceChanges
    WHERE Products_ProductArticle = %s AND DateOfChange >= %s
    ORDER BY DateOfChange
    LIMIT 1;"""
    cursor.execute(last_selling_price, (article, end_date))
    last_period_change = cursor.fetchall()

    date_list = [change[0] for change in selling_price_data]
    price_list = [float(change[1]) for change in selling_price_data[1:]]

    if len(last_period_change) == 0:
        price_list.append(float(product_actual_sell_price))
    else:
        price_list.append(float(last_period_change[1]))

    return date_list, price_list







