from marshmallow import fields
from app import ma
from app.models.warehouse.container import Container

class ContainerInsertSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Container
        fields = ("container_number", "container_type", "container_size", "container_iso_code", "container_location_code", "container_life", "created_at")
        include_relationships = False
        load_instance = True
        # unknown = INCLUDE
        # exclude = ("master_job_order",)