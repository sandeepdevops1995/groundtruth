from app.enums import ContainerFlag
from app.controllers.utils import convert_timestamp_to_ccls_date

class BuildCartingObject(object):
    def __init__(self,data,user_id,trans_date_time):
        self.ctrNo = self.ctrNo = "ABCD1234567" if data.get('container_number') is None else data.get('container_number')
        self.ctrLifeNo = convert_timestamp_to_ccls_date(data.get('container_life')) if data.get('container_life') else None
        self.crn = data.get('crn_number',None)
        self.dtStUnldg = convert_timestamp_to_ccls_date(data.get('start_time')) if data.get('start_time') else None
        self.dtEndUnldg =  convert_timestamp_to_ccls_date(data.get('end_time')) if data.get('end_time') else None
        self.sbillNo = data.get('shipping_bill',None)
        self.dtSbill = convert_timestamp_to_ccls_date(data.get('bill_date')) if data.get('bill_date') else None
        self.commCd = data.get('commodity_code',None)
        self.pkgCd = data.get('package_code',None)
        self.noPkgsUnldd = data.get('package_count',None)
        self.noPkgsDmg = int(data.get('damaged_count')) if data.get('damaged_count') else 0
        self.crgCrdFlg = None
        self.vehNo = data.get('truck_number',None)
        self.cnclFlg = data.get('cncl_flag',None)
        self.trnsDtTm = trans_date_time
        self.userId = user_id
        self.area = int(data.get('area_of_cargo')) if data.get('area_of_cargo') else 0
        self.whId = data.get('wh_id',None)
        self.gridNo = str(data.get('ccls_grid_locations')[0]) if data.get('ccls_grid_locations') else None
        self.crgType = data.get('cargo_type',None)
        self.ctrSize = data.get('container_size',None)
        self.ctrType = data.get('container_type',None)
        self.fclLclFlg = ContainerFlag(int(data.get('container_flag',1))).name
        self.pvtCncrFlg = data.get('private_or_concor_labour_flag',None)
        self.icdLocCd = data.get('icd_location_code',None)
        self.createdDate = None
        self.createdBy = None
        self.updatedDate = None
        self.updatedBy = None
        self.errorMsg = None
        self.statusFlag = None