
INSERT INTO TT_CINWTRDTLS (WTR_NO,WGN_NO,WGN_LIFE_NO,WGN_DMG_FLG,CTR_NO,CTR_LIFE_NO,CTR_ISO_CD,
CTR_STAT,CTR_SIZE,CTR_TYPE,CRG_TYPE,LDD_MT_FLG,IMP_EXP_FLG,SLINE_CD,
GW_PORT_CD,UNLDG_REQ_TYP,ACTY_CD,DT_ARR_DEP,TM_OPN,ERR_FLG,CTR_DMG_FLG,SEAL_STAT,TO_LOC,CNCL_FLG,
TRNS_DT_TM,USER_ID,SEAL_NO,DMG_CODE) VALUES 
(:wtr_no, :wagon_number,sysdate,NULL,:container_number,sysdate, :iso_code,
'IL',:container_size,:container_type,'N','L','I',:sline_code,
'BPT',NULL,'UR',sysdate ,sysdate ,'N','N','I','RS',NULL,
sysdate,'TEST',:seal_number,NULL)