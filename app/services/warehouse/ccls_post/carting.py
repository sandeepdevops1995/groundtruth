from app.enums import ContainerFlag
from app.controllers.utils import convert_timestamp_to_ccls_date
import time

class BuildCartingObject(object):
    def __init__(self,data,user_id,trans_date_time):
        self.ctrNo = data.get('container_number')[0] if data.get('container_number') else "ABCD1234567"
        self.ctrLifeNo = convert_timestamp_to_ccls_date(data.get('container_life')) if data.get('container_life') else convert_timestamp_to_ccls_date(int(time.time())*1000)
        self.crn = data.get('crn_number') if data.get('crn_number') else data.get('cargo_carting_number',None)
        self.dtStUnldg = convert_timestamp_to_ccls_date(data.get('ctms_start_time')) if data.get('ctms_start_time') else None
        self.dtEndUnldg =  convert_timestamp_to_ccls_date(data.get('ctms_end_time')) if data.get('ctms_end_time') else None
        self.sbillNo = data.get('shipping_bill',None)
        self.dtSbill = convert_timestamp_to_ccls_date(data.get('bill_date')) if data.get('bill_date') else None
        self.commCd = data.get('commodity_code',None)
        self.pkgCd = data.get('package_code',None)
        self.noPkgsUnldd = data.get('package_count',None)
        self.noPkgsDmg = int(data.get('damaged_count')) if data.get('damaged_count') else 0
        self.crgCrdFlg = data.get('is_cargo_card_generated',None)
        self.vehNo = data.get('truck_number',None)
        self.cnclFlg = data.get('cncl_flag',None)
        self.trnsDtTm = trans_date_time
        self.userId = user_id
        self.area = int(data.get('area_of_cargo')) if data.get('area_of_cargo') else 0
        self.whId = data.get('wh_id',None)
        self.gridNo = str(data.get('ccls_grid_locations')[0]) if data.get('ccls_grid_locations') else None
        self.crgType = data.get('cargo_type',None)
        self.ctrSize = data.get('container_size')[0] if data.get('container_size') else ""
        self.ctrType = data.get('container_type',None)
        self.fclLclFlg = ContainerFlag(int(data.get('container_flag',1))).name
        self.pvtCncrFlg = data.get('private_or_concor_labour_flag',None)
        self.icdLocCd = data.get('icd_location_code',None)
        self.fullPartFlg=data.get('full_or_part_flag',None)
        self.createdDate = data.get('created_at',None)
        self.createdBy = user_id#data.get('created_by',None)
        self.updatedDate = data.get('updated_at',None)
        self.updatedBy = user_id#data.get('updated_by',None)
        self.errorMsg = None
        self.statusFlag = None
        self.attribute1 = data.get('short',0)
        self.attribute2 = data.get('excessPkg',0)
        self.attribute3 = data.get('full_or_part_flag',None)