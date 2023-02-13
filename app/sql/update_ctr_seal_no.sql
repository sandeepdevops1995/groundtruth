UPDATE TM_CCTRDTLS
SET
    seal_no = :seal_no,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
