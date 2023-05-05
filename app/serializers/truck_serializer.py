from marshmallow import pre_load
from app import ma
from app.models.warehouse.truck import TruckDetails
from datetime import datetime
from app.controllers.utils import convert_ccls_date_to_timestamp

class TruckInsertSchema(ma.SQLAlchemyAutoSchema):

    @pre_load()
    def change_data(self, data, **kwargs):
        if data['truck_arrival_date'] and isinstance(data['truck_arrival_date'], datetime):
                data['truck_arrival_date']=convert_ccls_date_to_timestamp(data['truck_arrival_date'])
        return data
    
    class Meta:
        model = TruckDetails
        fields = ("truck_number", "truck_arrival_date", "created_at")
        include_relationships = True
        load_instance = True
        # unknown = INCLUDE
        # exclude = ("master_job_order",)

    job_order_id = ma.auto_field("master_job_order_truck")