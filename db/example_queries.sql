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
    
SELECT COUNT(ht.hospital_id), ht.treatment_code, ht.treatment_count
	FROM hospital_treatments AS ht
    WHERE ht.treatment_count > 0
    GROUP BY ht.treatment_code;
