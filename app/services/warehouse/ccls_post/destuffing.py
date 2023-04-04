from app.enums import ContainerFlag

class BuildDeStuffingObject(object):
 
    def __init__(self,data):
        self.ctrNo=data.get('container_number',None)
        self.ctrLifeNo=data.get('container_life',None)
        self.boeNo=data.get('bill_of_entry',None)
        self.dtBoe=data.get('bill_date',None)
        self.commCd=data.get('commodity_code',None)
        self.commDesc=data.get('commodity_description',None)
        self.pkgCd=data.get('package_code',None)
        self.commPkgsDstf=data.get('package_count',None)
        self.commPkgsDmg=data.get('damaged_count',None)
        self.commWtDstf=data.get('packages_weight',None)
        self.commWtDmg=data.get('damaged_packages_weight',None)
        self.hldRlsFlg=data.get('hld_rls_flag',None)
        self.cnclFlg=data.get('cncl_flag',None)
        self.trnsDtTm=data.get('trans_date_time',None)
        self.userId=data.get('user_id',None)
        self.blNo=data.get('bill_of_lading',None)
        self.dtBl=data.get('bill_date',None)
        self.area=data.get('area_of_cargo',None)
        self.commAreaDmg=data.get('area_of_damaged_cargo',None)
        self.fclLclFlg=ContainerFlag(int(data.get('container_flag',1))).name
        self.dstfStDt=data.get('start_time',None)
        self.dstfEndDt=data.get('end_time',None)
        self.slineCd=data.get('sline_code',None)
        self.hndgCd=data.get('handling_code',None)
        self.gridNo=data.get('grid_locations',None)
        self.crgType=data.get('cargo_type',None)
        self.ctrSize=data.get('container_size',None)
        self.ctrType=data.get('container_type',None)
        self.dtDstfpln=data.get('destuffing_plan_date',None)
        self.noBols=data.get('no_of_bills',None)
        self.icdLocCd=data.get('icd_location_code',None)
        self.pvtCncrFlg=data.get('private_or_concor_labour_flag',None)
        self.fullPartFlg=None
        self.vehNo=data.get('truck_number',None)
        self.createdDate=None
        self.createdBy=None
        self.updatedDate=None
        self.updatedBy=None
        self.errorMsg=None
        self.statusFlag=None

        
