from .maxcom import parse_maxcom_product
from .pcmarket import parse_pcmarket_product
from .ikarvon import parse_ikarvon_product
from .asaxiy import parse_asaxiy_product
from .texnomart import parse_texnomart_product
from .allgood import parse_allgood_product
from .mediapark import parse_mediapark_product
from .openshop import parse_openshop_product
from .radius import parse_radius_product
from .elmakon import parse_elmakon_product
from .olcha import parse_olcha_product
from .goodzone import parse_goodzone_product


def parse_and_save():
    parse_texnomart_product()
    parse_allgood_product()    
    parse_mediapark_product()
    parse_openshop_product()
    parse_radius_product()
    parse_elmakon_product()
    parse_olcha_product()
    parse_goodzone_product()
    parse_pcmarket_product()
    parse_maxcom_product()
    parse_asaxiy_product()
    parse_ikarvon_product()