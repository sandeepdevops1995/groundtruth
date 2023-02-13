UPDATE TM_CCTRDTLS
SET
    dmg_code = :dmg_code,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
