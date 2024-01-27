from enum import Enum

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM

from db.database import Base


class Websites(Enum):
    texnomart = "texnomart"
    mediapark = "mediapark"
    olcha = "olcha"
    asaxiy = "asaxiy"
    openshop = "openshop"
    elmakon = "elmakon"
    discount = "discount"
    allgood = "allgood"
    goodzone = "goodzone"
    radius = "radius"
    zon = "zon"
    ikarvon = "ikarvon"
    eSavdo = "eSavdo"
    idea = "idea"
    mytech = "mytech"
    royaltech = "royaltech"
    elso = "elso"
    mago = "mago"
    macbro = "macbro"
    azbo = "azbo"
    maxcom = "maxcom"
    openshop_uz = "openshop_uz"
    brandstore = "brandstore"
    ultrashop = "ultrashop"
    gshop = "gshop"
    mycom = "mycom"
    pcmarket = "pcmarket"
    bozon = "bozon"
    mionline = "mionline"
    treetech = "treetech"


class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    url = Column(String)
    website = Column(ENUM(Websites), default=Websites.texnomart)
