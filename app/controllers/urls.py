
from flask_restful import Resource
from app import api
from app.controllers.gate_controller import ContainerData,CclsData,GateInModel,GateOutModel, UpdateContainerDetails, UpdateCtrStackDetails, ISO6346Data
from app.controllers.rake_controller import RakeData, RakeContainer,RakeWagon, UpdateWTR, WagonTypes, SlineCodes, IcdLocations, PodCodes, ContainerTypes, CommodityCodes, CommodityTypes, ActivityTypes, ContainerTypes, PortCodes, OutLocation, OutPortCodes, CargoTypes, UserList
from app.controllers.warehouse_controller import WarehouseData
from app.controllers.GT_upload_controller import TrainSummary

import app.constants as Constants 

def register_controllers():
    api.add_resource(ContainerData,Constants.UPLOAD_DATA_ENDPOINT)          ##requires psql and oracle support          
    api.add_resource(CclsData,Constants.CCLS_DATA_ENDPOINT)                 ##requires psql and oracle support
    api.add_resource(GateInModel,"/gateIn")
    api.add_resource(GateOutModel,"/gateOut")
    api.add_resource(UpdateContainerDetails,"/updateContainerInfo")         ##requires psql and oracle support
    api.add_resource(UpdateCtrStackDetails,"/UpdateCtrStackDetails")
    api.add_resource(RakeData,Constants.RAKE_UPLOAD_DATA_ENDPOINT)          ##requires psql and oracle support
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
    api.add_resource(WarehouseData,Constants.WAREHOUSE_DATA_ENDPOINT)
    
    # To upload Ground Truth
    api.add_resource(TrainSummary,'/upload_train_summary')
