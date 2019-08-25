from schematics.models import Model
from schematics.types import (
    BaseType,
    DateTimeType,
    FloatType,
    ListType,
    ModelType,
    IntType,
    StringType,
)


class EmitterModel(Model):
    name = StringType(required=True)
    cnpj = IntType(required=True)
    uf = StringType(max_length=2, required=True)
    fantasy_name = StringType()
    state_reg = IntType()
    address = StringType()
    district = StringType()
    zipcode = IntType()
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
    access_key = StringType(required=True)
    number = StringType(required=True)
    issue_date = DateTimeType(required=True)
    total_value = FloatType(required=True)
    protocol = StringType()
    emitter = ModelType(EmitterModel)
    products = ListType(ModelType(ProductModel))
