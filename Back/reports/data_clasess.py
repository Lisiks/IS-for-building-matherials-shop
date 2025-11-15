from dataclasses import dataclass
from datetime import datetime


@dataclass
class Product:
    article: str
    name: str
    product_type: str
    purchases_count: int
    purchases_summ: float
    buying_cost_list: list
    selling_cost_list: list

    def __init__(self, article, name, product_type=None, actual_buying_price=None, actual_selling_price=None):
        self.article = article
        self.name = name
        self.product_type = product_type
        self.purchases_count = 0
        self.purchases_summ = 0.0
        self.buying_cost_list = [[datetime.now().replace(microsecond=0), actual_buying_price]]
        self.selling_cost_list = [[datetime.now().replace(microsecond=0), actual_selling_price]]


@dataclass
class Type:
    name: str
    purchases_count: int
    purchases_summ: float


@dataclass
class Supplier:
    inn: str
    name: str
    purchases_count: int
    purchases_summ: float

