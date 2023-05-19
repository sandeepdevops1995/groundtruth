
from app.enums import JobType,JobOrderType
from app.services.warehouse.wh_carting import WarehouseCarting
from app.services.warehouse.wh_stufffing import WarehouseStuffing
from app.services.warehouse.wh_destufffing import WarehouseDeStuffing
from app.services.warehouse.wh_delivery import WarehouseDelivery
import app.services.warehouse.constants as constants


class WarehouseJobView(object):
    def get_job_details(self,job_order,job_type,container_flag):
        result ={}
        if job_type == JobOrderType.CARTING_FCL.value:
            result = WarehouseCarting().get_carting_details(job_order,job_type,constants.KEY_CARTING_FCL_SERVICE_TYPE,constants.KEY_CARTING_FCL_SERVICE_NAME,constants.KEY_CARTING_FCL_PORT_NAME)
        elif job_type == JobOrderType.CARTING_LCL.value:
            result = WarehouseCarting().get_carting_details(job_order,job_type,constants.KEY_CARTING_LCL_SERVICE_TYPE,constants.KEY_CARTING_LCL_SERVICE_NAME,constants.KEY_CARTING_LCL_PORT_NAME)
        elif job_type == JobOrderType.STUFFING_FCL.value:
            result = WarehouseStuffing().get_stuffing_details(job_order,job_type,constants.KEY_STUFFING_FCL_SERVICE_TYPE,constants.KEY_STUFFING_FCL_SERVICE_NAME,constants.KEY_STUFFING_FCL_PORT_NAME)
        elif job_type == JobOrderType.STUFFING_LCL.value:
            result = WarehouseStuffing().get_stuffing_details(job_order,job_type,constants.KEY_STUFFING_LCL_SERVICE_TYPE,constants.KEY_STUFFING_LCL_SERVICE_NAME,constants.KEY_STUFFING_LCL_PORT_NAME)
        elif job_type == JobOrderType.DIRECT_STUFFING.value:
            result = WarehouseStuffing().get_stuffing_details(job_order,job_type,constants.KEY_STUFFING_FCL_SERVICE_TYPE,constants.KEY_STUFFING_FCL_SERVICE_NAME,constants.KEY_STUFFING_FCL_PORT_NAME)
        elif job_type == JobOrderType.DE_STUFFING_FCL.value:
            result = WarehouseDeStuffing().get_destuffing_details(job_order,job_type,constants.KEY_DESTUFFING_FCL_SERVICE_TYPE,constants.KEY_DESTUFFING_FCL_SERVICE_NAME,constants.KEY_DESTUFFING_FCL_PORT_NAME)
        elif job_type == JobOrderType.DE_STUFFING_LCL.value:
            result = WarehouseDeStuffing().get_destuffing_details(job_order,job_type,constants.KEY_DESTUFFING_LCL_SERVICE_TYPE,constants.KEY_DESTUFFING_LCL_SERVICE_NAME,constants.KEY_DESTUFFING_LCL_PORT_NAME)
        elif job_type == JobOrderType.DELIVERY_FCL.value:
            result = WarehouseDelivery().get_delivery_details(job_order,job_type,constants.KEY_DELIVERY_FCL_SERVICE_TYPE,constants.KEY_DELIVERY_FCL_SERVICE_NAME,constants.KEY_DELIVERY_FCL_PORT_NAME)
        elif job_type == JobOrderType.DELIVERY_LCL.value:
            result = WarehouseDelivery().get_delivery_details(job_order,job_type,constants.KEY_DELIVERY_LCL_SERVICE_TYPE,constants.KEY_DELIVERY_LCL_SERVICE_NAME,constants.KEY_DELIVERY_LCL_PORT_NAME)
        elif job_type == JobOrderType.DIRECT_DELIVERY.value:
            result = WarehouseDelivery().get_delivery_details(job_order,job_type,constants.KEY_DELIVERY_FCL_SERVICE_TYPE,constants.KEY_DELIVERY_FCL_SERVICE_NAME,constants.KEY_DELIVERY_FCL_PORT_NAME)
        else:
            pass
        result['container_flag'] = container_flag
        return result
