UPDATE TM_CCTRDTLS
SET
    sline_code = :sline_code,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
