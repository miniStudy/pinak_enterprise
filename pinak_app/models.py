from django.db import models

# Create your models here.

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
        db_table = 'company_details'



# Company Details Model
#  - company_name
#  - company_contact_number
#  - owner_name
#  - owner_contact_number
#  - company_address
#  - company_logo1
#  - company_logo_icon


# Bank Deatils Model
#  - bank_name
#  - bank_branch
#  - branch_ifsc
#  - bank_account_holder_name
#  - bank_account_number
#  - open_or_closed


# Machine Types Model
#  - machine_names_type


# Machine Owned By Company Model
#  - machine_owner
#  - machine_price
#  - machine_buy_date
#  - machine_condition choies-['new-buy', 'second-hand-buy']
#  - machine_number_plate
#  - machine_type (Foreignkey)
#  - machine_details 
#  - machine_contact_number
#  - machine_sold_out_date null,black=True
#  - machine_sold_price
#  - machine_working - Boolean

# Working Machines Model
#  - machine_ownership choies-['rented_machine', 'own_machine', 'company_machine']
#  - machine_working_start_date
#  - machine_working_end_date
#  - machine_number_plate
#  - machine_types (ForeignKey)
#  - machine_name 
#  - machine_details
#  - machine_owner_name
#  - machine_owner_contact_number
#  - machine_rented_amount (null,blank=True)


# Maintenance Types Model
#  - maintenance_names 


# Machine Maintenance Model
#  - machine_maintenance_date
#  - machine_maintenance_paid_by choies-['machine_owner', 'pinak_enterprise', 'pinak]
#  - machine_maintenance_amount_paid Boolean-paid n not-paid 
#  - machine_maintenance_amount
#  - machine_maintenance_types (ForeignKey)
#  - machine_maintenance_details
#  - machine_maintenance_present_person_name
#  - machine_maintenance_present_person_contact_number
#  - machine_maintenance_driver_name

# Project Types Model
#  - project_names
#  - project_details

# Project Model
#  - project_types (ForeignKey)
#  - project_location
#  - project_start_date
#  - project_end_date
#  - project_status choices-['ongoing', 'closed', 'taken']
#  - project_amount (null=True, blank=True)
#  - project_company_name 
#  - project_person_name

# Pay types Model 
#  - pay_type_name 
#  - pay_type_date


# Person Types Model
#  - person_type_name

# Person Model
#  - person_work_type choices-['worker', 'project', 'material', 'machine', 'bhatthu', 'other']
#  - person_type (ForeignKey)
#  - person_name
#  - person_contact_number


# Works Types Model
#  - works_types_name
#  - works_types_detail



# Person_N_Work_N_Machine
#  - project_type (ForeignKey)
#  - project_id (Project ForeignKey)
#  - person_joining_date
#  - person_type (ForeignKey)
#  - person (ForeignKey)
#  - person_contact_number
#  - person_payment_by choices-['company_owner', 'pinak', 'pinak_enterprise']
#  - person_payment_description
#  - machine_name 
#  - machine_owner_name
#  - machine_contact_number
#  - machine_
#  - work_type (ForeignKey)
#  - work_number
#  - work_amount
#  - total_amount
#  - description

# Materials Names Types Model
#  - material_type_name


# Material Model
#  - material_name (ForeignKey)
#  - material_owner_name
#  - material_used_date
#  - material_work_type (ForeignKey)
#  - material_work_number
#  - material_work_amount
#  - material_work_total_amount
#  - total_material_amount
#  - material_desc
#  - project_id (ForeignKey)