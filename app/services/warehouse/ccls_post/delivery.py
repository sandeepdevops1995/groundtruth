from app.enums import ContainerFlag

class BuildDeliveryObject(object):
    def __init__(self,data,user_id,trans_date_time):
        self.CTR_NO  = data.get('container_number',None)
        self.CTR_LIFE_NO  = data.get('container_life',None)
        self.BOE_NO  = data.get('bill_of_entry',None)
        self.DT_BOE  = data.get('bill_date',None)
        self.COMM_CD  = data.get('commodity_code',None)
        self.COMM_DESC  = data.get('commodity_description',None)
        self.PKG_CD  = data.get('package_code',None)
        self.NO_PKGS_LDD  = data.get('package_count',None)
        self.NO_PKGS_DMG  = data.get('damaged_count',None)
        self.CNCL_FLG   = data.get('cncl_flag',None)
        self.TRNS_DT_TM  = trans_date_time
        self.USER_ID  = user_id
        # self.BL_NO  = None
        # self.DT_BL  = None
        self.AREA  = data.get('area_of_cargo',None)
        self.COMM_AREA_DMG  = data.get('area_of_damaged_cargo',None)
        self.FCL_LCL_FLG  = ContainerFlag(int(data.get('container_flag',1))).name
        self.SLINE_CD  = data.get('sline_code',None)
        self.HNDG_CD  = data.get('handling_code',None)
        self.GRID_NO  = data.get('ccls_grid_locations',None)
        self.CRG_TYPE  = data.get('cargo_type',None)
        self.CTR_SIZE  = data.get('container_size',None)
        self.CTR_TYPE  = data.get('container_type',None)
        self.ICD_LOC_CD  = data.get('icd_location_code',None)
        self.PVT_CNCR_FLG  = data.get('private_or_concor_labour_flag',None)
        self.FULL_PART_FLG  = None
        self.GP_NO  = data.get('gpm_number',None)
        self.DT_ST_LDG  = data.get('start_time',None)
        self.DT_END_LDG  = data.get('end_time',None)
        self.VEH_NO  = data.get('truck_number',None)

        
