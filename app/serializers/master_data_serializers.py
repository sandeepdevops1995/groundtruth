from app import ma
from app.models import *
from marshmallow import EXCLUDE

class WagonMasterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WgnMst
        fields = ("wgn_no", "wgn_typ", "commisioned_on","ccls_wgn")
        load_instance = True
        
class GateWayPortMasterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Gwport
        fields = ("gw_port_cd", "gw_port_nam")
        load_instance = True