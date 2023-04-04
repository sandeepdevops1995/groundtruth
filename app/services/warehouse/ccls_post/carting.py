from app.enums import ContainerFlag

class BuildCartingObject(object):
    def __init__(self,data,user_id,trans_date_time):
        self.ctrNo = data.get('container_number',None)
        self.ctrLifeNo = data.get('container_life',None)
        self.crn = data.get('crn_number',None)
        self.dtStUnldg = data.get('start_time',None)
        self.dtEndUnldg = data.get('end_time',None)
        self.sbillNo = data.get('shipping_bill',None)
        self.dtSbill = data.get('bill_date',None)
        self.commCd = data.get('commodity_code',None)
        self.pkgCd = data.get('package_code',None)
        self.noPkgsUnldd = data.get('package_count',None)
        self.noPkgsDmg = data.get('damaged_count',None)
        self.crgCrdFlg = None
        self.vehNo = data.get('truck_number',None)
        self.cnclFlg = data.get('cncl_flag',None)
        self.trnsDtTm = trans_date_time
        self.userId = user_id
        self.area = data.get('area_of_cargo',None)
        self.whId = data.get('wh_id',None)
        self.gridNo = data.get('ccls_grid_locations',None)
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
        
