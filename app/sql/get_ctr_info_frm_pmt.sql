-- # Hardcoded test data with "T_{value}" need to change this for actual data
SELECT gt_doc_no as permit_no,
to_char(dt_gt_doc,'YYYY-MM-DD HH:MI:SS') as permit_date,
to_char(dt_gt_doc_vld,'YYYY-MM-DD HH:MI:SS')as permit_expiry_date,
ctr_no as container_no,
(SELECT CISO.CTR_ISO_CD FROM TM_CCTRISOCD CISO WHERE pt.CTR_SIZE=ciso.CTR_SIZE AND pt.CTR_TYPE= ciso.CTR_TYPE) AS iso_code,
CASE WHEN pt.ldd_mt_flg ='E' THEN 'Empty' ELSE 'Laden' end as is_empty_or_laden,
to_loc as pod,(select veh.veh_no from  TT_CVEHDOCDTLS  veh WHERE pt.GT_DOC_NO = veh.DOC_NO) as gt_truck_no,'TESTLND' AS POD,
'TESToil' as cargo_type,
CASE WHEN (SELECT ctr_dtls.seal_no FROM TM_CCTRDTLS ctr_dtls WHERE pt.ctr_no = ctr_dtls.ctr_no and pt.ctr_life_no = ctr_dtls.ctr_life_no ) is NULL THEN 'TEST111' ELSE
 (SELECT ctr_dtls.seal_no FROM TM_CCTRDTLS ctr_dtls WHERE pt.ctr_no = ctr_dtls.ctr_no and pt.ctr_life_no = ctr_dtls.ctr_life_no ) end as liner_seal,

CASE WHEN (SELECT ctr_dtls.seal_no FROM TM_CCTRDTLS ctr_dtls WHERE pt.ctr_no = ctr_dtls.ctr_no and pt.ctr_life_no = ctr_dtls.ctr_life_no ) is NULL THEN 'TEST111' ELSE
 (SELECT ctr_dtls.seal_no FROM TM_CCTRDTLS ctr_dtls WHERE pt.ctr_no = ctr_dtls.ctr_no and pt.ctr_life_no = ctr_dtls.ctr_life_no ) end as custom_seal,

'TEST89' as reefer,

CASE WHEN (SELECT ctr_dtls.imp_exp_flg FROM TM_CCTRDTLS  ctr_dtls WHERE pt.ctr_no = ctr_dtls.ctr_no and pt.ctr_life_no = ctr_dtls.ctr_life_no) is NULL THEN 'TESTExport' ELSE
 (SELECT ctr_dtls.imp_exp_flg FROM TM_CCTRDTLS  ctr_dtls WHERE pt.ctr_no = ctr_dtls.ctr_no and pt.ctr_life_no = ctr_dtls.ctr_life_no) end as permit_type,
'{}' as permit_details,
TO_CHAR(pt.dt_gt_doc, 'YYYY-MM-DD HH24:MI:SS')  as permit_date,
TO_CHAR(pt.dt_gt_doc_vld, 'YYYY-MM-DD HH24:MI:SS') as permit_expiry_date
FROM TT_CCTRGTDOC pt  where gt_doc_no = :permit_number