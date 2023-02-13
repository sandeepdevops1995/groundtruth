UPDATE TM_CCTRDTLS
SET
    iso_code = :iso_code,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
