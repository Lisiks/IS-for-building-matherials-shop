from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    article: str
    name: str
    product_type: str
    purchase_count: int
    purchase_summ: float
    sales_count: int
    sales_summ: float
    profit: float
    buying_cost_list: list
    selling_cost_list: list

    def __init__(self, article, name, product_type=None, actual_buying_price=None, actual_selling_price=None):
        self.article = article
        self.name = name
        self.product_type = product_type
        self.purchase_count = 0
        self.purchase_summ = 0.0
        self.sales_count = 0
        self.sales_summ = 0.0
        self.profit = 0.0

        self.buying_cost_list = [[datetime.now().replace(microsecond=0), actual_buying_price]]
        self.selling_cost_list = [[datetime.now().replace(microsecond=0), actual_selling_price]]


@dataclass
class Type:
    name: str
    purchases_count: int
    purchases_summ: float
    sales_count: int
    sales_summ: float
    profit: float


@dataclass
class Supplier:
    inn: str
    name: str
    purchases_count: int
    purchases_summ: float


@dataclass
class Client:
    card_number: str
    full_name: str
    sales_count: int
    sales_summ: float
    profit: float


