from app.enums import ContainerFlag
from app.controllers.utils import convert_timestamp_to_ccls_date

class BuildStuffingObject(object):
    def __init__(self,data,user_id,trans_date_time):
        self.ctrNo=data.get('container_number')
        self.ctrLifeNo=convert_timestamp_to_ccls_date(data.get('container_life')) if data.get('container_life') else None
        self.crn=data.get('crn_number',None)
        self.dtStStf=convert_timestamp_to_ccls_date(data.get('ctms_start_time')) if data.get('ctms_start_time') else None
        self.dtEndStf=convert_timestamp_to_ccls_date(data.get('ctms_end_time')) if data.get('ctms_end_time') else None
        self.crgWt=data.get('packages_weight',None)
        self.sbillNo=data.get('shipping_bill',None)
        self.dtSbill=convert_timestamp_to_ccls_date(data.get('bill_date')) if data.get('bill_date') else None
        self.commCd=data.get('commodity_code',None)
        self.commDesc=data.get('commodity_description',None)
        self.pkgCd=data.get('package_code',None)
        self.noPkgsStf=data.get('package_count',None)
        self.noPkgsDmg=int(data.get('damaged_count')) if data.get('damaged_count') else 0
        self.cnclFlg=data.get('cncl_flag',None)
        self.trnsDtTm=trans_date_time
        self.userId=user_id
        self.hsnCode=data.get('hsn_code',None)
        self.area=int(data.get('area_of_cargo')) if data.get('area_of_cargo') else 0
        self.wtStf=data.get('packages_weight',None)
        self.fromPkct=data.get('from_packet',None)
        self.toPkct=data.get('to_packet',None)
        self.whId=data.get('wh_id',None)
        self.gridNo=str(data.get('ccls_grid_locations')[0]) if data.get('ccls_grid_locations') else None
        self.crgType=data.get('cargo_type',None)
        self.fclLclFlg=ContainerFlag(int(data.get('container_flag',1))).name
        self.noSbill=data.get('no_of_bills',None)
        self.whEqptId=data.get('equipment_id',None)
        self.ctrSize=data.get('container_size',None)
        self.ctrType=data.get('container_type',None)
        self.sealNo=None
        self.dtSeal=None
        self.createdDate = data.get('created_at',None)
        self.createdBy = user_id#data.get('created_by',None)
        self.updatedDate = data.get('updated_at',None)
        self.updatedBy = user_id#data.get('updated_by',None)
        self.errorMsg=None
        self.statusFlag=None
        self.attribute1 = data.get('short',0)
        self.attribute2 = data.get('excess',0)