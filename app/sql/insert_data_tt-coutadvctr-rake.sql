INSERT INTO CCLS_DEV.TT_COUTADVCTR_RAKE (TRN_NO,DT_DESP,RAKE_NO,TRACK_NO,WGN_NO,WGN_LIFE_NO,WGN_TYPE,
CTR_NO,CTR_LIFE_NO,CTR_ISO_CD,CTR_SIZE,CTR_TYPE,CTR_STAT,SLINE_CD,CTR_WT,
FIR_POD,ORG_STN,DEST_STN,CNCL_FLG,TRNS_DT_TM,USER_ID) VALUES 
('TRAIN26742',TO_DATE(to_char(sysdate+2,'DD-MM-YYYY'),'DD-MM-YYYY'),'RAKE26','H2',:wagon_number,TO_DATE(to_char(sysdate,'DD-MM-YYYY'),'DD-MM-YYYY'),'C',
:container_number,TO_DATE(to_char(sysdate,'DD-MM-YYYY'),'DD-MM-YYYY'),NULL,40,'GL','EU','APL',4.6,
NULL,'TKD','MB',NULL,sysdate,'TEST')
