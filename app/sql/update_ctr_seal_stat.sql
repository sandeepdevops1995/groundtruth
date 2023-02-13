UPDATE TM_CCTRDTLS
SET
    seal_stat = :seal_stat,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
