from marshmallow import fields
from app import ma
from app.models.master.warehouse import Commodity as WarehouseCommodity

class CCLSCommodityList(ma.SQLAlchemyAutoSchema):
    comm_cd = fields.String(data_key='commodity_code')
    comm_desc = fields.String(data_key='commodity_description')
    class Meta:
        model = WarehouseCommodity
        fields = ("comm_cd",'comm_desc')     