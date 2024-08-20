USE hospital_register;

SET collation_connection = 'utf8mb4_unicode_ci';

SET @lang = 'de';

SELECT ht.hospital_id, hd.provider_type_code, ht.treatment_count, td.treatment_code, td.treatment_name, l.language_name, hd.emergency_service_level
	FROM hospital_treatments AS ht
    INNER JOIN hospital_details AS hd ON hd.hospital_id  = ht.hospital_id
    INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
    INNER JOIN languages AS l ON l.language_code = td.language_code
    WHERE td.language_code = @lang AND hd.provider_type_code IN ('P', 'O') AND ht.treatment_count > 0
    ;
    
SELECT hd.hospital_id, hd.nursing_count, hd.total_stations_count, hd.provider_type_code
	FROM hospital_details AS hd;

DROP TABLE total_count_per_treatment;
CREATE TEMPORARY TABLE total_count_per_treatment AS
	SELECT ht.treatment_code, SUM(ht.treatment_count) AS sum_treatment_count, AVG(ht.treatment_count) AS avg_treatment_count
		FROM hospital_treatments AS ht
		GROUP BY ht.treatment_code;

SELECT ht.treatment_code, td.treatment_name, hd.provider_type_code, tcpt.sum_treatment_count, AVG(ht.treatment_count), COUNT(ht.hospital_id), AVG(hd.bed_count)
	FROM hospital_treatments AS ht
    INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
    INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
    INNER JOIN total_count_per_treatment AS tcpt ON tcpt.treatment_code = ht.treatment_code
    WHERE td.language_code = 'en' AND ht.treatment_count > 0
    GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name, tcpt.sum_treatment_count;


DROP TABLE total_count_per_treatment;
CREATE TEMPORARY TABLE total_count_per_treatment AS
	SELECT ht.treatment_code, SUM(ht.treatment_count) AS sum_treatment_count, AVG(ht.treatment_count) AS avg_treatment_count
		FROM hospital_treatments AS ht
		GROUP BY ht.treatment_code;
        
WITH total_count_per_treatment AS
	(SELECT ht.treatment_code, SUM(ht.treatment_count) AS sum_treatment_count, AVG(ht.treatment_count) AS avg_treatment_count
		FROM hospital_treatments AS ht
		GROUP BY ht.treatment_code)
SELECT ht.treatment_code, td.treatment_name, hd.provider_type_code, ht.treatment_count, tcpt.sum_treatment_count, tcpt.avg_treatment_count, (ht.treatment_count-tcpt.avg_treatment_count)/tcpt.avg_treatment_count AS relative_treatment_count
	FROM hospital_treatments AS ht
    INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
    INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
    INNER JOIN total_count_per_treatment AS tcpt ON tcpt.treatment_code = ht.treatment_code
    WHERE td.language_code = 'en' AND ht.treatment_count > 0;
    
    
SELECT ht.treatment_code, hd.provider_type_code, td.treatment_name, SUM(ht.treatment_count) sum_treatment_count, SUM(hd.total_treatments) AS sum_total_treatments, AVG(ht.treatment_count/total_treatments*100) AS avg_treatment_count_share
	FROM hospital_treatments AS ht
    INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
    INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
    WHERE td.language_code = 'en' AND ht.treatment_count > 0
    GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name;
        

SELECT hd.provider_type_code, hd.nursing_quotient, hd.total_stations_count
	FROM hospital_details AS hd;
    
SELECT ht.treatment_code, hd.provider_type_code, td.treatment_name, SUM(ht.treatment_count) AS sum_treatment_count
	FROM hospital_treatments AS ht
    INNER JOIN hospital_details AS hd ON hd.hospital_id = ht.hospital_id
    INNER JOIN treatments_dict as td ON td.treatment_code = ht.treatment_code
    WHERE td.language_code = 'en'
    GROUP BY ht.treatment_code, hd.provider_type_code, td.treatment_name;


SELECT name, hd.provider_type_code, hd.bed_count AS beds_number, latitude, longitude, has_emergency_service
	FROM hospital_locations AS hl
	JOIN hospital_details AS hd ON hl.hospital_id = hd.hospital_id
	WHERE hd.bed_count >= 10
	AND hd.bed_count <= 1000
	AND hd.provider_type_code IN ('O','P')
    AND hd.has_emergency_service = True;