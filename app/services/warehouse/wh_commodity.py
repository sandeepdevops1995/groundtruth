
from app.services.warehouse.database_service import WarehouseDB


class WarehouseCommodityView(object):
    
    def get_commodity_details(self):
        result = WarehouseDB().get_commodities()
        return result
    
    def process_commodity_details(self,commodity_data):
        print("commodity_data--------",commodity_data)
        WarehouseDB().save_commodities(commodity_data)
