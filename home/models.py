from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Receipe(models.Model):
    User = models.ForeignKey(User , on_delete=models.SET_NULL , null=True, blank=True)
    case_number = models.CharField(max_length=100, null=True, blank=True)
    receipe_name = models.CharField(max_length=100, null=True, blank=True)

    relation = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    religion = models.CharField(max_length=100, null=True, blank=True)
    occupation = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)
    family_history = models.TextField(null=True, blank=True)
    investigation = models.TextField(null=True, blank=True)
    

    receipe_description = models.TextField(null=True, blank=True)
    receipe_image = models.ImageField(upload_to="receipe", null=True, blank=True)
    # Additional fields added to match the case sheet template
    age = models.IntegerField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)

    # Personal history
    appetite = models.TextField(null=True, blank=True)
    thirst = models.TextField(null=True, blank=True)
    cravings = models.TextField(null=True, blank=True)
    aversions = models.TextField(null=True, blank=True)
    bowel_habits = models.TextField(null=True, blank=True)
    urine = models.TextField(null=True, blank=True)
    sleep = models.TextField(null=True, blank=True)
    dreams = models.TextField(null=True, blank=True)
    perspiration = models.TextField(null=True, blank=True)
    thermal_reaction = models.CharField(max_length=50, null=True, blank=True)
    habits = models.TextField(null=True, blank=True)
    sexual_history = models.TextField(null=True, blank=True)

    # Menstrual / Obstetric
    menarche_age = models.CharField(max_length=50, null=True, blank=True)
    cycle = models.CharField(max_length=100, null=True, blank=True)
    flow = models.CharField(max_length=200, null=True, blank=True)
    menopause = models.CharField(max_length=100, null=True, blank=True)
    obstetric_history = models.TextField(null=True, blank=True)
    gravida = models.CharField(max_length=20, null=True, blank=True)
    para = models.CharField(max_length=20, null=True, blank=True)
    abortions = models.CharField(max_length=20, null=True, blank=True)
    full_term_deliveries = models.CharField(max_length=20, null=True, blank=True)

    # Mental generals / psychological
    mental_generals = models.TextField(null=True, blank=True)

    # General physical exam
    built = models.CharField(max_length=100, null=True, blank=True)
    height = models.CharField(max_length=50, null=True, blank=True)
    weight = models.CharField(max_length=50, null=True, blank=True)
    pulse = models.CharField(max_length=50, null=True, blank=True)
    bp = models.CharField(max_length=50, null=True, blank=True)
    temperature = models.CharField(max_length=50, null=True, blank=True)
    respiration = models.CharField(max_length=50, null=True, blank=True)
    pallor_cyanosis_edema = models.TextField(null=True, blank=True)
    tongue_nails_skin = models.TextField(null=True, blank=True)

    # Systemic exam
    respiratory_system = models.TextField(null=True, blank=True)
    cardiovascular_system = models.TextField(null=True, blank=True)
    gastrointestinal_system = models.TextField(null=True, blank=True)
    genitourinary_system = models.TextField(null=True, blank=True)
    nervous_system = models.TextField(null=True, blank=True)
    locomotor_system = models.TextField(null=True, blank=True)

    # Diagnosis / other
    allopathic_diagnosis = models.TextField(null=True, blank=True)
    miasmatic_diagnosis = models.CharField(max_length=100, null=True, blank=True)
    totality_of_symptoms = models.TextField(null=True, blank=True)
    repertorization = models.TextField(null=True, blank=True)

    # Final prescription
    chosen_remedy = models.CharField(max_length=200, null=True, blank=True)
    potency = models.CharField(max_length=50, null=True, blank=True)
    repetition = models.CharField(max_length=100, null=True, blank=True)
    basis_of_prescription = models.TextField(null=True, blank=True)
    

