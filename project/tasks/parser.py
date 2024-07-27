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
    try:
        parse_allgood_product()
    except Exception as e:
        print(f"Error in parse_allgood_product: {e}")
    
    try:
        parse_mediapark_product()
    except Exception as e:
        print(f"Error in parse_mediapark_product: {e}")
    
    try:
        parse_openshop_product()
    except Exception as e:
        print(f"Error in parse_openshop_product: {e}")
    
    try:
        parse_radius_product()
    except Exception as e:
        print(f"Error in parse_radius_product: {e}")

    try:
        parse_elmakon_product()
    except Exception as e:
        print(f"Error in parse_elmakon_product: {e}")
    
    try:
        parse_olcha_product()
    except Exception as e:
        print(f"Error in parse_olcha_product: {e}")

    try:
        parse_goodzone_product()
    except Exception as e:
        print(f"Error in parse_goodzone_product: {e}")
    
    try:
        parse_pcmarket_product()
    except Exception as e:
        print(f"Error in parse_pcmarket_product: {e}")

    try:
        parse_maxcom_product()
    except Exception as e:
        print(f"Error in parse_maxcom_product: {e}")
    
    try:
        parse_asaxiy_product()
    except Exception as e:
        print(f"Error in parse_asaxiy_product: {e}")
    
    try:
        parse_ikarvon_product()
    except Exception as e:
        print(f"Error in parse_ikarvon_product: {e}")

    try:
        parse_texnomart_product()
    except Exception as e:
        print(f"Error in parse_texnomart_product: {e}")
    