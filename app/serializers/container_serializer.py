from marshmallow import pre_load
from app import ma
from app.models.warehouse.container import Container
from app import postgres_db as db
from sqlalchemy import func, Integer
from sqlalchemy.sql.expression import cast

class ContainerInsertSchema(ma.SQLAlchemyAutoSchema):
    @pre_load()
    def change_data(self, data, **kwargs):
        max_val = db.session.query(func.max(cast(Container.id, Integer))).scalar()
        if max_val:
            data['id'] = str(max_val+1)
        else:
            data['id'] = "1"
        return data
    class Meta:
        model = Container
        fields = ("id","container_number", "container_type", "container_size", "container_iso_code", "container_location_code", "container_life", "created_at")
        include_relationships = False
        load_instance = True


class ContainerUpdateSchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = Container
        fields = ("id","container_number", "container_type", "container_size", "container_iso_code", "container_location_code", "container_life", "created_at")
        include_relationships = False
        load_instance = True