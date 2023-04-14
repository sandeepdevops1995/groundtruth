
from app.enums import JobType,JobOrderType
from app.services.warehouse.wh_carting import WarehouseCarting
from app.services.warehouse.wh_stufffing import WarehouseStuffing
from app.services.warehouse.wh_destufffing import WarehouseDeStuffing
from app.services.warehouse.wh_delivery import WarehouseDelivery


class WarehouseJobView(object):
    def get_job_details(self,job_order,job_type,container_flag):
        result ={}
        if job_type in [JobOrderType.CARTING_FCL.value,JobOrderType.CARTING_LCL.value]:
            result = WarehouseCarting().get_carting_details(job_order,job_type)
        elif job_type in [JobOrderType.STUFFING_FCL.value,JobOrderType.STUFFING_LCL.value,JobOrderType.DIRECT_STUFFING.value]:
            result = WarehouseStuffing().get_stuffing_details(job_order,job_type)
        elif job_type in [JobOrderType.DE_STUFFING_FCL.value,JobOrderType.DE_STUFFING_LCL.value]:
            result = WarehouseDeStuffing().get_destuffing_details(job_order,job_type)
        elif job_type in [JobOrderType.DELIVERY_FCL.value,JobOrderType.DELIVERY_LCL.value,JobOrderType.DIRECT_DELIVERY.value]:
            result = WarehouseDelivery().get_delivery_details(job_order,job_type)
        else:
            pass
        # result['wh_id'] = 'wh2'
        # result['job_type'] = job_type
        result['container_flag'] = container_flag
        return result
