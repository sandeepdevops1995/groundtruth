select CTR_NO as container_no,
 (SELECT CISO.CTR_ISO_CD FROM TM_CCTRISOCD CISO WHERE T_CTR.CTR_SIZE=ciso.CTR_SIZE AND T_CTR.CTR_TYPE= ciso.CTR_TYPE) AS iso_code,
 'TESTSEAL' as liner_seal, 
 'TESTSEAL' as custom_seal, 
 CAST(WGN_NO AS Int) as wagon_number,
 REC_NO as wagon_id,
 (SELECT TC.RAKE_NO FROM TT_CINADVCHK TC WHERE TC.WGN_NO = T_CTR.WGN_NO) AS rake_number,
 (SELECT TC.HLD_TRACK_NO FROM TT_CINADVCHK TC WHERE TC.WGN_NO = T_CTR.WGN_NO) AS track_number,
 TRN_NO AS train_number,
 'TESTCARGO' as cargo_type,
 STN_CD as pod,
 'TESTAR'  AS rake_type
 from TT_CINADVCTR T_CTR where WGN_NO =:wagon_number