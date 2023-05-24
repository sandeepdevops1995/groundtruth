from marshmallow import pre_load
from app import ma
from app.models.warehouse.container import Container
from datetime import datetime
from app.controllers.utils import convert_ccls_date_to_timestamp
from app import postgres_db as db
from sqlalchemy import func, Integer
from sqlalchemy.sql.expression import cast

class ContainerInsertSchema(ma.SQLAlchemyAutoSchema):
    @pre_load()
    def change_data(self, data, **kwargs):
        try:
            max_val = db.session.query(func.max(cast(Container.id, Integer))).scalar()
            data['id'] = str(max_val+1)
        except:
             data['id'] = 1
        if data['container_life'] and isinstance(data['container_life'], datetime):
                data['container_life']=convert_ccls_date_to_timestamp(data['container_life'])
        return data
    class Meta:
        model = Container
        fields = ("id","container_number", "container_type", "container_size", "container_iso_code", "container_location_code", "container_life", "created_at")
        include_relationships = False
        load_instance = True


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