
from app.enums import JobType
from app.services.warehouse.wh_carting import WarehouseCarting
from app.services.warehouse.wh_stufffing import WarehouseStuffing
from app.services.warehouse.wh_destufffing import WarehouseDeStuffing
from app.services.warehouse.wh_delivery import WarehouseDelivery


class WarehouseJobView(object):
    def get_job_details(self,job_order,job_type,container_flag):
        result ={}
        if job_type == JobType.CARTING.value:
            result = WarehouseCarting().get_carting_details(job_order,job_type,container_flag)
        elif job_type in [JobType.STUFFING.value,JobType.DIRECT_STUFFING.value]:
            result = WarehouseStuffing().get_stuffing_details(job_order,job_type,container_flag)
            result['wh_id'] = 'wh1'
        elif job_type == JobType.DESTUFFING.value:
            result = WarehouseDeStuffing().get_destuffing_details(job_order,job_type,container_flag)
        elif job_type in [JobType.DELIVERY.value,JobType.DIRECT_DELIVERY.value]:
            result = WarehouseDelivery().get_delivery_details(job_order,job_type,container_flag)
            result['wh_id'] = 'wh2'
        else:
            pass
        result['job_type'] = job_type
        result['container_flag'] = container_flag
        return result
