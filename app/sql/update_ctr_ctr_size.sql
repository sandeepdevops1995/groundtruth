UPDATE TM_CCTRDTLS
SET
    ctr_size = :ctr_size,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
