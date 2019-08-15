from schematics.models import Model
from schematics.types import (
    BaseType,
    NumberType,
    DateTimeType,
    FloatType,
    DecimalType,
    StringType,
    ModelType,
    ListType,
)


class EmitterModel(Model):
    name = StringType(required=True)
    cnpj = NumberType(required=True)
    uf = StringType(max_length=2, required=True)
    fantasy_name = StringType()
    state_reg = NumberType()
    address = StringType()
    district = StringType()
    zipcode = NumberType()
    city_code = StringType()
    city_name = StringType()


class ProductModel(Model):
    description = StringType()
    quantity = FloatType()
    business_unity = StringType()
    total_value = FloatType()
    unit_value = FloatType()
    product_code = StringType()
    ncm_code = StringType()
    cfop = StringType()
    total_tax = FloatType()
    metadata = BaseType()


class NFeModel(Model):
    access_key = NumberType(required=True)
    number = NumberType(required=True)
    datetime = DateTimeType(required=True)
    total_value = DecimalType(required=True)
    protocol = NumberType()
    emitter = ModelType(EmitterModel)
    products = ListType(ModelType(ProductModel))
