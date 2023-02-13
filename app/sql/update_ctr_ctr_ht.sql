UPDATE TM_CCTRDTLS
SET
    ctr_ht = :ctr_ht,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
