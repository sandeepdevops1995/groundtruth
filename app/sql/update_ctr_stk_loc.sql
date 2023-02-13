UPDATE TM_CCTRDTLS
SET
    stk_loc = :stk_loc,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
