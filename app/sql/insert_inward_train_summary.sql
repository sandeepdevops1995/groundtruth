INSERT INTO CCLS_DEV.TT_CINWTRSUMM (WTR_NO,HLD_TRACK_NO,DT_WTR,IMP_EXP_FLG,REC_CNT,
CNCL_FLG,TRNS_DT_TM,USER_ID,EQPT_ID) VALUES 
(:wtr_no,:track_number,sysdate,'I',:wagon_count,
NULL,sysdate,'TEST','RTG1')