import enum 

class JobType(enum.Enum):
    DIRECT_STUFFING = 0
    DIRECT_DELIVERY = 1
    STUFFING = 2
    DESTUFFING = 3
    CARTING = 4
    DELIVERY = 5

class ContainerFlag(enum.Enum):
    FCL = 1
    LCL = 2

class JobOrderType(enum.Enum):
   CARTING_FCL=1
   CARTING_LCL=2
   STUFFING_FCL=3
   STUFFING_LCL=4
   DE_STUFFING_FCL=5
   DE_STUFFING_LCL=6
   DELIVERY_FCL=7
   DELIVERY_LCL=8
   DIRECT_STUFFING=9
   DIRECT_DELIVERY=10

class JobStatus(enum.Enum):
    TALLYSHEET_GENERATED = 1
    TALLYSHEET_UPLOADED = 2

class SerialNumberType(enum.Enum):
    CARTING = 'C'
    STUFFING = 'S'
    DESTUFFING = 'D'
    DELIVERY = 'DE'
    DIRECT_STUFFING = 'DS'
    DIRECT_DELIVERY = 'DD'
    
class PendencyType(enum.Enum):
    LOADED = 1
    EMPTY = 2
    EXPRESS_LCL = 3
    BLOCK = 4

class EquipmentNames(enum.Enum):
    RMGTRCK = "RMG2"
    RMGTRCK02 = "RMG2"
    RST03 = "RH03"
    RST04 = "RH04"
    RST05 = "RH05"
    RST06 = "RH06"
    RST07 = "RH07"
    RST08 = "RH08"
    RST10 = "RH10"
    RST12 = "RH12"
    RST13 = "RH13"
    RST14 = "RH14"
    RTG03 = "RTG3"
    RTG04 = "RTG4"
    RTG05 = "RTG5"
    RTG6 = "RTG6"
    RTG07 = "RTG7"
    RTG08 = "RTG8"
    RTG09 = "RTG9"
    SANY01 = "R-S1"
    SANY02 = "R-S2"
    SANY03 = "R-S3"
    FLT01 = "FRK1"

class RevenueType(enum.Enum):
    EXPORT_FCL_REVENUE=1
    EXPORT_LCL_REVENUE=2
    IMPORT_FCL_REVENUE=3
    IMPORT_LCL_REVENUE=4
