from .maxcom import parse_maxcom_product
from .pcmarket import parse_pcmarket_product
from .ikarvon import parse_ikarvon_product
from .asaxiy import parse_asaxiy_product


def parse_and_save():
    parse_ikarvon_product()
    parse_pcmarket_product()
    parse_maxcom_product()
    parse_asaxiy_product()