from marshmallow import fields
from app import ma
from app.models.warehouse.truck import TruckDetails

class TruckInsertSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = TruckDetails
        fields = ("truck_number", "truck_arrival_date", "created_at")
        include_relationships = True
        load_instance = True
        # unknown = INCLUDE
        # exclude = ("master_job_order",)

    job_order_id = ma.auto_field("master_job_order_truck")