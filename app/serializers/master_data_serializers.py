from app import ma
from app.models import *
from marshmallow import EXCLUDE

class WagonMasterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WgnMst
        # exclude = ("id",)
        # fields = '__all__'
        fields = ("wgn_no", "wgn_typ", "commisioned_on","ccls_wgn")
        load_instance = True
        
class GateWayPortMasterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Gwport
        # exclude = ("id",)
        # fields = '__all__'
        fields = ("gw_port_cd", "gw_port_nam")
        load_instance = True

class TrackMasterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TrackDetails
        fileds = ("track_id", "track_no")
        load_instance = True    