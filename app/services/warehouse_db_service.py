import config
import requests
import json
from app.logger import logger
import pandas as pd


class WarehouseDbService:

    def save_warehouse(self,j_data):
        # crud_obj.insert(j_data,Constants.WAREHOUSE_TABLE_NAME,objects="one")
        pass

    def get_warehouse_details(self,job_order):
        response ={}
        # if Constants.IS_EVENT_BASED:
        #     result = self.get_warehouse_details_by_bill_number(bill_number)
        #     # print(result)
        #     return result
        # else:
        response = requests.get(config.CLIENT_WAREHOUSE_GROUND_TRUTH_END_POINT+"/"+job_order)
        print("response:", type(response), response._content)
        if response.status_code == 200:
            WarehouseDbService().save_warehouse_details(response.json())
            return response.json()
        else:
            return

    def get_warehouse_file_data(self,file_obj):
        dframe = pd.read_excel(file_obj, engine='openpyxl')
        data = dframe.to_json(orient = "records" )
        j_data = json.loads(data)
        return j_data

    def save_warehouse_details(self,warehouse_data):
        self.save_warehouse(warehouse_data)
        logger.info('Captured warehouse Excel Data and Saved In Data Base')
        return
