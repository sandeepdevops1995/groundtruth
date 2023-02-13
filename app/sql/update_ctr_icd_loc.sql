UPDATE TM_CCTRDTLS
SET
    icd_loc_cd = :icd_loc,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
