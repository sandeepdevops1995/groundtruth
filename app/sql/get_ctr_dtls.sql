SELECT ctr.CTR_NO , ctr.CTR_SIZE ,ctr.CTR_TYPE ,ctype.CTR_TYPE_DESC ,ctr.SLINE_CD , ctr.SEAL_NO , ctr.FCL_LCL_FLG ,ctr.GW_PORT_CD ,ctr.LDD_MT_FLG , 
ctr.CTR_LOC_FLG ,CASE  WHEN ctr.IMP_EXP_FLG='E'  THEN 'Export' ELSE 'Import' end as Trans_type, TO_CHAR (ctr.DT_ARR, 'dd-mm-yyyy HH24:MI') as date_arr, 
TO_CHAR (ctr.DT_DEP, 'dd-mm-yyyy HH24:MI') as date_dept , ctr.CTR_STAT ,(SELECT CISO.CTR_ISO_CD FROM TM_CCTRISOCD CISO WHERE ctr.CTR_SIZE=ciso.CTR_SIZE 
AND ctr.CTR_TYPE= ciso.CTR_TYPE) AS iso_code, pt.gt_doc_no as permit_no,to_date (TO_char (pt.DT_GT_DOC_VLD, 'dd-mm-YYYY HH24:MI'),'dd-mm-YYYY HH24:MI') as validity
FROM TM_CCTRDTLS ctr ,TM_CCTRTYPE ctype, TT_CCTRGTDOC pt
WHERE ctr.CTR_TYPE = CTYPe.CTR_TYPE AND ctr.CTR_NO = pt.CTR_NO AND ctr.ctr_life_no = pt.ctr_life_no AND ctr.CTR_NO =:container_number 
ORDER BY pt.DT_GT_DOC_VLD desc 