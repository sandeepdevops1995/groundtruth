select HLD_TRACK_NO as track_number,
TRN_NO as train_number,
CAST(WGN_NO AS Int) as wagon_number,
CTR_NO as container_no,
RAKE_NO as rake_number,
(SELECT STN_CD FROM TT_CINADVCTR tc WHERE TC.CTR_NO = T_CIN.CTR_NO ) AS POD,
(SELECT REC_NO FROM TT_CINADVCTR tc WHERE TC.CTR_NO = T_CIN.CTR_NO ) AS wagon_id,
(SELECT CISO.CTR_ISO_CD FROM TM_CCTRISOCD CISO, TT_CINADVCTR tc WHERE tc.CTR_NO =T_CIN.CTR_NO AND tc.CTR_SIZE=ciso.CTR_SIZE AND tc.CTR_TYPE= ciso.CTR_TYPE) AS iso_code,
'TESTCARGO' AS CARGO_TYPE,
'TESTSEAL' AS LINER_SEAL,
'TESTSEAL' AS CUSTOM_SEAL,
'TESTAR' AS RAKE_TYPE
from TT_CINADVCHK T_CIN where RAKE_NO =:rake_number