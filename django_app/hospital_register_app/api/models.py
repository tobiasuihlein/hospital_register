from django.db import models

class Languages(models.Model):
    language_code = models.CharField(primary_key=True, max_length=2)
    language_name = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'languages'
        app_label = 'api'

class ProviderTypeCodes(models.Model):
    provider_type_code = models.CharField(primary_key=True, max_length=1)

    class Meta:
        db_table = 'provider_type_codes'
        app_label = 'api'


class ProviderTypesDict(models.Model):
    provider_type_code = models.ForeignKey(ProviderTypeCodes, models.DO_NOTHING, db_column='provider_type_code', blank=True, null=True)
    provider_type_name = models.CharField(max_length=50, blank=True, null=True)
    language_code = models.ForeignKey(Languages, models.DO_NOTHING, db_column='language_code', blank=True, null=True)

    class Meta:
        db_table = 'provider_types_dict'
        app_label = 'api'
        unique_together = (('provider_type_code', 'language_code'),)


class DepartmentCodes(models.Model):
    department_code = models.CharField(primary_key=True, max_length=4)

    class Meta:
        db_table = 'department_codes'
        app_label = 'api'


class TreatmentCodes(models.Model):
    treatment_code = models.CharField(primary_key=True, max_length=7)

    class Meta:
        db_table = 'treatment_codes'
        app_label = 'api'


class FederalStates(models.Model):
    federal_state_code = models.CharField(primary_key=True, max_length=2)
    area = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    population = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'federal_states'
        app_label = 'api'


class FederalStatesDict(models.Model):
    federal_state_code = models.ForeignKey(FederalStates, models.DO_NOTHING, db_column='federal_state_code', blank=True, null=True)
    federal_state_name = models.CharField(max_length=191, blank=True, null=True)
    language_code = models.ForeignKey('Languages', models.DO_NOTHING, db_column='language_code', blank=True, null=True)

    class Meta:
        db_table = 'federal_states_dict'
        app_label = 'api'
        unique_together = (('federal_state_code', 'language_code'),)


class HospitalLocations(models.Model):
    hospital_id = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=191, blank=True, null=True)
    street = models.CharField(max_length=191, blank=True, null=True)
    city = models.CharField(max_length=191, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)
    federal_state_code = models.ForeignKey(FederalStates, models.DO_NOTHING, db_column='federal_state_code', blank=True, null=True)
    phone = models.CharField(max_length=191, blank=True, null=True)
    mail = models.CharField(max_length=191, blank=True, null=True)
    latitude = models.DecimalField(max_digits=14, decimal_places=12, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=12, blank=True, null=True)
    link = models.CharField(max_length=191, blank=True, null=True)

    class Meta:
        db_table = 'hospital_locations'
        app_label = 'api'


class DepartmentsDict(models.Model):
    department_code = models.ForeignKey(DepartmentCodes, models.DO_NOTHING, db_column='department_code', blank=True, null=True)
    parent_department_code = models.CharField(max_length=4, blank=True, null=True)
    department_name = models.CharField(max_length=191, blank=True, null=True)
    parent_department_name = models.CharField(max_length=191, blank=True, null=True)
    language_code = models.ForeignKey('Languages', models.DO_NOTHING, db_column='language_code', blank=True, null=True)

    class Meta:
        db_table = 'departments_dict'
        app_label = 'api'
        unique_together = (('department_code', 'language_code'),)


class HospitalDepartments(models.Model):
    hospital = models.ForeignKey('HospitalLocations', models.DO_NOTHING, blank=True, null=True)
    department_code = models.ForeignKey(DepartmentCodes, models.DO_NOTHING, db_column='department_code', blank=True, null=True)
    treatment_count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'hospital_departments'
        app_label = 'api'
        unique_together = (('hospital', 'department_code'),)


class TreatmentsDict(models.Model):
    treatment_code = models.ForeignKey(TreatmentCodes, models.DO_NOTHING, db_column='treatment_code', blank=True, null=True)
    treatment_name = models.CharField(max_length=191, blank=True, null=True)
    language_code = models.ForeignKey(Languages, models.DO_NOTHING, db_column='language_code', blank=True, null=True)

    class Meta:
        db_table = 'treatments_dict'
        app_label = 'api'
        unique_together = (('treatment_code', 'language_code'),)


class HospitalTreatments(models.Model):
    hospital = models.ForeignKey(HospitalLocations, models.DO_NOTHING, blank=True, null=True)
    treatment_code = models.ForeignKey('TreatmentCodes', models.DO_NOTHING, db_column='treatment_code', blank=True, null=True)
    treatment_count = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'hospital_treatments'
        app_label = 'api'
        unique_together = (('hospital', 'treatment_code'),)


class HospitalDetails(models.Model):
    hospital = models.OneToOneField('HospitalLocations', models.DO_NOTHING, blank=True, primary_key=True, default='123456')
    total_treatments = models.IntegerField(blank=True, null=True)
    nursing_quotient = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    nursing_count = models.IntegerField(blank=True, null=True)
    provider_type_code = models.ForeignKey('ProviderTypeCodes', models.DO_NOTHING, db_column='provider_type_code', blank=True, null=True)
    bed_count = models.IntegerField(blank=True, null=True)
    semi_residential_count = models.IntegerField(blank=True, null=True)
    total_stations_count = models.IntegerField(blank=True, null=True)
    has_emergency_service = models.IntegerField(blank=True, null=True)
    emergency_service_level = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'hospital_details'
        app_label = 'api'


class HospitalCertificates(models.Model):
    hospital = models.ForeignKey('HospitalLocations', models.DO_NOTHING, blank=True, null=True)
    certificate = models.CharField(max_length=191, blank=True, null=True)
    language_code = models.ForeignKey('Languages', models.DO_NOTHING, db_column='language_code', blank=True, null=True)

    class Meta:
        db_table = 'hospital_certificates'
        app_label = 'api'
        unique_together = (('hospital', 'certificate', 'language_code'),)


class Places(models.Model):
    name = models.CharField(max_length=191, blank=True, null=True)
    city_district = models.CharField(max_length=191, blank=True, null=True)
    rural_district = models.CharField(max_length=191, blank=True, null=True)
    zip = models.CharField(max_length=5, blank=True, null=True)
    federal_state_code = models.ForeignKey(FederalStates, models.DO_NOTHING, db_column='federal_state_code', blank=True, null=True)
    latitude = models.DecimalField(max_digits=8, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        db_table = 'places'
        app_label = 'api'
        unique_together = (('name', 'city_district', 'rural_district', 'zip', 'federal_state_code'),)









