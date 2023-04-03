from app.enums import ContainerFlag

class BuildStuffingObject(object):
    def __init__(self,data):
        self.ctrNo=data.get('container_number',None)
        self.ctrLifeNo=data.get('container_life',None)
        self.crn=data.get('crn_number',None)
        self.dtStStf=data.get('start_time',None)
        self.dtEndStf=data.get('end_time',None)
        self.crgWt=data.get('packages_weight',None)
        self.sbillNo=data.get('shipping_bill',None)
        self.dtSbill=data.get('bill_date',None)
        self.commCd=data.get('commodity_code',None)
        self.commDesc=data.get('commodity_description',None)
        self.pkgCd=data.get('package_code',None)
        self.noPkgsStf=data.get('package_count',None)
        self.noPkgsDmg=data.get('damaged_count',None)
        self.cnclFlg=data.get('cncl_flag',None)
        self.trnsDtTm=data.get('trans_date_time',None)
        self.userId=data.get('user_id',None)
        self.hsnCode=data.get('hsn_code',None)
        self.area=data.get('area_of_cargo',None)
        self.wtStf=data.get('packages_weight',None)
        self.fromPkct=data.get('from_packet',None)
        self.toPkct=data.get('to_packet',None)
        self.whId=data.get('wh_id',None)
        self.gridNo=data.get('grid_locations',None)
        self.crgType=data.get('cargo_type',None)
        self.fclLclFlg=ContainerFlag(int(data.get('container_flag',1))).name
        self.noSbill=data.get('no_of_bills',None)
        self.whEqptId=data.get('equipment_id',None)
        self.ctrSize=data.get('container_size',None)
        self.ctrType=data.get('container_type',None)
        self.sealNo=None
        self.dtSeal=None
        self.createdDate=None
        self.createdBy=None
        self.updatedDate=None
        self.updatedBy=None
        self.errorMsg=None
        self.statusFlag=None

        
