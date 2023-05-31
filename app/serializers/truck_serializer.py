from app import ma
from app.models.warehouse.truck import TruckDetails

class TruckInsertSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = TruckDetails
        fields = ("truck_number", "truck_arrival_date", "created_at")
        include_relationships = True
        load_instance = True

    job_order_id = ma.auto_field("master_job_order_truck")


class TruckUpdateSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = TruckDetails
        fields = ("id","truck_number", "truck_arrival_date", "created_at","job_order_id")
        load_instance = True

class GETTruckDetailsSchema(ma.SQLAlchemyAutoSchema):
    
    class Meta:
        model = TruckDetails
        fields = ("truck_number", "truck_arrival_date")