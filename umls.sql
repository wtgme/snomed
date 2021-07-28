SELECT * FROM SRDEF s WHERE s.RT LIKE 'RL';

SELECT DISTINCT (REL) FROM MRREL m WHERE m.RELA IS NULL ; 
-- RB
-- RN
-- RO
-- CHD
-- PAR
-- SIB
-- SY
-- RQ
-- AQ
-- QB

-- The mapping between a RELA label and its corresponding SNOMED CT ConceptId
SELECT * FROM MRDOC m WHERE m.`TYPE` = 'snomedct_rela_mapping'

select * from MRSTY WHERE TUI='T154'


SELECT * FROM MRDOC WHERE type = 'rela_inverse' AND dockey = 'RELA' 

AND VALUE LIKE '%treat'


SELECT COUNT(DISTINCT CUI2) FROM MRREL m WHERE m.DIR = 'Y'
-- 410716

SELECT COUNT(DISTINCT CUI2) FROM MRREL
-- 3741066

select COUNT(DISTINCT CUI2) from MRREL where (DIR='Y' or DIR IS NULL) AND (SUPPRESS='N') AND (RELA is not null)
-- 2031373

SELECT COUNT(DISTINCT CUI2) from MRREL where (DIR='Y') AND (SUPPRESS='N') AND (RELA is not null)
-- 409326

select COUNT(DISTINCT CUI2) from MRREL where (SUPPRESS='N') AND (RELA is not null)