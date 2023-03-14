
from app.services.warehouse.database_service import WarehouseDB


class WarehouseCommodityView(object):
    def get_commodity_details(self):
        result = WarehouseDB().get_commodities()
        return result
