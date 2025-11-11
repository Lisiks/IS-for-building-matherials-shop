from Back.database_connector import get_connector
from datetime import datetime
import json


def get_organization_name():
    with open("JSON/organization_data.json", "r") as org_data_file:
        org_data = json.loads(json.load(org_data_file))

    return org_data["organization_name"]


def get_month_purchases_sales_count():
    connector = get_connector()
    cursor = connector.cursor()

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

    get_count_query = """SELECT count(*) FROM Purchases WHERE PurchaseDate >= %s AND PurchaseDate < %s;"""
    cursor.execute(get_count_query, (start_date, end_date))

    purchases_count = cursor.fetchall()[0][0]

    get_count_query = """SELECT count(*) FROM Sales WHERE SaleDate >= %s AND SaleDate < %s;"""
    cursor.execute(get_count_query, (start_date, end_date))

    sales_count = cursor.fetchall()[0][0]

    connector.close()
    return purchases_count, sales_count
