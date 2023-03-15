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
    INPROGRESS = 1
    COMPLETED = 2