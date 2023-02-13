UPDATE TM_CCTRDTLS
SET
    imp_exp_flg = :import_export,trns_dt_tm = sysdate
WHERE
    ctr_no = :container_number
