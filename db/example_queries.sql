USE hospital_register;

SELECT ht.hospital_id, hd.provider_type_code, ht.treatment_count, td.treatment_code, td.treatment_name, l.language_name, hd.emergency_service_level
	FROM hospital_treatments AS ht
    INNER JOIN hospital_details AS hd ON hd.hospital_id  = ht.hospital_id
    INNER JOIN treatments_dict AS td ON td.treatment_code = ht.treatment_code
    INNER JOIN languages AS l ON l.language_code = td.language_code
    WHERE td.language_code = 'de'
    ;