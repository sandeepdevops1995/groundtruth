from app.enums import ContainerFlag
from app.controllers.utils import convert_timestamp_to_ccls_date

class BuildDeliveryObject(object):
    def __init__(self,data,user_id,trans_date_time):
        self.ctrNo=data.get('container_number')
        self.ctrLifeNo=convert_timestamp_to_ccls_date(data.get('container_life')) if data.get('container_life') else None
        self.boeNo=data.get('bill_of_entry',None)
        self.dtBoe=convert_timestamp_to_ccls_date(data.get('bill_date')) if data.get('bill_date') else None
        self.commCd=data.get('commodity_code',None)
        self.commDesc=data.get('commodity_description',None)
        self.pkgCd=data.get('package_code',None)
        self.noPkgsLdd=data.get('package_count',0)
        self.noPkgsDmg=int(data.get('damaged_count')) if data.get('damaged_count') else 0
        self.cnclFlg=data.get('cncl_flag',None)
        self.trnsDtTm=trans_date_time
        self.userId=user_id
        self.blNo=data.get('bill_of_lading',None)
        self.dtBl=convert_timestamp_to_ccls_date(data.get('bol_date')) if data.get('bol_date') else None
        self.area=int(data.get('area_of_cargo')) if data.get('area_of_cargo') else 0
        self.commAreaDmg=int(data.get('area_of_damaged_cargo')) if data.get('area_of_damaged_cargo') else 0
        self.fclLclFlg=ContainerFlag(int(data.get('container_flag',1))).name
        self.slineCd=data.get('sline_code',None)
        self.hndgCd=data.get('handling_code',None)
        self.gridNo=str(data.get('ccls_grid_locations')[0]) if data.get('ccls_grid_locations') else None
        self.crgType=data.get('cargo_type',None)
        self.ctrSize=data.get('container_size',None)
        self.ctrType=data.get('container_type',None)
        self.icdLocCd=data.get('icd_location_code',None)
        self.pvtCncrFlg=data.get('private_or_concor_labour_flag',None)
        self.fullPartFlg=data.get('full_or_part_flag',None)
        self.gpNo=data.get('gpm_number',None)
        self.dtStLdg=convert_timestamp_to_ccls_date(data.get('ctms_start_time')) if data.get('ctms_start_time') else None
        self.dtEndLdg=convert_timestamp_to_ccls_date(data.get('ctms_end_time')) if data.get('ctms_end_time') else None
        self.vehNo=data.get('truck_number',None)
        self.createdDate = data.get('created_at',None)
        self.createdBy = data.get('created_by',None)
        self.updatedDate = data.get('updated_at',None)
        self.updatedBy = data.get('updated_by',None)
        self.errorMsg=None
        self.statusFlag=None