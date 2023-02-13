-- # Hardcoded tcontainer number MSKU6523832 for testing need to change for actual data
SELECT * FROM 
(SELECT sbill_no as bill_no, 'Shipping Bill' as bill_type,'' as bill_details,ctr_no FROM TP_EDI_CAR_SBILL_CAPTURE tecsc 
UNION 
SELECT ti.BOE_NO as bill_no, 'Bill of Entry' as bill_type,'' as bill_details,ctr_no  FROM TT_IBOECTR ti)
WHERE (:container_number is null or  CTR_NO ='MSKU6523832')