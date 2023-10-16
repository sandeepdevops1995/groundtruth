
from flask_restful import Resource
from app import api
from app.controllers.gate_controller import *
from app.controllers.rake_controller import *
# from app.controllers.warehouse_controller import WarehouseData
from app.controllers.warehouse_controller import JobDetails,WarehouseTallySheet,WarehouseCommodities,WarehousePrintTallySheet, WarehouseRevenue,GetRevenueInfo
from app.controllers.GT_upload_controller import TrainSummary,PendancySummary
from app.controllers.master_controller import *
from app.controllers.yard_controller import StackLocation

import app.constants as Constants 

def register_controllers(): 
    
    # Gate
    api.add_resource(ContainerData,Constants.UPLOAD_DATA_ENDPOINT)                              ##requires psql and oracle support          
    api.add_resource(CclsData,Constants.CCLS_DATA_ENDPOINT)                                     ##requires psql and oracle support
    api.add_resource(UpdateContainerDetails,Constants.UPDATE_CONTAINER_DETAILS_ENDPOINT)        ##requires psql and oracle support

    
    # Rake
    api.add_resource(TrainDetails,Constants.TRAIN_DETAILS_ENDPOINT)
    api.add_resource(RakeData,Constants.RAKE_UPLOAD_DATA_ENDPOINT)                              ##requires psql and oracle support
    api.add_resource(UpdateInwardRakeDetails,Constants.UPDATE_INWARD_WTR_ENDPOINT)
    api.add_resource(UpdateOutwardRakeDetails,Constants.UPDATE_OUTWARD_WTR_ENDPOINT)
    api.add_resource(RakePlanDetails,Constants.RAKE_PLAN_ENDPOINT)
    api.add_resource(UpdateCGISurvey,Constants.CGI_SURVEY_ENDPOINT)
    api.add_resource(UpdateCGOSurvey,Constants.CGO_SURVEY_ENDPOINT)
    api.add_resource(UpdateVGISurvey,Constants.VGI_SURVEY_ENDPOINT)
    api.add_resource(RakeInContainer,Constants.RAKE_INWARD_CONTAINER_ENDPOINT)
    api.add_resource(CclsResponseData,'/ccls_response_data')
    api.add_resource(TrainNumberDetails,'/train_number')
    api.add_resource(UpdateRakeDetails,'/update_ctms_rake_details')
    # api.add_resource(GtRangeData,'/gt_range_data')
    # api.add_resource(GtTrainData,'/gt_train_data')

    
    # To upload Ground Truth
    api.add_resource(TrainSummary,'/upload_train_summary')      # input: CCLS XML file
    api.add_resource(GroundTruthData,'/rake_ground_truth')      # input: OUR JSON Format data
    api.add_resource(PendancySummary,'/pendancy_summary')       # input: CCLS PENDANCY XML file 
    
    
    # Yard
    api.add_resource(WagonMaster,Constants.WAGON_ENDPOINT)
    api.add_resource(GatewayPortsMaster,Constants.GATEWAY_PORT_ENDPOINT)
    api.add_resource(StackLocation,Constants.STACK_LOCATION_ENDPOINT)
    api.add_resource(PendancyList,Constants.PENDANCY_CONTAINERS_ENDPOINT)
    api.add_resource(DomesticPendancyList,Constants.DOMESTIC_PENDENCY_CONTAINERS_ENDPOINT)
    api.add_resource(UpdateRakeContainerDetails,Constants.UPDATE_RAKE_CONTAINER_ENDPOINT)
    
    
    # Warehouse
    # api.add_resource(WarehouseData,Constants.WAREHOUSE_DATA_ENDPOINT)
    api.add_resource(JobDetails,'/warehouse_details')
    api.add_resource(WarehouseTallySheet,'/api/warehouse_tallysheet')
    api.add_resource(WarehousePrintTallySheet,'/api/warehouse_print_tallysheet')
    api.add_resource(WarehouseCommodities,'/fetch_commodities')
    api.add_resource(WarehouseRevenue,'/warehouse_revenue_details')
    api.add_resource(GetRevenueInfo,'/warehouse_revenue_info')
    
    #Master
    api.add_resource(TrackMasterDetails,Constants.TRACK_MASTER_DATA_ENDPOINT)
    api.add_resource(ContainerStatDetails,Constants.CONTAINER_STAT_ENDPOINT)
    
    # These API's use ORACLE Db. Currently we are anot using it
    api.add_resource(GateInModel,"/gateIn")
    api.add_resource(GateOutModel,"/gateOut")
    api.add_resource(UpdateCtrStackDetails,"/UpdateCtrStackDetails")
    api.add_resource(RakeContainer,Constants.CONTAINER_DETAILS_ENDPOINT)    ##requires psql and oracle support
    api.add_resource(RakeWagon,Constants.WAGON_DETAILS_ENDPOINT)            ##requires psql and oracle support
    api.add_resource(UpdateWTR,Constants.UPDATE_WTR_ENDPOINT)
    api.add_resource(WagonTypes,'/wagon_types')
    api.add_resource(SlineCodes,'/sline_codes')
    api.add_resource(PodCodes,'/pod_codes')
    api.add_resource(IcdLocations,'/icd_locations')
    api.add_resource(ContainerTypes,'/container_types')
    api.add_resource(CommodityCodes,'/commodity_codes')
    api.add_resource(CommodityTypes,'/commodity_types')
    api.add_resource(ActivityTypes,'/activity_types')
    api.add_resource(PortCodes,'/port_codes')
    api.add_resource(OutLocation,'/out_locations')
    api.add_resource(OutPortCodes,'/out_ports')
    api.add_resource(CargoTypes,'/cargo_types')
    api.add_resource(UserList,'/user_list')
    api.add_resource(ISO6346Data, Constants.ISO_6346_CODE_ENDPOINT)
      
    
