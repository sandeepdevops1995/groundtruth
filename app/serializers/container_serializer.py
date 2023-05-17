from marshmallow import pre_load
from app import ma
from app.models.warehouse.container import Container
from datetime import datetime
from app.controllers.utils import convert_ccls_date_to_timestamp

class ContainerInsertSchema(ma.SQLAlchemyAutoSchema):
    @pre_load()
    def change_data(self, data, **kwargs):
        if data['container_life'] and isinstance(data['container_life'], datetime):
                data['container_life']=convert_ccls_date_to_timestamp(data['container_life'])
        return data
    class Meta:
        model = Container
        fields = ("container_number", "container_type", "container_size", "container_iso_code", "container_location_code", "container_life", "created_at")
        include_relationships = False
        load_instance = True
        # unknown = INCLUDE
        # exclude = ("master_job_order",)


class ContainerUpdateSchema(ma.SQLAlchemyAutoSchema):
    @pre_load()
    def change_data(self, data, **kwargs):
        if data['container_life'] and isinstance(data['container_life'], datetime):
                data['container_life']=convert_ccls_date_to_timestamp(data['container_life'])
        return data
    class Meta:
        model = Container
        fields = ("id","container_number", "container_type", "container_size", "container_iso_code", "container_location_code", "container_life", "created_at")
        include_relationships = False
        load_instance = True
        # unknown = INCLUDE
        # exclude = ("master_job_order",)