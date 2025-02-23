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
            dalali_amt = (project.project_agent_percentage*100)/int(day_detail_total_amt)
        else:
            dalali_amt= int(project.project_agent_fixed_amount)


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
    initial_amount = 0
    print('initialamount',initial_amount)    
    credit_in_bank = bank_cash.objects.filter(credit_debit='Credit').aggregate(total=Sum('amount'))['total'] or 0  
    print(credit_in_bank)    
    debit_in_bank = bank_cash.objects.filter(credit_debit='Debit').aggregate(total=Sum('amount'))['total'] or 0
    bnak_transfer = credit_in_bank-debit_in_bank
    print('bnak_transfer',bnak_transfer)
    total_maintenance_amount = Machine_Maintenance.objects.filter(machine_maintenance_amount_paid=True).filter(Q(machine_maintenance_amount_paid_by = 'Pinak') | Q(machine_maintenance_amount_paid_by = 'Company_Owner')).aggregate(
            total_amount=Sum('machine_maintenance_amount')
            )['total_amount'] or 0
    projectperson_rokad_pay = Project_Person_Data.objects.filter(person_payment_mode='Cash').aggregate(total=Sum('project_person_total_price'))['total'] or 0
    print('projectperson_cash_pay',projectperson_rokad_pay)
    projectExpense_rokad_pay = Project_Expense.objects.filter(project_payment_mode='Cash').aggregate(total=Sum('project_expense_amount'))['total'] or 0
    print('projectExpense_cash_pay',projectExpense_rokad_pay)
    avak_in_rokad = Money_Debit_Credit.objects.filter(money_payment_mode='CASH',receiver_person_id__person_id=1).aggregate(total=Sum('money_amount'))['total'] or 0
    javak_in_rokad = Money_Debit_Credit.objects.filter(money_payment_mode='CASH', sender_person_id__person_id=1).aggregate(total=Sum('money_amount'))['total'] or 0
    avak_javak_rokad = avak_in_rokad - javak_in_rokad
    print('avak_javak_cash_pay',avak_javak_rokad)
    current_rokad_Amount = initial_amount - bnak_transfer - projectperson_rokad_pay - projectExpense_rokad_pay + avak_javak_rokad
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
    amount_to_rent_machine_owner = machine_rent.objects.filter(machine_rent_machine_id__machine_owner_id__person_id=person_id).aggregate(total=Sum('rent_amount'))['total'] or 0

    #maintenance

    amount_to_maintenance_person = Machine_Maintenance.objects.filter(machine_maintenance_person_id__person_id=person_id).aggregate(total=Sum('machine_maintenance_amount'))['total'] or 0

    #driver or Employee
    amount_to_driverEmployee = Salary.objects.filter(person_id__person_id = person_id).aggregate(total=Sum('salary_amount'))['total'] or 0

    #material
    amount_to_material_person = Material.objects.filter(material_owner__person_id=person_id).aggregate(total=Sum('material_total_price'))['total'] or 0

    #dalali
    amount_to_dalali_in_project = amount_to_dalali_in_project
    amount_to_dalali_in_material = Material.objects.filter(material_agent_person__person_id=person_id).aggregate(total=Sum('material_agent_amount'))['total'] or 0

    levani_rakam = amount_from_maintenance_project_owner+amount_from_project_day_detail+amount_from_projectperson_project_owner+amount_from_bhagidari_in_project+amount_from_maintenance_machine_owner
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

