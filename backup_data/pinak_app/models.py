from django.db import models

# Create your models here.
class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.CharField(max_length=155)
    user_email = models.EmailField()
    user_contact = models.CharField(max_length=15)
    user_password = models.CharField(max_length=55)
    user_otp = models.CharField(max_length=6, null=True, blank=True)

    def __str__(self):
        return self.user_email

    class Meta:
        db_table = 'User'

class Notification(models.Model):
    notification_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    notification_title = models.CharField(max_length=55)
    notification_msg = models.CharField(max_length=255)
    notification_date = models.DateField(auto_now_add=True)


    def __str__(self):
        return self.user_id.user_email

    class Meta:
        db_table = 'Notification'


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
    company_logo = models.ImageField(upload_to='uploads/', null=True, blank=True)
    company_logo_icon = models.ImageField(upload_to='uploads/', null=True, blank=True)
    company_sharuaati_shilak = models.FloatField(default=0.0,null=True,blank=True)
    
    def __str__(self):
        return self.company_owner_name

    class Meta:
        db_table = 'Company_Details'


class Person_Type(models.Model):
    person_type_id = models.BigAutoField(primary_key=True)
    person_type_name = models.CharField(max_length=155)

    def __str__(self):
        return f'{self.person_type_name}'

    class Meta:
        db_table = 'Person_Type'

        
class Machine_Types(models.Model):
    machine_type_id = models.BigAutoField(primary_key=True)
    machine_type_name = models.CharField(max_length=155)

    def __str__(self):
        return self.machine_type_name

    class Meta:
        db_table = 'Machine_Types'


class Project_Types(models.Model):
    project_type_id = models.BigAutoField(primary_key=True)
    project_type_name = models.CharField(max_length=155)
    project_type_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.project_type_name}'

    class Meta:
        db_table = 'Project_Types'


class Work_Types(models.Model):
    work_type_id = models.BigAutoField(primary_key=True)
    work_type_name = models.CharField(max_length=155)

    def __str__(self):
        return f'{self.work_type_name}'

    class Meta:
        db_table = 'Work_Types'


class Material_Types(models.Model):
    material_type_id = models.BigAutoField(primary_key=True)
    material_type_name = models.CharField(max_length=155)

    def __str__(self):
        return f'{self.material_type_name}'

    class Meta:
        db_table = 'Material_Types'


class Maintenance_Types(models.Model):
    maintenance_type_id = models.BigAutoField(primary_key=True)
    maintenance_type_name = models.CharField(max_length=155)

    def __str__(self):
        return f'{self.maintenance_type_name}'

    class Meta:
        db_table = 'Maintenance_Types'


class Pay_Types(models.Model):
    pay_type_id = models.BigAutoField(primary_key=True)
    pay_type_name = models.CharField(max_length=155)

    def __str__(self):
        return f'{self.pay_type_name}'

    class Meta:
        db_table = 'Pay_Types'


class Document_Types(models.Model):
    document_type_id = models.BigAutoField(primary_key=True)
    document_type_name = models.CharField(max_length=155)

    def __str__(self):
        return f'{self.document_type_name}'

    class Meta:
        db_table = 'Document_Types'


class Person(models.Model):
    class project_person_options(models.TextChoices):
        Worker = 'Worker', 'Worker'
        Project = 'Project', 'Project'
        Material = 'Material', 'Material'
        Machine = 'Machine', 'Machine'
        Other = 'Other', 'Other'

    person_id = models.BigAutoField(primary_key=True)
    person_name = models.CharField(max_length=155)
    person_contact_number = models.CharField(max_length=15)
    person_register_date = models.DateField(auto_now_add=True)
    person_status = models.BooleanField(default=1)
    person_address = models.TextField(null=True, blank=True)
    person_other_details = models.TextField(null=True, blank=True)
    person_business_job_name = models.CharField(max_length=255, null=True, blank=True)
    person_business_job_company_num = models.CharField(max_length=15, null=True, blank=True)
    person_business_job_address = models.TextField(null=True, blank=True)
    person_gst = models.CharField(max_length=155, null=True, blank=True)
    person_type_id = models.ForeignKey(Person_Type, on_delete=models.CASCADE, null=True, blank=True)
    person_types_for_project = models.CharField(choices=project_person_options, max_length=155, null=True, blank=True)
    person_salary = models.CharField(max_length=150, null=True, blank=True)
    person_khatu = models.FloatField(default=0)

    def __str__(self):
        return f'{self.person_type_id.person_type_name} {self.person_name}'

    class Meta:
        db_table = 'Person'


class Bank_Details(models.Model):
    bank_id = models.BigAutoField(primary_key=True)
    bank_name = models.CharField(max_length=155)
    bank_branch = models.CharField(max_length=155)
    bank_account_number = models.CharField(max_length=100)
    bank_ifsc_code = models.CharField(max_length=55)
    bank_account_holder = models.CharField(max_length=155, null=True, blank=True)  
    bank_initial_amount = models.FloatField(max_length=155, null=True, blank=True)
    bank_open_closed = models.BooleanField(default=1)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    company_bank_account = models.BooleanField(default=0)
    bank_current_amount = models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.bank_name

    class Meta:
        db_table = 'Bank_Details'


class Salary(models.Model):
    salary_id = models.BigAutoField(primary_key=True)
    salary_date = models.DateField(null=True, blank=True) # null and blank should be removed
    salary_amount = models.CharField(max_length=155)
    salary_working_days = models.CharField(max_length=155)
    salary_details = models.TextField(null=True, blank=True)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.person_id.person_name} {self.salary_amount}'

    class Meta:
        db_table = 'Salary'



class Machines(models.Model):
    class condition_options(models.TextChoices):
        New = 'New', 'New'
        Second_hand = 'Second_hand', 'Second_hand'

    class own_options(models.TextChoices):
        Company = 'Company', 'Company'
        Rented_fixedprice = 'Rented_fixedprice', 'Rented_fixedprice'
        Rented_variableprice = 'Rented_variableprice', 'Rented_variableprice'

    machine_id = models.BigAutoField(primary_key=True)
    machine_name = models.CharField(max_length=155)
    machine_number_plate = models.CharField(max_length=55)
    machine_register_date = models.DateField(auto_now_add=True,null=True,blank=True)
    machine_own = models.CharField(choices=own_options, max_length=55)
    machine_condition = models.CharField(choices=condition_options, max_length=55, null=True, blank=True)
    machine_working = models.BooleanField(default=1)
    machine_types_id = models.ForeignKey(Machine_Types, on_delete=models.CASCADE)
    machine_details = models.TextField(null=True, blank=True)
    machine_owner_id = models.ForeignKey(Person, on_delete=models.CASCADE,null=True,blank=True)
    machine_buy_price = models.CharField(max_length=155, null=True, blank=True)
    machine_buy_date = models.DateField(null=True, blank=True)
    machine_sold_price = models.CharField(max_length=155, null=True, blank=True)
    machine_sold_out_date = models.DateField(null=True, blank=True)
    machine_other_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.machine_name} {self.machine_number_plate}'

    class Meta:
        db_table = 'Machines'



class Project(models.Model):
    class status_options(models.TextChoices):
        Ongoing = 'Ongoing', 'Ongoing'
        Closed = 'Closed', 'Closed'
        Taken = 'Taken', 'Taken'

    class agent_type(models.TextChoices):
        Percentage = 'Percentage', 'Percentage',
        Fixed = 'Fixed', 'Fixed',

    project_id = models.BigAutoField(primary_key=True)
    project_name = models.CharField(max_length=155)
    project_amount= models.CharField(max_length=55, null=True, blank=True)
    project_location = models.CharField(max_length=155)
    project_types_id = models.ForeignKey(Project_Types, on_delete=models.CASCADE)
    project_status = models.CharField(choices=status_options, max_length=55)
    project_start_date = models.DateField(auto_now_add=True, null=True, blank=True)
    project_end_date = models.DateField(auto_now_add=True, null=True, blank=True)
    project_owner_name = models.ForeignKey(Person, on_delete=models.CASCADE ,null=True,blank=True, related_name='owner_name')
    project_cgst = models.CharField(max_length=55, null=True, blank=True)
    project_sgst = models.CharField(max_length=55, null=True, blank=True)
    project_tax = models.CharField(max_length=55, null=True, blank=True)
    project_discount = models.CharField(max_length=55, null=True, blank=True)
    project_grahak_amount = models.FloatField(null=True,blank=True)
    project_agent = models.BooleanField(default=0)
    project_agent_id = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True, related_name='agent_name')
    project_agent_type = models.CharField(choices=agent_type, max_length=155, null=True, blank=True)
    project_agent_percentage = models.CharField(max_length=155, null=True, blank=True)
    project_agent_fixed_amount = models.CharField(max_length=155, null=True, blank=True)
    


    project_investor = models.BooleanField(default=0)
    project_investor_id = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True, related_name='investor_name')
    project_investor_percentage = models.CharField(max_length=155, null=True, blank=True)
    project_investor_amount = models.FloatField(max_length=155, null=True, blank=True)

    project_padatar_rakam = models.FloatField(null=True,blank=True)
    project_dalali_rakam = models.FloatField(null=True,blank=True)
    project_investor_rakam = models.FloatField(null=True,blank=True)

    project_final_amount = models.CharField(max_length=155, null=True, blank=True)

    def __str__(self):
        return f'{self.project_types_id.project_type_name} {self.project_name}'

    class Meta:
        db_table = 'Project'

class Project_Machine_Data(models.Model):
    project_machine_data_id = models.BigAutoField(primary_key=True)
    project_machine_date = models.DateField(auto_now_add=True, null=True, blank=True)
    machine_project_id = models.ForeignKey(Machines, on_delete=models.CASCADE)
    work_type_id = models.ForeignKey(Work_Types, on_delete=models.CASCADE)
    project_machine_data_work_number = models.CharField(max_length=155)
    project_machine_data_work_price = models.CharField(max_length=155)
    project_machine_data_total_amount = models.CharField(max_length=155)
    project_machine_data_work_details = models.TextField(null=True, blank=True)
    project_machine_data_more_details = models.TextField(null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.project_machine_data_id}'

    class Meta:
        db_table = 'Project_Machine_Data'
    

class Project_Person_Data(models.Model):
    class paid_by_options(models.TextChoices):
        Project_Owner = 'Project_Owner', 'Project_Owner'
        Pinak = 'Pinak', 'Pinak'
        Office = 'Office', 'Office'
    project_person_id = models.BigAutoField(primary_key=True)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    project_person_date = models.DateField(auto_now_add=True, null=True, blank=True)
    work_type_id = models.ForeignKey(Work_Types, on_delete=models.CASCADE)
    project_machine_data_id = models.ForeignKey(Project_Machine_Data, on_delete=models.CASCADE, null=True, blank=True)
    project_person_work_num = models.CharField(max_length=55)
    project_person_price = models.FloatField()
    project_person_total_price = models.FloatField()
    project_person_paid_by = models.CharField(choices=paid_by_options, max_length=155)
    project_person_payment_details = models.TextField(null=True, blank=True)
    project_person_more_details = models.TextField(null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    bank_id = models.ForeignKey(Bank_Details, on_delete=models.CASCADE,null=True,blank=True)
    person_payment_mode = models.CharField(max_length=155, null=True,blank=True)

    def __str__(self):
        return f'{self.project_person_id}'

    class Meta:
        db_table = 'Project_Person_Data'


class Machine_Maintenance(models.Model):
    class paid_options(models.TextChoices):
        Project_Owner = 'Project_Owner', 'Project_Owner'
        Office = 'Office', 'Office'
        Pinak = 'Pinak', 'Pinak'
        machine_owner = 'machine_owner','machine_owner'

    machine_maintenance_id = models.BigAutoField(primary_key=True)
    machine_machine_id = models.ForeignKey(Machines, on_delete=models.CASCADE,null=True, blank=True)
    machine_maintenance_amount = models.FloatField(max_length=155)
    machine_maintenance_date = models.DateField(auto_now_add=True, null=True, blank=True)
    machine_maintenance_amount_paid_by = models.CharField(choices=paid_options, max_length=55)
    machine_maintenance_amount_paid = models.BooleanField(default=0)
    machine_maintenance_types_id = models.ForeignKey(Maintenance_Types, on_delete=models.CASCADE)
    machine_maintenance_details = models.TextField(null=True, blank=True)
    machine_maintenance_driver_id = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True, related_name="driver")
    machine_maintenance_person_id = models.ForeignKey(Person, on_delete=models.CASCADE, null=True, blank=True, related_name="repair_person")
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.machine_maintenance_types_id.maintenance_type_name} {self.machine_maintenance_amount}'

    class Meta:
        db_table = 'Machine_Maintenance'


class Money_Debit_Credit(models.Model):
    class payment_options(models.TextChoices):
        CASH = 'CASH', 'CASH'
        BANK = 'BANK', 'BANK'
    money_id = models.BigAutoField(primary_key=True)
    sender_person_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='sender_person_id')
    receiver_person_id = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='receiver_person_id')
    pay_type_id = models.ForeignKey(Pay_Types, on_delete=models.CASCADE)
    money_payment_mode = models.CharField(choices=payment_options, max_length=155)
    money_amount = models.FloatField()
    money_date = models.DateField()
    sender_bank_id = models.ForeignKey(Bank_Details, on_delete=models.CASCADE, related_name='sender_bank_id', null=True, blank=True)
    money_sender_cheque_no = models.CharField(max_length=155, null=True, blank=True)
    receiver_bank_id = models.ForeignKey(Bank_Details, on_delete=models.CASCADE, related_name='receiver_bank_id',null=True, blank=True)
    money_payment_details = models.TextField(null=True, blank=True)
    machine_id = models.ForeignKey(Machines, on_delete=models.CASCADE, null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True,blank=True)
    def __str__(self):
        return f'{self.money_id}'

    class Meta:
        db_table = 'Money_Debit_Credit'


class Material_Owner_data(models.Model):
    Material_Owner_id = models.BigAutoField(primary_key=True)
    material_owner_person_id = models.ForeignKey(Person, on_delete=models.CASCADE)
    Material_Owner_status = models.BooleanField(default=1)
    Material_Owner_location = models.TextField(null=True, blank=True)
    Material_Owner_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.material_owner_person_id.person_name}'

    class Meta:
        db_table = 'Material_Owner_data'




class Material(models.Model):
    material_id = models.BigAutoField(primary_key=True)
    material_type_id = models.ForeignKey(Material_Types, on_delete=models.CASCADE)
    material_owner = models.ForeignKey(Person, on_delete=models.CASCADE)
    material_status = models.BooleanField(default=1,null=True,blank=True)
    material_buy_date = models.DateField(null=True,blank=True)
    material_buy_location = models.TextField(null=True, blank=True)
    material_work_type = models.ForeignKey(Work_Types, on_delete=models.CASCADE)
    material_work_no = models.FloatField(max_length=100,null=True,blank=True)
    material_price = models.FloatField(max_length=250,blank=True,null=True)
    material_total_price = models.FloatField(max_length=250,null=True,blank=True)
    material_is_agent = models.BooleanField(default=0)
    material_agent_person = models.ForeignKey(Person, on_delete=models.CASCADE,null=True,blank=True,related_name='material_agent_person')
    material_agent_name = models.CharField(max_length=100,null=True,blank=True)
    material_agent_contact = models.CharField(max_length=100,null=True,blank=True)
    material_agent_price_choice = models.CharField(max_length=50,null=True,blank=True)
    material_agent_percentage = models.CharField(max_length=10,null=True,blank=True)
    material_agent_amount = models.FloatField(max_length=200,null=True,blank=True)
    material_final_amount = models.FloatField(max_length=200,null=True,blank=True)
    material_details = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.material_type_id.material_type_name}'

    class Meta:
        db_table = 'Material'


class Project_Day_Details(models.Model):
    project_day_detail_id = models.BigAutoField(primary_key=True)
    proejct_day_detail_date = models.DateField(auto_now_add=True, null=True, blank=True)
    project_day_detail_machine_id = models.ForeignKey(Machines, on_delete=models.CASCADE,null=True,blank=True)
    project_day_detail_work_type = models.ForeignKey(Work_Types, on_delete=models.CASCADE)
    project_day_detail_total_tyres = models.CharField(max_length=55, null=True, blank=True)
    project_day_detail_work_no = models.CharField(max_length=155)
    project_day_detail_price = models.CharField(max_length=155)
    project_day_detail_total_price = models.FloatField(max_length=155)
    project_day_detail_details = models.TextField(null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    def __str__(self):
        return f'{self.project_day_detail_machine_id.machine_name} {self.project_day_detail_work_type.work_type_name}'

    class Meta:
        db_table = 'Project_Day_Details'


class Project_Material_Data(models.Model):
    project_material_id = models.BigAutoField(primary_key=True)
    project_material_date = models.DateField(auto_now_add=True, null=True, blank=True)
    project_material_material_id = models.ForeignKey(Material_Owner_data, on_delete=models.CASCADE)
    project_material_material_type_id = models.ForeignKey(Material_Types, on_delete=models.CASCADE)
    project_material_work_type_id = models.ForeignKey(Work_Types, on_delete=models.CASCADE)
    project_material_work_no = models.CharField(max_length=155)
    project_material_price = models.CharField(max_length=155)
    project_material_total_amount = models.CharField(max_length=155)
    person_material_information = models.TextField(null=True, blank=True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.project_material_id}'

    class Meta:
        db_table = 'Project_Material_Data'



class Documents(models.Model):
    document_id = models.BigAutoField(primary_key=True)
    document_name = models.CharField(max_length=155)
    document_date = models.DateField(auto_now_add=True)
    document_unique_code = models.CharField(max_length=155, unique=True)
    document_file = models.FileField(upload_to='uploads/')
    document_type_id = models.ForeignKey(Document_Types, on_delete=models.CASCADE)
    person_id = models.ForeignKey(Person, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return f'{self.document_type_id.document_type_name} {self.document_name}'

    class Meta:
        db_table = 'Documents'



class Project_Expense(models.Model):
    class payment_options_field(models.TextChoices):
        Cash = 'Cash', 'Cash'
        Bank = 'Bank', 'Bank'
    project_expense_id = models.BigAutoField(primary_key=True)
    project_expense_name = models.CharField(max_length=155)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    project_expense_date = models.DateField(auto_now_add=True, null=True, blank=True)
    project_expense_amount = models.FloatField()
    project_payment_mode = models.CharField(choices=payment_options_field, max_length=155)
    bank_id = models.ForeignKey(Bank_Details, on_delete=models.CASCADE,null=True,blank=True)
    project_expense_desc = models.TextField()

    def __str__(self):
        return f'{self.project_expense_name}'

    class Meta:
        db_table = 'Project_Expense'        


class Document_Dates(models.Model):
    dd_id = models.BigAutoField(primary_key=True)
    dd_document = models.ForeignKey(Documents, on_delete=models.CASCADE, null=True,blank=True)
    dd_date_name = models.CharField(max_length=200)
    dd_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.dd_date_name}'

    class Meta:
        db_table = 'Document_Dates'



class bank_cash(models.Model):
    bank_cash_id = models.BigAutoField(primary_key=True)
    credit_debit = models.CharField(max_length=100)
    amount = models.IntegerField()
    bank_id = models.ForeignKey(Bank_Details, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    details = models.TextField(null=True,blank=True)

    def __str__(self):
        return f'{self.date} {self.bank_id.bank_name} {self.amount}'

    class Meta:
        db_table = 'bank_cash'


class language(models.Model):
    language_id = models.BigAutoField(primary_key=True)
    gujarati = models.CharField(max_length=200)
    english = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.language_id} - {self.english} {self.gujarati}'

    class Meta:
        db_table = 'language'


class Settingsss(models.Model):
    settings_id = models.BigAutoField(primary_key=True)
    settings_field_name = models.CharField(max_length=200)
    settings_field_value = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.settings_field_name} - {self.settings_field_value}'

    class Meta:
        db_table = 'Settingsss'


class diary(models.Model):
    diary_id = models.BigAutoField(primary_key=True)
    diary_text = models.TextField()

    def __str__(self):
        return f'{self.diary_text}'

    class Meta:
        db_table = 'diary'

class machine_rent(models.Model):
    machine_rent_id = models.BigAutoField(primary_key=True)
    machine_rent_machine_id = models.ForeignKey(Machines, on_delete=models.CASCADE)
    machine_rented_work_type = models.ForeignKey(Work_Types, models.CASCADE, null=True,blank=True)
    machine_rented_work_price = models.CharField(max_length=150, null=True,blank=True)
    machine_km = models.CharField(max_length=100,null=True,blank=True)
    rent_start_date = models.DateField(auto_now_add=True,null=True,blank=True)
    rent_end_date = models.DateField(null=True,blank=True)
    rent_amount = models.FloatField(null=True,blank=True)
        
    def __str__(self):
        return f'{self.machine_rent_machine_id.machine_name}'

    class Meta:
        db_table = 'machine_rent'



class Bill(models.Model):
    bill_id = models.BigAutoField(primary_key=True)
    invoice_number = models.CharField(max_length=100,null=True,blank=True)
    is_tax = models.BooleanField(default=0)
    Project_id = models.ForeignKey(Project,null=True,blank=True,on_delete=models.CASCADE)
    invoice_date = models.DateField(auto_now_add=True,null=True,blank=True)

    def __str__(self):
        return f'{self.invoice_number}'

    class Meta:
        db_table = 'Bill'



#Add Expiry Date for Document
#Add Service Date for Vehicle Data
#Day Wise kM for vehicle



# Notification model

# user_id
# notification Data 
# notification title
# date
