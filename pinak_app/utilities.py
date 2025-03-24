from pinak_app.models import *
from django.db.models import *
from django.db.models.functions import Cast
from django.conf import settings
from rest_framework.response import Response


def single_project_functionality(project_id):
    
    project = Project.objects.get(project_id=project_id)    
    # Construct a dictionary with all data, including related fields
    project_data = {
        "project_id": project.project_id,
        "project_name": project.project_name,
        "project_amount": project.project_amount,
        "project_location": project.project_location,
        "project_type_name": project.project_types_id.project_type_name,
        "project_status": project.project_status,
        "project_start_date": project.project_start_date,
        "project_end_date": project.project_end_date,
        "project_owner_name": project.project_owner_name.person_name if project.project_owner_name else None,
        "project_owner_contact_number": project.project_owner_name.person_contact_number if project.project_owner_name else None,
        "project_cgst": project.project_cgst,
        "project_sgst": project.project_sgst,
        "project_tax": project.project_tax,
        "project_discount": project.project_discount,
        "project_agent_name": project.project_agent_id.person_name if project.project_agent_id else None,
        "project_investor_name": project.project_investor_id.person_name if project.project_investor_id else None,
        "project_investor_percentage":int(project.project_investor_percentage) if project.project_investor_percentage else 0,
        "project_investor_amount":int(project.project_investor_amount) if project.project_investor_amount else 0,
        "project_investor":project.project_investor,
    }

    day_detail_total_amt = Project_Day_Details.objects.filter(project_id__project_id = project.project_id).aggregate(
        total_amount=Sum('project_day_detail_total_price')
    )['total_amount']
    day_detail_total_amt = day_detail_total_amt if day_detail_total_amt else 0

    project_material_total_amount = Project_Material_Data.objects.filter(project_id__project_id = project.project_id).aggregate(
        total_amount=Sum('project_material_total_amount')
    )['total_amount']
    project_material_total_amount = project_material_total_amount if project_material_total_amount else 0

    project_expense_total_amount = Project_Expense.objects.filter(project_id__project_id = project.project_id).aggregate(
        total_amount=Sum('project_expense_amount')
    )['total_amount']
    project_expense_total_amount = project_expense_total_amount if project_expense_total_amount else 0


    project_machine_total_amount = Project_Machine_Data.objects.filter(project_id__project_id = project.project_id).aggregate(
        total_amount=Sum('project_machine_data_total_amount')
    )['total_amount']
    project_machine_total_amount = project_machine_total_amount if project_machine_total_amount else 0


    project_machine_maintenance_total_amount = Machine_Maintenance.objects.filter(project_id__project_id = project.project_id).aggregate(
        total_amount=Sum('machine_maintenance_amount')
    )['total_amount']
    project_machine_maintenance_total_amount = project_machine_maintenance_total_amount if project_machine_maintenance_total_amount else 0

    project_person_total_amount = Project_Person_Data.objects.filter(project_id__project_id = project.project_id).aggregate(
        total_amount=Sum('project_person_total_price')
    )['total_amount']
    project_person_total_amount = project_person_total_amount if project_person_total_amount else 0


    grahak_paid_amount_for_project = Money_Debit_Credit.objects.filter(project_id__project_id = project.project_id, receiver_person_id__person_id=1).aggregate(
        total_amount=Sum('money_amount')
    )['total_amount']
    grahak_paid_amount_for_project = grahak_paid_amount_for_project if grahak_paid_amount_for_project else 0


    dalali_amt = 0
    if project.project_agent:
        if project.project_agent_type == 'Percentage':
            dalali_amt = (float(project.project_agent_percentage)*int(day_detail_total_amt))/100

        else:
            dalali_amt= int(project.project_agent_fixed_amount)

    print(dalali_amt)

    mudirokan_amt = 0
    mudirokankar_bhag_amount = 0
    if project.project_investor:
        mudirokan_amt = int(project.project_investor_amount)

    discount = int(project.project_discount) if project.project_discount else 0

    padatar_rakam = project_material_total_amount + project_expense_total_amount + project_machine_total_amount + project_machine_maintenance_total_amount + project_person_total_amount + dalali_amt

    profit_loss_onproject = day_detail_total_amt - padatar_rakam - discount
    
    profit_loss_onproject_with_investor = profit_loss_onproject + mudirokan_amt
    if project.project_investor:
        if profit_loss_onproject_with_investor != 0:
            mudirokankar_bhag_amount = (int(project.project_investor_percentage)*int(profit_loss_onproject_with_investor))/100
    
    profit_loss = profit_loss_onproject_with_investor - mudirokankar_bhag_amount
    total_chukvel_amt = project_expense_total_amount + project_person_total_amount

    grahak_kul_rakam = day_detail_total_amt - discount

    project.project_amount = grahak_kul_rakam
    project.project_padatar_rakam= padatar_rakam
    project.project_dalali_rakam= dalali_amt
    project.project_investor_rakam= mudirokankar_bhag_amount
    project.save()


    project_saransh = {
        'profit_loss':profit_loss,
        'padatar_rakam':padatar_rakam,
        'kul_chukvel_rakam':total_chukvel_amt,
        'machine_kharch':project_machine_total_amount,
        'maramat_kharch':project_machine_maintenance_total_amount,
        'vyakti_kharch':project_person_total_amount,
        'material_kharch':project_material_total_amount,
        'sareras_kharch':project_expense_total_amount,
        'grahak_kul_rakam':grahak_kul_rakam,
        'discount':discount,
        'dalali_amt':dalali_amt,
        'mudirokan_amt':mudirokan_amt,
        'mudirokankar_bhag_amount':mudirokankar_bhag_amount,
        'grahak_paid_amount_for_project':grahak_paid_amount_for_project,
        'profit_loss_onproject':profit_loss_onproject,
        'profit_loss_onproject_with_investor':profit_loss_onproject_with_investor

    }
    
    return ({"status": "success", "data": project_data,"title":project.project_name,"project_saransh":project_saransh})






def currentbank_amount(request,bank_id):
    if Bank_Details.objects.filter(bank_id = bank_id).count()>0:
        bank_instance = Bank_Details.objects.get(bank_id = bank_id)
        initial_amount = bank_instance.bank_initial_amount
        print('initialamount',initial_amount)
        credit_in_bank = bank_cash.objects.filter(bank_id__bank_id=bank_id, credit_debit='Credit').aggregate(total=Sum('amount'))['total'] or 0  
        print(credit_in_bank)    
        debit_in_bank = bank_cash.objects.filter(bank_id__bank_id=bank_id,credit_debit='Debit').aggregate(total=Sum('amount'))['total'] or 0
        bnak_transfer = credit_in_bank-debit_in_bank
        print('bnak_transfer',bnak_transfer)

        # total_maintenance_amount = Machine_Maintenance.objects.filter(machine_maintenance_amount_paid=True).filter(Q(machine_maintenance_amount_paid_by = 'Pinak') | Q(machine_maintenance_amount_paid_by = 'Company_Owner')).aggregate(
        #         total_amount=Sum('machine_maintenance_amount')
        #         )['total_amount']
        projectperson_bank_pay = Project_Person_Data.objects.filter(person_payment_mode='Bank',bank_id__bank_id=bank_id).aggregate(total=Sum('project_person_total_price'))['total'] or 0
        print('projectperson_bank_pay',projectperson_bank_pay)
        projectExpense_bank_pay = Project_Expense.objects.filter(project_payment_mode='Bank',bank_id__bank_id=bank_id).aggregate(total=Sum('project_expense_amount'))['total'] or 0
        print('projectExpense_bank_pay',projectExpense_bank_pay)
        avak_in_bank = Money_Debit_Credit.objects.filter(money_payment_mode='BANK',receiver_bank_id__bank_id=bank_id).aggregate(total=Sum('money_amount'))['total'] or 0
        javak_in_bank = Money_Debit_Credit.objects.filter(money_payment_mode='BANK',sender_bank_id__bank_id=bank_id).aggregate(total=Sum('money_amount'))['total'] or 0
        avak_javak_bank_pay = avak_in_bank - javak_in_bank
        print('avak_javak_bank_pay',avak_javak_bank_pay)
        current_Bank_Amount = initial_amount + bnak_transfer - projectperson_bank_pay - projectExpense_bank_pay + avak_javak_bank_pay
        return current_Bank_Amount
    

def rokad_amount(request):
    initial_amount = Company_Details.objects.first().company_sharuaati_shilak
    print('initialamount',initial_amount)    
    credit_in_bank = bank_cash.objects.filter(credit_debit='Credit').aggregate(total=Sum('amount'))['total'] or 0  
    print(credit_in_bank)    
    debit_in_bank = bank_cash.objects.filter(credit_debit='Debit').aggregate(total=Sum('amount'))['total'] or 0
    bnak_transfer = credit_in_bank-debit_in_bank
    print('bnak_transfer',bnak_transfer)
    # total_maintenance_amount = Machine_Maintenance.objects.filter(machine_maintenance_amount_paid=True).filter(Q(machine_maintenance_amount_paid_by = 'Pinak_Enterprise') | Q(machine_maintenance_amount_paid_by = 'Company_Owner')).aggregate(
    #         total_amount=Sum('machine_maintenance_amount')
    #         )['total_amount'] or 0
    total_maintenance_amount = Machine_Maintenance.objects.filter(machine_maintenance_amount_paid=True).filter(Q(machine_maintenance_amount_paid_by = 'Pinak_Enterprise') | Q(machine_maintenance_amount_paid_by = 'Company_Owner')).aggregate(
            total_amount=Sum('machine_maintenance_amount')
            )['total_amount'] or 0
    projectperson_rokad_pay = Project_Person_Data.objects.filter(person_payment_mode='Cash').aggregate(total=Sum('project_person_total_price'))['total'] or 0
    print('projectperson_cash_pay',projectperson_rokad_pay)
    projectExpense_rokad_pay = Project_Expense.objects.filter(project_payment_mode='Cash').aggregate(total=Sum('project_expense_amount'))['total'] or 0
    print('projectExpense_cash_pay',projectExpense_rokad_pay)
    avak_in_rokad = Money_Debit_Credit.objects.filter(money_payment_mode='CASH',receiver_person_id__person_id=1).exclude(pay_type_id__pay_type_name='વ્યક્તિ ડિસ્કાઉન્ટ').aggregate(total=Sum('money_amount'))['total'] or 0
    javak_in_rokad = Money_Debit_Credit.objects.filter(money_payment_mode='CASH', sender_person_id__person_id=1).exclude(pay_type_id__pay_type_name='વ્યક્તિ ડિસ્કાઉન્ટ').aggregate(total=Sum('money_amount'))['total'] or 0
    avak_javak_rokad = avak_in_rokad - javak_in_rokad
    print('avak_javak_cash_pay',avak_javak_rokad)
    current_rokad_Amount = initial_amount - total_maintenance_amount - bnak_transfer - projectperson_rokad_pay - projectExpense_rokad_pay + avak_javak_rokad
    return current_rokad_Amount

def totalbank_amount(request):
    total =0
    for x in Bank_Details.objects.filter(company_bank_account=True):
        bank_id = x.bank_id
        total = total + currentbank_amount(request,bank_id)
    return total  




def levani_aapvani_rakam(request,person_id):
    person_obj = Person.objects.get(person_id=person_id)
    print('===================================new person - {}============================================='.format(person_obj.person_name))

    # projectowner
    amount_from_maintenance_project_owner = Machine_Maintenance.objects.filter(project_id__project_owner_name__person_id=person_id,machine_maintenance_amount_paid_by='Project_Owner').aggregate(total=Sum('machine_maintenance_amount'))['total'] or 0
    amount_from_project_day_detail = Project_Day_Details.objects.filter(project_id__project_owner_name__person_id = person_id).aggregate(total=Sum('project_day_detail_total_price'))['total'] or 0
    amount_to_discount_project_owner = Project.objects.filter(project_owner_name__person_id = person_id).aggregate(total=Sum('project_discount'))['total'] or 0
    amount_from_projectperson_project_owner = Project_Person_Data.objects.filter(project_id__project_owner_name__person_id = person_id,project_person_paid_by='Project_Owner').aggregate(total=Sum('project_person_total_price'))['total'] or 0

    # bhgidari
    amount_from_bhagidari_in_project = Project.objects.filter(project_investor_id__person_id = person_id).aggregate(total=Sum('project_investor_amount'))['total'] or 0
    amount_to_bhagidari_in_project = 0
    amount_to_dalali_in_project =0
    for x in Project.objects.filter(project_investor_id__person_id=person_id):
        amount_to_bhagidari_in_project = amount_to_bhagidari_in_project + int(single_project_functionality(x.project_id)['project_saransh']['mudirokan_amt'])
    
    for x in Project.objects.filter(project_agent_id__person_id=person_id):    
        amount_to_dalali_in_project = amount_to_dalali_in_project + int(single_project_functionality(x.project_id)['project_saransh']['dalali_amt'])

    print("===========dalali - ",amount_to_dalali_in_project)
    # machineOwner
    amount_from_maintenance_machine_owner = Machine_Maintenance.objects.filter(machine_machine_id__machine_owner_id__person_id=person_id,machine_maintenance_amount_paid_by='machine_owner').aggregate(total=Sum('machine_maintenance_amount'))['total'] or 0
    amount_to_rent_machine_owner = Project_Machine_Data.objects.filter(machine_project_id__machine_own='Rented',machine_project_id__machine_owner_id__person_id=person_id).aggregate(total=Sum('project_machine_data_total_amount'))['total'] or 0
    amount_from_machine_owner_in_project_person = Project_Person_Data.objects.filter(project_machine_data_id__machine_owner_id__person_id=person_id,project_person_paid_by='machine_owner').aggregate(total=Sum('project_person_total_price'))['total'] or 0

    #maintenance

    amount_to_maintenance_person = Machine_Maintenance.objects.filter(machine_maintenance_person_id__person_id=person_id). exclude(machine_maintenance_amount_paid=1).aggregate(total=Sum('machine_maintenance_amount'))['total'] or 0

    #driver or Employee
    amount_to_driverEmployee = Salary.objects.filter(person_id__person_id = person_id).aggregate(total=Sum('salary_amount'))['total'] or 0

    #material
    amount_to_material_person = Material.objects.filter(material_owner__person_id=person_id).aggregate(total=Sum('material_total_price'))['total'] or 0

    #dalali
    amount_to_dalali_in_project = amount_to_dalali_in_project
    amount_to_dalali_in_material = Material.objects.filter(material_agent_person__person_id=person_id).aggregate(total=Sum('material_agent_amount'))['total'] or 0

    levani_rakam = amount_from_maintenance_project_owner+amount_from_project_day_detail+amount_from_projectperson_project_owner+amount_from_bhagidari_in_project+amount_from_maintenance_machine_owner+amount_from_machine_owner_in_project_person
    person_chukvel_rakam = Money_Debit_Credit.objects.filter(sender_person_id__person_id=person_id).aggregate(total=Sum('money_amount'))['total'] or 0
    levani_baki_rakam = levani_rakam - person_chukvel_rakam
    print('levani_rakam',levani_rakam)
    print('person_chukvel_rakam',person_chukvel_rakam)
    print('levani_baki_rakam',levani_baki_rakam)


    aapvani_rakam = amount_to_discount_project_owner+amount_to_bhagidari_in_project+amount_to_rent_machine_owner+amount_to_maintenance_person+amount_to_driverEmployee+amount_to_material_person+amount_to_dalali_in_project+amount_to_dalali_in_material
    person_aapididhel_rakam = Money_Debit_Credit.objects.filter(receiver_person_id__person_id=person_id).aggregate(total=Sum('money_amount'))['total'] or 0
    aapvani_baki_rakam = aapvani_rakam - person_aapididhel_rakam
    print('aapvani_rakam',aapvani_rakam)
    print('person_aapididhel_rakam',person_aapididhel_rakam)
    print('aapvani_baki_rakam',aapvani_baki_rakam)

    final_rakam = levani_baki_rakam - aapvani_baki_rakam
    # if +100 levana
    # if -100 aapvana
    context={'levani_baki_rakam':levani_baki_rakam,'aapvani_baki_rakam':aapvani_baki_rakam,'final_rakam':final_rakam}
    return context



def kul_rakam_hisab(request):
    kul_levani_baki_rakam = 0
    kul_aapvani_baki_rakam = 0
    kul_rakam = 0
    for x in Person.objects.all():
        if x.person_id != 1:
            kul_levani_baki_rakam = kul_levani_baki_rakam + levani_aapvani_rakam(request,x.person_id)['levani_baki_rakam']
            kul_aapvani_baki_rakam = kul_aapvani_baki_rakam + levani_aapvani_rakam(request,x.person_id)['aapvani_baki_rakam']
            kul_rakam = kul_rakam + levani_aapvani_rakam(request,x.person_id)['final_rakam']
    
    return {'kul_levani_baki_rakam':kul_levani_baki_rakam,'kul_aapvani_baki_rakam':kul_aapvani_baki_rakam,'kul_rakam':kul_rakam}








def person_report_data(person_id):
    person_obj = Person.objects.get(person_id=person_id)
    all_data = {}
    print('===================================new person - {}============================================='.format(person_obj.person_name))

    # projectowner
    amount_from_maintenance_project_owner = Machine_Maintenance.objects.filter(project_id__project_owner_name__person_id=person_id,machine_maintenance_amount_paid_by='Project_Owner').aggregate(total=Sum('machine_maintenance_amount'))['total'] or 0
    amount_from_project_day_detail = Project_Day_Details.objects.filter(project_id__project_owner_name__person_id = person_id).aggregate(total=Sum('project_day_detail_total_price'))['total'] or 0

    amount_from_project_day_detail_data = Project_Day_Details.objects.filter(project_id__project_owner_name__person_id = person_id).values()
    all_data.update({'amount_from_project_day_detail_data':amount_from_project_day_detail_data,'amount_from_project_day_detail_total':amount_from_project_day_detail})

    amount_to_discount_project_owner = Project.objects.filter(project_owner_name__person_id = person_id).aggregate(total=Sum('project_discount'))['total'] or 0
    amount_to_discount_project_owner_data = Project.objects.filter(project_owner_name__person_id = person_id).values('project_discount','project_name')
    all_data.update({'amount_to_discount_project_owner_data':amount_to_discount_project_owner_data,'amount_to_discount_project_owner_total':amount_to_discount_project_owner})

    amount_from_projectperson_project_owner = Project_Person_Data.objects.filter(project_id__project_owner_name__person_id = person_id,project_person_paid_by='Project_Owner').aggregate(total=Sum('project_person_total_price'))['total'] or 0

    # bhgidari
    amount_from_bhagidari_in_project = Project.objects.filter(project_investor_id__person_id = person_id).aggregate(total=Sum('project_investor_amount'))['total'] or 0
    amount_from_bhagidari_in_project_data = Project.objects.filter(project_investor_id__person_id = person_id).values('project_investor_amount','project_name')
    all_data.update({'amount_from_bhagidari_in_project':amount_from_bhagidari_in_project_data,'amount_from_bhagidari_in_project_total':amount_from_bhagidari_in_project})

    amount_to_bhagidari_in_project = 0
    amount_to_bhagidari_in_project_data=[]
    amount_to_dalali_in_project =0
    amount_to_dalali_in_project_data = []
    for x in Project.objects.filter(project_investor_id__person_id=person_id):
        amount_to_bhagidari_in_project = amount_to_bhagidari_in_project + int(single_project_functionality(x.project_id)['project_saransh']['mudirokan_amt'])
        amount_to_bhagidari_in_project_data.append({'mudirokan_amt': int(single_project_functionality(x.project_id)['project_saransh']['mudirokan_amt']),'project_name':x.project_name})
    all_data.update({'amount_to_bhagidari_in_project_data':amount_to_bhagidari_in_project_data,'amount_to_bhagidari_in_project_total':amount_to_bhagidari_in_project})

    for x in Project.objects.filter(project_agent_id__person_id=person_id):    
        amount_to_dalali_in_project = amount_to_dalali_in_project + int(single_project_functionality(x.project_id)['project_saransh']['dalali_amt'])
        amount_to_dalali_in_project_data.append({'dalali_amt': int(single_project_functionality(x.project_id)['project_saransh']['dalali_amt']),'project_name':x.project_name})
    all_data.update({'amount_to_dalali_in_project_data':amount_to_dalali_in_project_data,'amount_to_dalali_in_project_total':amount_to_dalali_in_project})

    # machineOwner
    amount_from_maintenance_machine_owner = Machine_Maintenance.objects.filter(machine_machine_id__machine_owner_id__person_id=person_id,machine_maintenance_amount_paid_by='machine_owner').aggregate(total=Sum('machine_maintenance_amount'))['total'] or 0
    amount_from_maintenance_machine_owner_data = Machine_Maintenance.objects.filter(machine_machine_id__machine_owner_id__person_id=person_id,machine_maintenance_amount_paid_by='machine_owner').values()
    all_data.update({'amount_from_maintenance_machine_owner_data':amount_from_maintenance_machine_owner_data,'amount_from_maintenance_machine_owner_total':amount_from_maintenance_machine_owner})

    amount_to_rent_machine_owner = Project_Machine_Data.objects.filter(machine_project_id__machine_own='Rented',machine_project_id__machine_owner_id__person_id=person_id).aggregate(total=Sum('project_machine_data_total_amount'))['total'] or 0
    amount_to_rent_machine_owner_data = Project_Machine_Data.objects.filter(machine_project_id__machine_own='Rented',machine_project_id__machine_owner_id__person_id=person_id).values()
    all_data.update({'amount_to_rent_machine_owner_data':amount_to_rent_machine_owner_data,'amount_to_rent_machine_owner_total':amount_to_rent_machine_owner})

    amount_from_machine_owner_in_project_person = Project_Person_Data.objects.filter(project_machine_data_id__machine_owner_id__person_id=person_id,project_person_paid_by='machine_owner').aggregate(total=Sum('project_person_total_price'))['total'] or 0
    amount_from_machine_owner_in_project_person_data = Project_Person_Data.objects.filter(project_machine_data_id__machine_owner_id__person_id=person_id,project_person_paid_by='machine_owner').values()
    all_data.update({'amount_from_machine_owner_in_project_person_data':amount_from_machine_owner_in_project_person_data,'amount_from_machine_owner_in_project_person_total':amount_from_machine_owner_in_project_person})
    #maintenance

    amount_to_maintenance_person = Machine_Maintenance.objects.filter(machine_maintenance_person_id__person_id=person_id).exclude(machine_maintenance_amount_paid=1).aggregate(total=Sum('machine_maintenance_amount'))['total'] or 0
    amount_to_maintenance_person_data = Machine_Maintenance.objects.filter(machine_maintenance_person_id__person_id=person_id).exclude(machine_maintenance_amount_paid=1).values()
    all_data.update({'amount_to_maintenance_person_data':amount_to_maintenance_person_data,'amount_to_maintenance_person_total':amount_to_maintenance_person})

    #driver or Employee
    amount_to_driverEmployee = Salary.objects.filter(person_id__person_id = person_id).aggregate(total=Sum('salary_amount'))['total'] or 0
    amount_to_driverEmployee_data = Salary.objects.filter(person_id__person_id = person_id).values()
    all_data.update({'amount_to_driverEmployee_data':amount_to_driverEmployee_data,'amount_to_driverEmployee_total':amount_to_driverEmployee})

    #material
    amount_to_material_person = Material.objects.filter(material_owner__person_id=person_id).aggregate(total=Sum('material_total_price'))['total'] or 0
    amount_to_material_person_data = Material.objects.filter(material_owner__person_id=person_id).values()
    all_data.update({'amount_to_material_person_data':amount_to_material_person_data,'amount_to_material_person_total':amount_to_material_person})

    #dalali
    amount_to_dalali_in_project = amount_to_dalali_in_project
    amount_to_dalali_in_material = Material.objects.filter(material_agent_person__person_id=person_id).aggregate(total=Sum('material_agent_amount'))['total'] or 0
    amount_to_dalali_in_material_data = Material.objects.filter(material_agent_person__person_id=person_id).values()
    all_data.update({'amount_to_dalali_in_material_data':amount_to_dalali_in_material_data,'amount_to_dalali_in_material_total':amount_to_dalali_in_material})



    levani_rakam = amount_from_maintenance_project_owner+amount_from_project_day_detail+amount_from_projectperson_project_owner+amount_from_bhagidari_in_project+amount_from_maintenance_machine_owner+amount_from_machine_owner_in_project_person
    person_chukvel_rakam = Money_Debit_Credit.objects.filter(sender_person_id__person_id=person_id).aggregate(total=Sum('money_amount'))['total'] or 0
    person_chukvel_rakam_data = Money_Debit_Credit.objects.filter(sender_person_id__person_id=person_id).values()
    all_data.update({'person_chukvel_rakam_data':person_chukvel_rakam_data,'person_chukvel_rakam_total':person_chukvel_rakam})

    levani_baki_rakam = levani_rakam - person_chukvel_rakam
    print('levani_rakam',levani_rakam)
    print('person_chukvel_rakam',person_chukvel_rakam)
    print('levani_baki_rakam',levani_baki_rakam)

    aapvani_rakam = amount_to_discount_project_owner+amount_to_bhagidari_in_project+amount_to_rent_machine_owner+amount_to_maintenance_person+amount_to_driverEmployee+amount_to_material_person+amount_to_dalali_in_project+amount_to_dalali_in_material
    person_aapididhel_rakam = Money_Debit_Credit.objects.filter(receiver_person_id__person_id=person_id).aggregate(total=Sum('money_amount'))['total'] or 0
    person_aapididhel_rakam_data = Money_Debit_Credit.objects.filter(receiver_person_id__person_id=person_id).values()
    all_data.update({'person_aapididhel_rakam_data':person_aapididhel_rakam_data,'person_aapididhel_rakam_total':person_aapididhel_rakam})

    aapvani_baki_rakam = aapvani_rakam - person_aapididhel_rakam
    print('aapvani_rakam',aapvani_rakam)
    print('person_aapididhel_rakam',person_aapididhel_rakam)
    print('aapvani_baki_rakam',aapvani_baki_rakam)
    all_data.update({'levani_baki_rakam':levani_baki_rakam,'aapvani_baki_rakam':aapvani_baki_rakam})
    final_rakam = levani_baki_rakam - aapvani_baki_rakam
    all_data.update({'final_rakam':final_rakam})
    # if +100 levana
    # if -100 aapvana
    return all_data



def bank_credit_report_data(bank_id):
    bank_obj = Bank_Details.objects.get(bank_id=bank_id)
    current_balance = currentbank_amount('request',bank_id)
    bank_datails = {'bank_name':bank_obj.bank_name,'bank_branch':bank_obj.bank_branch,'bank_account_number':bank_obj.bank_account_number,'bank_ifsc_code':bank_obj.bank_ifsc_code,'bank_account_holder':bank_obj.bank_account_holder,'bank_initial_amount':bank_obj.bank_initial_amount,'bank_open_closed':bank_obj.bank_open_closed,'bank_person_name':bank_obj.person_id.person_name,'current_balance':current_balance}
    money_credit_into_bank = Money_Debit_Credit.objects.filter(receiver_bank_id=bank_obj).values('sender_person_id__person_name','receiver_person_id__person_name','pay_type_id__pay_type_name','money_amount','money_date','money_payment_details','machine_id__machine_name','machine_id__machine_number_plate','project_id__project_name')
    money_credit_into_bank_total = Money_Debit_Credit.objects.filter(receiver_bank_id=bank_obj).aggregate(total=Sum('money_amount'))['total'] or 0
    bank_cash_trasfer_data = bank_cash.objects.filter(bank_id=bank_obj,credit_debit='Credit').values('credit_debit','amount','date','details')
    bank_cash_trasfer_data_total = bank_cash.objects.filter(bank_id=bank_obj).aggregate(total=Sum('amount'))['total'] or 0
    return {'bank_datails':bank_datails,'money_credit_into_bank':money_credit_into_bank,'money_credit_into_bank_total':money_credit_into_bank_total,'bank_cash_trasfer_data':bank_cash_trasfer_data,'bank_cash_trasfer_data_total':bank_cash_trasfer_data_total}
    



def bank_debit_report_data(bank_id):
    bank_obj = Bank_Details.objects.get(bank_id=bank_id)
    current_balance = currentbank_amount('request',bank_id)
    bank_datails = {'bank_name':bank_obj.bank_name,'bank_branch':bank_obj.bank_branch,'bank_account_number':bank_obj.bank_account_number,'bank_ifsc_code':bank_obj.bank_ifsc_code,'bank_account_holder':bank_obj.bank_account_holder,'bank_initial_amount':bank_obj.bank_initial_amount,'bank_open_closed':bank_obj.bank_open_closed,'bank_person_name':bank_obj.person_id.person_name,'current_balance':current_balance}
    project_person_data_trasactions = Project_Person_Data.objects.filter(bank_id=bank_obj).values('person_id__person_name','person_id__person_contact_number','project_person_date','work_type_id__work_type_name','project_machine_data_id__machine_name','project_machine_data_id__machine_number_plate','project_person_work_num','project_person_price','project_person_total_price','project_person_paid_by','project_person_payment_details','project_id__project_name','project_person_paid_by')
    project_person_data_trasactions_total = Project_Person_Data.objects.filter(bank_id=bank_obj).aggregate(total=Sum('project_person_total_price'))['total'] or 0
    money_debit_into_bank = Money_Debit_Credit.objects.filter(sender_bank_id=bank_obj).values('sender_person_id__person_name','receiver_person_id__person_name','pay_type_id__pay_type_name','money_amount','money_date','money_payment_details','machine_id__machine_name','machine_id__machine_number_plate','project_id__project_name')
    money_debit_into_bank_total = Money_Debit_Credit.objects.filter(sender_bank_id=bank_obj).aggregate(total=Sum('money_amount'))['total'] or 0
    project_expense_data = Project_Expense.objects.filter(bank_id=bank_obj).values('project_expense_name','project_id__project_name','project_expense_date','project_expense_amount','project_expense_desc')
    project_expense_data_total = Project_Expense.objects.filter(bank_id=bank_obj).aggregate(total=Sum('project_expense_amount'))['total'] or 0
    bank_cash_trasfer_data = bank_cash.objects.filter(bank_id=bank_obj,credit_debit='Debit').values('credit_debit','amount','date','details')
    bank_cash_trasfer_data_total = bank_cash.objects.filter(bank_id=bank_obj,credit_debit='Debit').aggregate(total=Sum('amount'))['total'] or 0
    return {'bank_datails':bank_datails,'project_person_data_trasactions':project_person_data_trasactions,'project_person_data_trasactions_total':project_person_data_trasactions_total,'money_credit_into_bank':money_debit_into_bank,'money_credit_into_bank_total':money_debit_into_bank_total,'project_expense_data':project_expense_data,'project_expense_data_total':project_expense_data_total,'bank_cash_trasfer_data':bank_cash_trasfer_data,'bank_cash_trasfer_data_total':bank_cash_trasfer_data_total}
    





def rokad_hisab_amount(request):
    initial_amount = Company_Details.objects.first().company_sharuaati_shilak
    current = rokad_amount(request)
    credit_in_bank = bank_cash.objects.filter(credit_debit='Credit').aggregate(total=Sum('amount'))['total'] or 0
    credit_in_bank_data = bank_cash.objects.filter(credit_debit='Credit').values('credit_debit','amount','bank_id__bank_name','bank_id__bank_id','date','details')

    debit_in_bank = bank_cash.objects.filter(credit_debit='Debit').aggregate(total=Sum('amount'))['total'] or 0
    bnak_transfer = credit_in_bank-debit_in_bank
    debit_in_bank_data = bank_cash.objects.filter(credit_debit='Debit').values('credit_debit','amount','bank_id__bank_name','bank_id__bank_id','date','details')

    total_maintenance_amount = Machine_Maintenance.objects.filter(machine_maintenance_amount_paid=True).filter(Q(machine_maintenance_amount_paid_by = 'Pinak_Enterprise') | Q(machine_maintenance_amount_paid_by = 'Company_Owner')).aggregate(
            total_amount=Sum('machine_maintenance_amount')
            )['total_amount'] or 0
    total_maintenance_amount_data = Machine_Maintenance.objects.filter(machine_maintenance_amount_paid=True).filter(Q(machine_maintenance_amount_paid_by = 'Pinak_Enterprise') | Q(machine_maintenance_amount_paid_by = 'Company_Owner')).values('machine_maintenance_amount','machine_maintenance_date','machine_maintenance_amount_paid_by','machine_maintenance_amount_paid','machine_maintenance_types_id__maintenance_type_name','machine_maintenance_types_id__maintenance_type_id','machine_maintenance_details','machine_maintenance_person_id__person_name','machine_maintenance_person_id__person_id','machine_maintenance_driver_id__person_name','machine_maintenance_driver_id__person_id')

    projectperson_rokad_pay = Project_Person_Data.objects.filter(project_person_paid_by='Pinak').aggregate(total=Sum('project_person_total_price'))['total'] or 0
    projectperson_rokad_pay_data = Project_Person_Data.objects.filter(project_person_paid_by='Pinak').values('person_id__person_name', 'person_id__person_id', 'person_id__person_contact_number',
        'work_type_id__work_type_name', 'project_person_work_num', 'project_person_price',
        'project_person_total_price', 'project_person_paid_by', 'project_id__project_name',
        'project_id__project_owner_name__person_name')

    projectExpense_rokad_pay = Project_Expense.objects.filter().aggregate(total=Sum('project_expense_amount'))['total'] or 0
    projectExpense_rokad_pay_data = Project_Expense.objects.filter().values('project_expense_id',
        'project_expense_name',
        'project_id__project_name',
        'project_expense_date',
        'project_expense_amount',
        'project_payment_mode',
        'bank_id__bank_name',
        'project_expense_desc',)


    # money_payment_mode='CASH'
    avak_in_rokad_total = Money_Debit_Credit.objects.filter(receiver_person_id__person_id=1).exclude(pay_type_id__pay_type_name='વ્યક્તિ ડિસ્કાઉન્ટ').aggregate(total=Sum('money_amount'))['total'] or 0
    avak_in_rokad_data = Money_Debit_Credit.objects.filter(receiver_person_id__person_id=1).exclude(pay_type_id__pay_type_name='વ્યક્તિ ડિસ્કાઉન્ટ').values('sender_person_id__person_name','receiver_person_id__person_name','pay_type_id__pay_type_name','money_amount','money_date','money_payment_details','machine_id__machine_name','machine_id__machine_number_plate','project_id__project_name')

    javak_in_rokad_total = Money_Debit_Credit.objects.filter(sender_person_id__person_id=1).exclude(pay_type_id__pay_type_name='વ્યક્તિ ડિસ્કાઉન્ટ').aggregate(total=Sum('money_amount'))['total'] or 0
    javak_in_rokad_data = Money_Debit_Credit.objects.filter(sender_person_id__person_id=1).exclude(pay_type_id__pay_type_name='વ્યક્તિ ડિસ્કાઉન્ટ').values('sender_person_id__person_name','receiver_person_id__person_name','pay_type_id__pay_type_name','money_amount','money_date','money_payment_details','machine_id__machine_name','machine_id__machine_number_plate','project_id__project_name')
    avak_javak_rokad = avak_in_rokad_total - javak_in_rokad_total

    return {'initial_amount':initial_amount,'credit_in_bank_data':credit_in_bank_data,'debit_in_bank_data':debit_in_bank_data,'total_maintenance_amount':total_maintenance_amount,'total_maintenance_amount_data':total_maintenance_amount_data,'projectperson_rokad_pay_total':projectperson_rokad_pay,'projectperson_rokad_pay_data':projectperson_rokad_pay_data,'projectExpense_rokad_pay_total':projectExpense_rokad_pay,
            'projectExpense_rokad_pay_data':projectExpense_rokad_pay_data,'total_aavak':avak_in_rokad_total,
            'avak_in_rokad_data':avak_in_rokad_data,'total_javak':javak_in_rokad_total,'javak_in_rokad_data':javak_in_rokad_data,'avak_javak_rokad':avak_javak_rokad,'final_Balance':avak_javak_rokad}



