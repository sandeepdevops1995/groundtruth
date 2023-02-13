UPDATE TM_CCTRDTLS
SET
    ctr_type = :ctr_type,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
