UPDATE TM_CCTRDTLS
SET
    ldd_mt_flg = :empty_laden,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
