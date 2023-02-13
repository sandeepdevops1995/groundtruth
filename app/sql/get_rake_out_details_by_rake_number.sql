select TRACK_NO as track_number,
TRN_NO as train_number,
CAST(WGN_NO AS Int) as wagon_number,
CTR_NO as container_no,
RAKE_NO as rake_number,
DEST_STN  AS POD,
1 AS wagon_id,
(SELECT CISO.CTR_ISO_CD FROM TM_CCTRISOCD CISO WHERE tcr.CTR_SIZE=ciso.CTR_SIZE AND tcr.CTR_TYPE= ciso.CTR_TYPE) AS iso_code,
'TESTCARGO' AS CARGO_TYPE,
'TESTSEAL' AS LINER_SEAL,
'TESTSEAL' AS CUSTOM_SEAL,
'TESTDE' AS RAKE_TYPE
from TT_COUTADVCTR_RAKE tcr where RAKE_NO =:rake_number 