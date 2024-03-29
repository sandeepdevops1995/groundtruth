##  ccls job order keys
CCLS_CON_DATE='con_date'
CCLS_CRN_DATE='crn_date'
CCLS_SHIPPING_LINER_CODE='shipping_liner_code'
CCLS_PARTY_CODE='party_code'
CCLS_CHA_CODE='cha_code'
CCLS_GW_PORT_CODE='gw_port_code'
CCLS_GROSS_WEIGHT='gross_weight'
CCLS_GPM_NUMBER='gpm_number'
CCLS_GPM_CREATED_DATE='gpm_created_date'
CCLS_GPM_VALIDATE_DATE='gpm_valid_date'
CCLS_CON_NUMBER='carting_order_number'
CCLS_CRN_NUMBER='crn_number'
CCLS_CARGO_WEIGHT_IN_CRN='cargo_weight_in_crn'
CCLS_WEIGHT_REMAINING='weight_remaining'
CCLS_STUFFING_JOB_ORDER='stuffing_job_order'
CCLS_DESTUFFING_JOB_ORDER='destuffing_job_order'
CCLS_PRIVATE_OR_CONCOR_LABOUR_FLAG='private_or_concor_labour_flag'
CCLS_HANDLING_CODE='handling_code'
CCLS_ICD_LOCATION_CODE='icd_location_code'
CCLS_IS_CARGO_CARD_GENERATED='is_cargo_card_generated'
CCLS_REVERSE_FLAG='reserve_flag'
CCLS_CARGO_TYPE='cargo_type'
CCLS_CANCEL_FLAG='cncl_flag'
CCLS_HSN_CODE='hsn_code'
CCLS_DESTUFFING_PLAN_DATE='destuffing_plan_date'
CCLS_HOLD_RELEASE_FLAG='hld_rls_flag'
CCLS_GP_STAT='gp_stat'
CCLS_ORDER_NO='Order_Number'

## ccls bill detail keys
CCLS_COMMODITY_ID='commodity_id'
CCLS_BILL_OF_ENTRY_NUMBER='boe_number'
CCLS_BILL_OF_LADEN_NUMBER='bol_number'
CCLS_BILL_DATE='bill_date'
CCLS_SHIPPING_BILL_DATE='shipping_bill_date'
CCLS_IMPORTER_CODE='importer_code'
CCLS_IMPORTER_NAME='importer_name'
CCLS_PACKAGE_CODE='package_code'
CCLS_NO_OF_PACKAGES_DECLARED='no_of_packages_declared'
CCLS_PACKAGE_WEIGHT='package_weight'
CCLS_JOB_ORDER_ID='job_order_id'
CCLS_SHIPPING_BILL_NUMBER='shipping_bill_number'
CCLS_BOL_DATE='bol_date'

## ccls commodity keys
CCLS_COMMODITY_CODE='commodity_code'
CCLS_COMMODITY_DESCRIPTION='commodity_description'

## ccls container keys
CCLS_CONTAINER_NUMBER = 'container_number'
CCLS_CONTAINER_TYPE = 'container_type'
CCLS_CONTAINER_SIZE = 'container_size'
CCLS_CONTAINER_ISO_CODE = 'container_iso_code'
CCLS_CONTAINER_LOCATION_CODE = 'container_location_code'
CCLS_CONTAINER_LIFE = 'container_life'


BACKEND_CON_NUMBER = 'carting_order_number'
BACKEND_GPM_NUMBER = 'gpm_number'
BACKEND_GPM_CREATED_DATE='gpm_created_date'
BACKEND_EQUIPMENT_ID='equipment_id'
BACKEND_PH_LOCATION='ph_location'
BACKEND_REVERSE_FLAG='reserve_flag'
BACKEND_SHIPPING_LINER_CODE='sline_code'
BACKEND_CHA_CODE='cha_code'
BACKEND_GW_PORT_CODE='gw_port_code'
BACKEND_JOB_START_TIME='job_start_time'
BACKEND_JOB_END_TIME='job_end_time'
BACKEND_TOTAL_NO_OF_PACKAGES_JOB_DONE='total_package_count'
BACKEND_TOTAL_NO_OF_PACKAGES_DAMAGED='total_no_of_packages_damaged'
BACKEND_TOTAL_NO_AREA='total_no_area'
BACKEND_MAX_DATE_UNLOADING='max_date_unloading'
BACKEND_TOTAL_NO_OF_PACKAGES_EXCESS='total_no_of_packages_excess'
BACKEND_TOTAL_NO_OF_PACKAGES_SHORT='total_no_of_packages_short'
BACKEND_GATE_NUMBER='gate_number'
BACKEND_CRN_DATE='crn_date'
BACKEND_CON_DATE='con_date'
BACKEND_CRN_NUMBER='crn_number'
BACKEND_CARGO_WEIGHT_IN_CRN='cargo_weight_in_crn'
BACKEND_WEIGHT_REMAINING='weight_remaining'
BACKEND_PRIVATE_OR_CONCOR_LABOUR_FLAG='private_or_concor_labour_flag'
BACKEND_HANDLING_CODE='handling_code'
BACKEND_WAREHOUSE_NAME='warehouse_name'
BACKEND_WAREHOUSE_ID='concor_warehouse_id'
BACKEND_STACKING_TYPE='stacking_type'



BACKEND_SHIPPING_BILL_NUMBER = 'shipping_bill'
BACKEND_BILL_OF_ENTRY_NUMBER = 'bill_of_entry'
BACKEND_BILL_OF_LADEN_NUMBER = 'bill_of_lading'
# BACKEND_BILL_DATE = 'bill_date'
# BACKEND_IMPORTER_CODE = 'importer_code'
# BACKEND_IMPORTER_NAME = 'importer_name'
BACKEND_PACKAGE_CODE = 'package_code'
BACKEND_FULL_OR_PART_DESTUFF = 'full_or_part_destuff'
BACKEND_PACKAGE_COUNT = 'package_count'
BACKEND_NO_OF_PACKAGES_DAMAGED = 'damaged_count'
BACKEND_AREA = 'area_of_cargo'
BACKEND_GRID_NUMBER = 'grid_number'
BACKEND_AREA_DAMAGED = 'area_of_damaged_cargo'
BACKEND_GRID_LOCATIONS = 'grid_locations'
BACKEND_CCLS_GRID_LOCATIONS = 'ccls_grid_locations'
BACKEND_CHA_CODE = 'cha_code'
BACKEND_PACKAGE_WEIGHT = 'packages_weight'
BACKEND_DAMAGED_PACKAGES_WEIGHT = 'damaged_packages_weight'
BACKEND_START_TIME = 'start_time'
BACKEND_END_TIME = 'end_time'
BACKEND_TRUCK_NUMBER = 'truck_number'
BACKEND_CONTAINER_NUMBER = 'container_number'
BACKEND_JOB_TYPE = 'job_type'
BACKEND_CONTAINER_FLAG = 'fcl_or_lcl'


#exception message
WH_COMMON_EXCEPTION_MESSAGE="CCLS Service,Error while communication with ccls service"
WH_CCLS_JOB_ORDER_NOT_FOUND="CCLS Service,Data doesn't exists with this job order"


# warehouse ccls wsdl
#carting
KEY_CARTING_FCL_SERVICE_TYPE='CWHCartingRead'
KEY_CARTING_FCL_SERVICE_NAME='cwhcartingreadbpel_client_ep'
KEY_CARTING_FCL_PORT_NAME='CWHCartingReadBPEL_pt'
KEY_CARTING_LCL_SERVICE_TYPE='CWHCartingReadLCL'
KEY_CARTING_LCL_SERVICE_NAME='cwhcartinglclbpel_client_ep'
KEY_CARTING_LCL_PORT_NAME='CWHCartingLCLBpel_pt'
#stuffing
KEY_STUFFING_FCL_SERVICE_TYPE='CWHStuffingReadFCL'
KEY_STUFFING_FCL_SERVICE_NAME='cwhstuffingfcl_client_ep'
KEY_STUFFING_FCL_PORT_NAME='CWHStuffingFCL_pt'
KEY_STUFFING_LCL_SERVICE_TYPE='CWHStuffingRead'
KEY_STUFFING_LCL_SERVICE_NAME='cwhstuffingreadbpel_client_ep'
KEY_STUFFING_LCL_PORT_NAME='CWHStuffingReadBPEL_pt'
#destuffing
KEY_DESTUFFING_FCL_SERVICE_TYPE='CWHDestuffingRead'
KEY_DESTUFFING_FCL_SERVICE_NAME='cwhdestuffingreadbpel_client_ep'
KEY_DESTUFFING_FCL_PORT_NAME='CWHDeStuffingReadBPEL_pt'
KEY_DESTUFFING_LCL_SERVICE_TYPE='CWHDestuffingReadLCL'
KEY_DESTUFFING_LCL_SERVICE_NAME='lclcargodestuffing_client_ep'
KEY_DESTUFFING_LCL_PORT_NAME='LCLCargoDestuffing_pt'
#delivery
KEY_DELIVERY_FCL_SERVICE_TYPE='CWHDeliveryRead'
KEY_DELIVERY_FCL_SERVICE_NAME='cwhdeliveryreadbpel_client_ep'
KEY_DELIVERY_FCL_PORT_NAME='CWHDeliveryReadBPEL_pt'
KEY_DELIVERY_LCL_SERVICE_TYPE='CWHDeliveryRead'
KEY_DELIVERY_LCL_SERVICE_NAME='cwhdeliveryreadbpel_client_ep'
KEY_DELIVERY_LCL_PORT_NAME='CWHDeliveryReadBPEL_pt'

#ccls response
KEY_CCLS_RESPONSE_TYPE='warehouse'

#revenue
#impot
KEY_IMPORT_REVENUE_SERVICE_TYPE='ImportRevenue'
KEY_IMPORT_REVENUE_SERVICE_NAME='importrvenuereport_client_ep'
KEY_IMPORT_REVENUE_PORT_NAME='CWHImportReadBPL'

#export
KEY_EXPORT_REVENUE_SERVICE_TYPE='ExportRevenue'
KEY_EXPORT_REVENUE_SERVICE_NAME='exportrevenuebpel_client_ep'
KEY_EXPORT_REVENUE_PORT_NAME='CWHExportReadBPL'

#revenue amount info
KEY_EXPORT_FCL_ESTIMATED_REVENUE_SERVICE_TYPE='RevenueEstExpFCL'
KEY_EXPORT_FCL_ESTIMATED_REVENUE_SERVICE_NAME='revenueestexpfclbpel_client_ep'
KEY_EXPORT_FCL_ESTIMATED_REVENUE_PORT_NAME='RevenueEstExpFCLBpel_pt'

KEY_EXPORT_LCL_ESTIMATED_REVENUE_SERVICE_TYPE='RevenueEstExportLCL'
KEY_EXPORT_LCL_ESTIMATED_REVENUE_SERVICE_NAME='revenueestexportlclbpel_client_ep'
KEY_EXPORT_LCL_ESTIMATED_REVENUE_PORT_NAME='RevenueEstExportLCLBPEL_pt'

KEY_IMPORT_FCL_ESTIMATED_REVENUE_SERVICE_TYPE='RevenueEstimate'
KEY_IMPORT_FCL_ESTIMATED_REVENUE_SERVICE_NAME='revenueest_client_ep'
KEY_IMPORT_FCL_ESTIMATED_REVENUE_PORT_NAME='RevenueEst_pt'

KEY_IMPORT_LCL_ESTIMATED_REVENUE_SERVICE_TYPE='RevenueEstImpBillwise'
KEY_IMPORT_LCL_ESTIMATED_REVENUE_SERVICE_NAME='revenueestimpbillwisebpel_client_ep'
KEY_IMPORT_LCL_ESTIMATED_REVENUE_PORT_NAME='RevenueEstImpBillwiseBPEL_pt'