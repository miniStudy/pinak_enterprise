from django.db import models

# Create your models here.
class Languages(models.Model):
    class language_choices(models.TextChoices):
        English = 'English', 'English'
        Gujarati = 'Gujarati', 'Gujarati'

    language_id = models.BigAutoField(primary_key=True)
    language_type = models.CharField(choices=language_choices, max_length=155)

    def __str__(self):
        return self.language_type

    class Meta:
        db_table = 'Languages'


class Company_Details(models.Model):
    company_id = models.BigAutoField(primary_key=True)
    company_contact_number = models.CharField(max_length=15)
    company_owner_name = models.CharField(max_length=155)
    company_owner_contact = models.CharField(max_length=15)
    company_address = models.TextField()
    company_logo = models.ImageField(upload_to='uploads/')
    company_logo_icon = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.company_owner_name

    class Meta:
        db_table = 'Company_Details'


class Bank_Details(models.Model):
    bank_id = models.BigAutoField(primary_key=True)
    bank_name = models.CharField(max_length=155)
    bank_branch = models.CharField(max_length=155)
    bank_account_number = models.IntegerField()
    bank_ifsc_code = models.CharField(max_length=55)
    bank_account_holder = models.CharField(max_length=155)  
    bank_open_closed = models.BooleanField(default=1)

    def __str__(self):
        return self.bank_name

    class Meta:
        db_table = 'Bank_Details'


class Machine_Types(models.Model):
    machine_type_id = models.BigAutoField(primary_key=True)
    machine_type_name = models.CharField(max_length=155)

    def __str__(self):
        return self.machine_type_name

    class Meta:
        db_table = 'Machine_Types'


class Company_Machines(models.Model):
    class condition_options(models.TextChoices):
        New = 'New', 'New'
        Second_hand = 'Second_hand', 'Second_hand'

    machine_id = models.BigAutoField(primary_key=True)
    machine_owner = models.CharField(max_length=155)
    machine_buy_date = models.DateField()
    machine_condition = models.CharField(choices=condition_options, max_length=55)
    machine_number_plate = models.CharField(max_length=55)
    machine_details = models.TextField()
    machine_contact_number = models.CharField(max_length=15)
    machine_sold_out_date = models.DateField(null=True, blank=True)
    machine_sold_price = models.CharField(max_length=155, null=True, blank=True)
    machine_working = models.BooleanField(default=1)
    machine_types_id = models.ForeignKey(Machine_Types, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.machine_types_id.machine_type_name} {self.machine_owner}'

    class Meta:
        db_table = 'Company_Machines'


class Working_Machines(models.Model):
    class ownership_options(models.TextChoices):
        Rent_Machine = 'Rent_Machine', 'Rent_Machine'
        Own_Machine = 'Own_Machine', 'Own_Machine'
        Company_Machine = 'Company_Machine', 'Company_Machine'

    working_machine_id = models.BigAutoField(primary_key=True)
    working_machine_name = models.CharField(max_length=155)
    working_machine_owner_name = models.CharField(max_length=155)
    working_machine_owner_contact = models.CharField(max_length=15)
    working_machine_plate_number = models.CharField(max_length=55)
    working_machine_start_date = models.DateField(null=True, blank=True)
    working_machine_end_date = models.DateField(null=True, blank=True)
    working_machine_ownership = models.CharField(choices=ownership_options, max_length=55)
    working_machine_details = models.TextField()
    working_machine_rented_amount = models.CharField(max_length=55, null=True, blank=True)
    machine_type_id = models.ForeignKey(Machine_Types, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.working_machine_name} {self.working_machine_owner_name}'

    class Meta:
        db_table = 'Working_Machines'
    

class Maintenance_Types(models.Model):
    maintenance_type_id = models.BigAutoField(primary_key=True)
    maintenance_type_name = models.CharField(max_length=155)

    def __str__(self):
        return f'{self.maintenance_type_name}'

    class Meta:
        db_table = 'Maintenance_Types'


class Machine_Maintenance(models.Model):
    class paid_options(models.TextChoices):
        Machine_Owner = 'Machine_Owner', 'Machine_Owner'
        Pinak_Enterprise = 'Pinak_Enterprise', 'Pinak_Enterprise'
        Pinak = 'Pinak', 'Pinak'

    machine_maintenance_id = models.BigAutoField(primary_key=True)
    machine_maintenance_amount = models.CharField(max_length=155)
    machine_maintenance_date = models.DateField()
    machine_maintenance_amount_paid = models.BooleanField(default=0)
    machine_maintenance_amount_paid_by = models.CharField(choices=paid_options, max_length=55)
    machine_maintenance_person = models.CharField(max_length=155)
    machine_maintenance_contact = models.CharField(max_length=15)
    machine_maintenance_driver = models.CharField(max_length=155)
    machine_maintenance_details = models.TextField()
    machine_maintenance_types_id = models.ForeignKey(Maintenance_Types, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.machine_maintenance_types_id.maintenance_type_name} {self.machine_maintenance_amount}'

    class Meta:
        db_table = 'Machine_Maintenance'


class Project_Types(models.Model):
    project_type_id = models.BigAutoField(primary_key=True)
    project_type_name = models.CharField(max_length=155)
    project_type_details = models.TextField()

    def __str__(self):
        return f'{self.project_type_name}'

    class Meta:
        db_table = 'Project_Types'


class Project(models.Model):
    class status_options(models.TextChoices):
        Ongoing = 'Ongoing', 'Ongoing'
        Closed = 'Closed', 'Closed'
        Taken = 'Taken', 'Taken'

    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=155)
    project_start_date = models.DateField(null=True, blank=True)
    project_end_date = models.DateField(null=True, blank=True)
    project_amount= models.CharField(max_length=55, null=True, blank=True)
    project_location = models.CharField(max_length=155, null=True, blank=True)
    project_company_name = models.CharField(max_length=155)
    project_person_name = models.CharField(max_length=155)
    project_status = models.CharField(choices=status_options, max_length=55)
    project_types_id = models.ForeignKey(Project_Types, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.project_types_id.project_type_name} {self.project_name}'

    class Meta:
        db_table = 'Project'


class Pay_Types(models.Model):
    pay_type_id = models.BigAutoField(primary_key=True)
    pay_type_name = models.CharField(max_length=155)
    pay_type_date = models.DateField()

    def __str__(self):
        return f'{self.pay_type_name}'

    class Meta:
        db_table = 'Pay_Types'


class Person_Type(models.Model):
    person_type_id = models.BigAutoField(primary_key=True)
    person_type_name = models.CharField(max_length=155)

    def __str__(self):
        return f'{self.person_type_name}'

    class Meta:
        db_table = 'Person_Type'


class Person(models.Model):
    class work_options(models.TextChoices):
        Worker = 'Worker', 'Worker'
        Project = 'Project', 'Project'
        Material = 'Material', 'Material'
        Machine = 'Machine', 'Machine'
        Bhatthu = 'Bhatthu', 'Bhatthu'
        Other = 'Other', 'Other'

    person_id = models.BigAutoField(primary_key=True)
    person_name = models.CharField(max_length=155)
    person_contact_number = models.CharField(max_length=15)
    person_work_type = models.CharField(choices=work_options, max_length=155)
    person_type_id = models.ForeignKey(Person_Type, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.person_type_id.person_type_name} {self.person_name}'

    class Meta:
        db_table = 'Person'


class Work_Types(models.Model):
    work_type_id = models.BigAutoField(primary_key=True)
    work_type_name = models.CharField(max_length=155)
    work_type_details = models.TextField()

    def __str__(self):
        return f'{self.work_type_name}'

    class Meta:
        db_table = 'Work_Types'


class Person_Work_Machine(models.Model):
    class payment_options(models.TextChoices):
        Company_Owner = 'Company_Owner', 'Company_Owner'
        Pinak_Enterprise = 'Pinak_Enterprise', 'Pinak_Enterprise'
        Pinak = 'Pinak', 'Pinak'

    pwm_id = models.BigAutoField(primary_key=True)
    pwm_machine_name = models.CharField(max_length=155)
    pwm_machine_owner_name = models.CharField(max_length=155)
    pwm_machine_owner_number = models.CharField(max_length=15)
    working_machine_id = models.ForeignKey(Working_Machines, on_delete=models.CASCADE)
    pwm_person_joining_date = models.DateField(null=True, blank=True)
    pwm_person_contact_number = models.CharField(max_length=15)
    pwm_person_payment_by = models.CharField(choices=payment_options, max_length=155)
    pwm_person_payment_desc = models.TextField(null=True, blank=True)
    person_type_id = models.ForeignKey(Person_Type, on_delete=models.CASCADE)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    project_type_id = models.ForeignKey(Project_Types, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    work_types_id = models.ForeignKey(Work_Types, on_delete=models.CASCADE)
    pwm_work_number = models.CharField(max_length=55)
    pwm_work_amount = models.CharField(max_length=55)
    pwm_total_amount = models.CharField(max_length=55)
    pwm_work_desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.pwm_machine_name} {self.pwm_machine_owner_name}'

    class Meta:
        db_table = 'Person_Work_Machine'


class Material_Types(models.Model):
    material_type_id = models.BigAutoField(primary_key=True)
    material_type_name = models.CharField(max_length=155)

    def __str__(self):
        return f'{self.material_type_name}'

    class Meta:
        db_table = 'Material_Types'


class Materials(models.Model):
    material_id = models.BigAutoField(primary_key=True)
    material_owner_name = models.CharField(max_length=155)
    material_used_date = models.DateField(null=True, blank=True)
    material_type_id = models.ForeignKey(Material_Types, on_delete=models.CASCADE)
    work_type_id = models.ForeignKey(Work_Types, on_delete=models.CASCADE)
    material_work_number = models.CharField(max_length=55)
    material_work_amount = models.CharField(max_length=55)
    material_work_total_amount = models.CharField(max_length=55)
    total_material_amount = models.CharField(max_length=55)
    material_desc = models.TextField(null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.material_type_id.material_type_name} {self.material_owner_name}'

    class Meta:
        db_table = 'Materials'

class Document_Types(models.Model):
    document_type_id = models.BigAutoField(primary_key=True)
    document_type_name = models.CharField(max_length=155)

    def __str__(self):
        return f'{self.document_type_name}'

    class Meta:
        db_table = 'Document_Types'

class Documents(models.Model):
    document_id = models.BigAutoField(primary_key=True)
    document_name = models.CharField(max_length=155)
    document_date = models.DateField(auto_now_add=True)
    document_unique_code = models.CharField(max_length=155, unique=True)
    document_file = models.FileField(upload_to='uploads/')
    document_type_id = models.ForeignKey(Document_Types, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.document_type_id.document_type_name} {self.document_name}'

    class Meta:
        db_table = 'Documents'


