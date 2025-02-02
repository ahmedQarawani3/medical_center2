# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountsUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    role = models.CharField(max_length=10)
    phone_number = models.CharField(unique=True, max_length=15)
    email = models.CharField(max_length=254)
    username = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'accounts_user'


class AccountsUserGroups(models.Model):
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_user_groups'
        unique_together = (('user', 'group'),)


class AccountsUserUserPermissions(models.Model):
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_user_user_permissions'
        unique_together = (('user', 'permission'),)


class AppointmentsAppointment(models.Model):
    date = models.DateField()
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    doctor = models.ForeignKey('DoctorsDoctor', models.DO_NOTHING)
    patient = models.ForeignKey('PatientsPatient', models.DO_NOTHING, blank=True, null=True)
    payment = models.ForeignKey('BillingPayment', models.DO_NOTHING, blank=True, null=True)
    time_slot = models.TimeField()
    payment_transaction_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'appointments_appointment'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AccountsUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'authtoken_token'


class BillingPayment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    status = models.CharField(max_length=10)
    patient = models.ForeignKey('PatientsPatient', models.DO_NOTHING)
    payment_date = models.DateTimeField(blank=True, null=True)
    transaction_id = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'billing_payment'


class DjangoAdminLog(models.Model):
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING)
    action_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class DoctorsAssistantdoctor(models.Model):
    notes = models.TextField()
    status = models.CharField(max_length=20)
    patient = models.ForeignKey('PatientsPatient', models.DO_NOTHING)
    doctor = models.ForeignKey('DoctorsDoctor', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'doctors_assistantdoctor'


class DoctorsAvailability(models.Model):
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()
    doctor = models.ForeignKey('DoctorsDoctor', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'doctors_availability'


class DoctorsDepartment(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'doctors_department'


class DoctorsDoctor(models.Model):
    years_of_experience = models.PositiveIntegerField()
    user = models.OneToOneField(AccountsUser, models.DO_NOTHING)
    name = models.CharField(max_length=255)
    specialty = models.CharField(max_length=255)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=5)  # max_digits and decimal_places have been guessed, as this database handles decimal fields as float
    department = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'doctors_doctor'


class MedicalMedication(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'medical_medication'


class MedicalPrescriptionmedication(models.Model):
    date_issued = models.DateField()
    quantity = models.PositiveIntegerField()
    patient = models.ForeignKey('PatientsPatient', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'medical_prescriptionmedication'


class MedicalPrescriptionmedicationMedication(models.Model):
    prescriptionmedication = models.ForeignKey(MedicalPrescriptionmedication, models.DO_NOTHING)
    medication = models.ForeignKey(MedicalMedication, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'medical_prescriptionmedication_medication'
        unique_together = (('prescriptionmedication', 'medication'),)


class PatientsMedicalrecord(models.Model):
    diagnosis = models.TextField()
    recommended_treatment = models.TextField()
    created_at = models.DateTimeField()
    patient = models.ForeignKey('PatientsPatient', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'patients_medicalrecord'


class PatientsNotification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField()
    expiry_date = models.DateTimeField()
    is_active = models.BooleanField()
    title = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'patients_notification'


class PatientsPatient(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=10)
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    user = models.OneToOneField(AccountsUser, models.DO_NOTHING)
    allergies = models.TextField(blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    past_surgeries = models.TextField(blank=True, null=True)
    profile_picture = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients_patient'


class PatientsTest(models.Model):
    name = models.CharField(max_length=100)
    test_date = models.DateTimeField()
    patient = models.ForeignKey(PatientsPatient, models.DO_NOTHING)
    description = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patients_test'


class TokenBlacklistBlacklistedtoken(models.Model):
    blacklisted_at = models.DateTimeField()
    token = models.OneToOneField('TokenBlacklistOutstandingtoken', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'token_blacklist_blacklistedtoken'


class TokenBlacklistOutstandingtoken(models.Model):
    token = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    expires_at = models.DateTimeField()
    user = models.ForeignKey(AccountsUser, models.DO_NOTHING, blank=True, null=True)
    jti = models.CharField(unique=True, max_length=255)

    class Meta:
        managed = False
        db_table = 'token_blacklist_outstandingtoken'
