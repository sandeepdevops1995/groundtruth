UPDATE TM_CCTRDTLS
SET
    dmg_flg = :dmg_flg,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
