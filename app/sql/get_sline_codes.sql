select   sline_cus as  sline_cus  ,
         sline_cncr as  sline_cncr  ,
         user_id as  user_id 
from TM_FSLINECONV

-- Got from gate not used anywhere in gate groud truth
-- SELECT tc.SLINE_CD, tc.SLINE_NAM, tc.CHQ_FACILITY, tc.ACTV_FLG FROM TM_CSLINE tc 
