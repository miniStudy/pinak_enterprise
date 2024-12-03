from django.shortcuts import render
from pinak_app.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.


@api_view(['GET'])
def show_comapny_details(request):
    comapny_details_data = Company_Details.objects.last()
    comapny_details_data = {'company_contact_number': comapny_details_data.company_contact_number, 'company_owner_name': comapny_details_data.company_owner_name, 'company_owner_contact': comapny_details_data.company_owner_contact, 'company_address': comapny_details_data.company_address, 'company_logo': comapny_details_data.company_logo.url, 'company_logo_icon': comapny_details_data.company_logo_icon.url}
    
    return Response({
        "status": "success",
        "title": "Company",
        "data": comapny_details_data
    })

@api_view(['POST'])
def insert_update_comapny_detail(request):
    company_contact_number = request.data.get('company_contact_number')
    company_owner_name = request.data.get('company_owner_name')
    company_owner_contact = request.data.get('company_owner_contact')
    company_address = request.data.get('company_address')
    company_logo = request.FILES.get('company_logo')
    company_logo_icon = request.FILES.get('company_logo_icon')

    company_details, created = Company_Details.objects.update_or_create(
        company_contact_number=company_contact_number,
        defaults={
            "company_owner_name": company_owner_name,
            "company_owner_contact": company_owner_contact,
            "company_address": company_address,
            "company_logo": company_logo,
            "company_logo_icon": company_logo_icon
        }
    )
    
    return Response({
        "status": "success",
        "message": "Company details created successfully." if created else "Company details updated successfully.",
        "data": {
            "company_contact_number": company_details.company_contact_number,
            "company_owner_name": company_details.company_owner_name,
            "company_owner_contact": company_details.company_owner_contact,
            "company_address": company_details.company_address,
            "company_logo": company_details.company_logo.url if company_details.company_logo else None,
            "company_logo_icon": company_details.company_logo_icon.url if company_details.company_logo_icon else None
        }
    })

@api_view(['GET'])
def show_bank_details(request):
    bank_details_data = Bank_Details.objects.all().values('bank_id', 'bank_name', 'bank_branch', 'bank_account_number', 'bank_ifsc_code', 'bank_account_holder', 'bank_open_closed')

    return Response({
        "status": "success",
        "title": "Bank",
        "data": bank_details_data
    })



@api_view(['POST','GET'])
def insert_update_bank_detail(request):
    bank_id = request.data.get('bank_id')
    bank_name = request.data.get('bank_name')
    bank_branch = request.data.get('bank_branch')
    bank_account_number = request.data.get('bank_account_number')
    bank_ifsc_code = request.data.get('bank_ifsc_code')
    bank_account_holder = request.data.get('bank_account_holder')
    bank_open_closed = request.data.get('bank_open_closed')

    if request.GET.get('getdata_id'):
        bank_obj = Bank_Details.objects.get(bank_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            "bank_id": bank_obj.bank_id,
            "bank_name": bank_obj.bank_name,
            "bank_branch": bank_obj.bank_branch,
            "bank_account_number": bank_obj.bank_account_number,
            "bank_ifsc_code": bank_obj.bank_ifsc_code,
            "bank_account_holder": bank_obj.bank_account_holder,
            "bank_open_closed": bank_obj.bank_open_closed
        }
        })

    if bank_id:
        bank_detail = Bank_Details.objects.get(bank_id=bank_id)
        bank_detail.bank_name = bank_name
        bank_detail.bank_branch = bank_branch
        bank_detail.bank_account_number = bank_account_number
        bank_detail.bank_ifsc_code = bank_ifsc_code
        bank_detail.bank_account_holder = bank_account_holder
        bank_detail.bank_open_closed = bank_open_closed
        bank_detail.save()
        message = "Bank details updated successfully."
    else:
        bank_detail = Bank_Details.objects.create(
            bank_name=bank_name,
            bank_branch=bank_branch,
            bank_account_number=bank_account_number,
            bank_ifsc_code=bank_ifsc_code,
            bank_account_holder=bank_account_holder,
            bank_open_closed=bank_open_closed
        )
        message = "Bank details created successfully."
        
    return Response({
        "status": "success",
        "message": message,
        "data": {
            "bank_id": bank_detail.bank_id,
            "bank_name": bank_detail.bank_name,
            "bank_branch": bank_detail.bank_branch,
            "bank_account_number": bank_detail.bank_account_number,
            "bank_ifsc_code": bank_detail.bank_ifsc_code,
            "bank_account_holder": bank_detail.bank_account_holder,
            "bank_open_closed": bank_detail.bank_open_closed
        }
        })


@api_view(['DELETE'])
def delete_bank_detail(request):
    bank_id = request.data.get('bank_id')
    bank_detail = Bank_Details.objects.get(bank_id=bank_id)     
    bank_detail.delete()
        
    return Response({
        "status": "success",
        "message": "Bank details deleted successfully."
    })


@api_view(['GET'])
def show_machine_types(request):
    machine_types_data = Machine_Types.objects.all().values('machine_type_id', 'machine_type_name')
    return Response({
        "status": "success",
        "data": machine_types_data
    })


@api_view(['POST','GET'])
def insert_update_machine_type(request):
    machine_type_id = request.data.get('machine_type_id')
    machine_type_name = request.data.get('machine_type_name')

    if request.GET.get('getdata_id'):
        machine_type_obj = Machine_Types.objects.get(machine_type_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            "machine_type_id": machine_type_obj.machine_type_id,
            "machine_type_name": machine_type_obj.machine_type_name,  
        }
        })

    if machine_type_id:
        machine_type = Machine_Types.objects.get(machine_type_id=machine_type_id)
        machine_type.machine_type_name = machine_type_name
        machine_type.save()
        message = "Machine type updated successfully."
       
    else:
        machine_type = Machine_Types.objects.create(
            machine_type_name=machine_type_name
        )
        message = "Machine type created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "machine_type_id": machine_type.machine_type_id,
            "machine_type_name": machine_type.machine_type_name
        }
    })


@api_view(['DELETE'])
def delete_machine_type(request):
    machine_type_id = request.data.get('machine_type_id')
    machine_type = Machine_Types.objects.get(machine_type_id=machine_type_id)
    machine_type.delete()

    return Response({
        "status": "success",
         "message": "Machine type deleted successfully."
    })

@api_view(['GET'])
def show_company_machines(request):
    company_machines = Company_Machines.objects.all().values('machine_id', 'machine_owner', 'machine_buy_date', 'machine_condition', 'machine_number_plate', 'machine_details', 'machine_contact_number','machine_sold_out_date', 'machine_sold_price', 'machine_working', 'machine_types_id__machine_type_id', 'machine_types_id__machine_type_name')

    return Response({
        "status": "success",
        "title": "Machine",
        "data": company_machines
    })


@api_view(['POST','GET'])
def insert_update_company_machine(request):

    machine_types_data = Machine_Types.objects.all().values('machine_type_id', 'machine_type_name')
    if request.method == 'POST':
        machine_id = request.data.get('machine_id')
        machine_owner = request.data.get('machine_owner')
        machine_buy_date = request.data.get('machine_buy_date')
        machine_condition = request.data.get('machine_condition')
        machine_number_plate = request.data.get('machine_number_plate')
        machine_details = request.data.get('machine_details')
        machine_contact_number = request.data.get('machine_contact_number')
        machine_sold_out_date = request.data.get('machine_sold_out_date')
        machine_sold_price = request.data.get('machine_sold_price')
        machine_working = request.data.get('machine_working')
        machine_types_id = request.data.get('machine_types_id')
        machine_types_instance = Machine_Types.objects.get(machine_type_id=machine_types_id)

    if request.GET.get('getdata_id'):
        machine_obj = Company_Machines.objects.get(machine_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            "machine_id": machine_obj.machine_id,
            "machine_owner": machine_obj.machine_owner,
            "machine_buy_date": machine_obj.machine_buy_date,
            "machine_condition": machine_obj.machine_condition,
            "machine_number_plate": machine_obj.machine_number_plate,
            "machine_details": machine_obj.machine_details,
            "machine_contact_number": machine_obj.machine_contact_number,
            "machine_sold_out_date": machine_obj.machine_sold_out_date,
            "machine_sold_price": machine_obj.machine_sold_price,
            "machine_working": machine_obj.machine_working,
            "machine_types_id": machine_obj.machine_types_id.machine_type_id,
            "machine_types": machine_types_data,
        }
        })

    if machine_id:
        machine = Company_Machines.objects.get(machine_id=machine_id)
        machine.machine_owner = machine_owner
        machine.machine_buy_date = machine_buy_date
        machine.machine_condition = machine_condition
        machine.machine_number_plate = machine_number_plate
        machine.machine_details = machine_details
        machine.machine_contact_number = machine_contact_number
        machine.machine_sold_out_date = machine_sold_out_date
        machine.machine_sold_price = machine_sold_price
        machine.machine_working = machine_working
        machine.machine_types_id = machine_types_instance
        machine.save()
        message = "Machine details updated successfully."
        
    else:
        machine = Company_Machines.objects.create(
            machine_owner=machine_owner,
            machine_buy_date=machine_buy_date,
            machine_condition=machine_condition,
            machine_number_plate=machine_number_plate,
            machine_details=machine_details,
            machine_contact_number=machine_contact_number,
            machine_sold_out_date=machine_sold_out_date,
            machine_sold_price=machine_sold_price,
            machine_working=machine_working,
            machine_types_id=machine_types_instance,
        )
        if machine:
            message = "Machine details created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "machine_id": machine.machine_id,
            "machine_owner": machine.machine_owner,
            "machine_buy_date": machine.machine_buy_date,
            "machine_condition": machine.machine_condition,
            "machine_number_plate": machine.machine_number_plate,
            "machine_details": machine.machine_details,
            "machine_contact_number": machine.machine_contact_number,
            "machine_sold_out_date": machine.machine_sold_out_date,
            "machine_sold_price": machine.machine_sold_price,
            "machine_working": machine.machine_working,
            "machine_types_id": machine.machine_types_id.machine_type_id,
            "machine_types": machine_types_data,
        }
    })


@api_view(['DELETE'])
def delete_company_machine(request):
    machine_id = request.data.get('machine_id')
    if not machine_id:
        return Response({
            "status": "error",
            "message": "No machine ID provided"
        }, status=400)
    try:
        machine = Company_Machines.objects.get(machine_id=machine_id)
        machine.delete()

        return Response({
            "status": "success",
            "message": "Machine deleted successfully."
        })

    except Company_Machines.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Machine with the provided ID not found."
        }, status=404)
    
@api_view(['GET'])
def show_working_machines(request):
    working_machines = Working_Machines.objects.all().values(
        'working_machine_id',
        'working_machine_name',
        'working_machine_owner_name',
        'working_machine_owner_contact',
        'working_machine_plate_number',
        'working_machine_start_date',
        'working_machine_end_date',
        'working_machine_ownership',
        'working_machine_details',
        'working_machine_rented_amount',
        'machine_type_id__machine_type_id',
        'machine_type_id__machine_type_name'
    )
    return Response({
        "status": "success",
        "data": working_machines
    })


@api_view(['POST'])
def insert_update_working_machine(request):
    working_machine_id = request.data.get('working_machine_id')
    working_machine_name = request.data.get('working_machine_name')
    working_machine_owner_name = request.data.get('working_machine_owner_name')
    working_machine_owner_contact = request.data.get('working_machine_owner_contact')
    working_machine_plate_number = request.data.get('working_machine_plate_number')
    working_machine_start_date = request.data.get('working_machine_start_date')
    working_machine_end_date = request.data.get('working_machine_end_date')
    working_machine_ownership = request.data.get('working_machine_ownership')
    working_machine_details = request.data.get('working_machine_details')
    working_machine_rented_amount = request.data.get('working_machine_rented_amount')
    machine_type_id = request.data.get('machine_type_id')

    machine_type_instance = Machine_Types.objects.get(machine_type_id=machine_type_id)
    
    if working_machine_id:
        working_machine = Working_Machines.objects.get(working_machine_id=working_machine_id)
        working_machine.working_machine_name = working_machine_name
        working_machine.working_machine_owner_name = working_machine_owner_name
        working_machine.working_machine_owner_contact = working_machine_owner_contact
        working_machine.working_machine_plate_number = working_machine_plate_number
        working_machine.working_machine_start_date = working_machine_start_date
        working_machine.working_machine_end_date = working_machine_end_date
        working_machine.working_machine_ownership = working_machine_ownership
        working_machine.working_machine_details = working_machine_details
        working_machine.working_machine_rented_amount = working_machine_rented_amount
        working_machine.machine_type_id = machine_type_instance
        working_machine.save()
        message = "Working machine updated successfully."
    else:
        working_machine = Working_Machines.objects.create(
            working_machine_name=working_machine_name,
            working_machine_owner_name=working_machine_owner_name,
            working_machine_owner_contact=working_machine_owner_contact,
            working_machine_plate_number=working_machine_plate_number,
            working_machine_start_date=working_machine_start_date,
            working_machine_end_date=working_machine_end_date,
            working_machine_ownership=working_machine_ownership,
            working_machine_details=working_machine_details,
            working_machine_rented_amount=working_machine_rented_amount,
            machine_type_id=machine_type_instance
        )
        message = "Working machine created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "working_machine_id": working_machine.working_machine_id,
            "working_machine_name": working_machine.working_machine_name,
            "working_machine_owner_name": working_machine.working_machine_owner_name,
            "working_machine_owner_contact": working_machine.working_machine_owner_contact,
            "working_machine_plate_number": working_machine.working_machine_plate_number,
            "working_machine_start_date": working_machine.working_machine_start_date,
            "working_machine_end_date": working_machine.working_machine_end_date,
            "working_machine_ownership": working_machine.working_machine_ownership,
            "working_machine_details": working_machine.working_machine_details,
            "working_machine_rented_amount": working_machine.working_machine_rented_amount,
            "machine_type_id": working_machine.machine_type_id.machine_type_id
        }
    })

@api_view(['DELETE'])
def delete_working_machine(request):
    working_machine_id = request.data.get('working_machine_id')

    if not working_machine_id:
        return Response({
            "status": "error",
            "message": "Working machine ID is required."
        }, status=400)

    try:
        working_machine = Working_Machines.objects.get(working_machine_id=working_machine_id)
        working_machine.delete()
        return Response({
            "status": "success",
            "message": "Working machine deleted successfully."
        })
    except Working_Machines.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Working machine not found."
        }, status=404)
    

@api_view(['GET'])
def show_maintenance_types(request):
    maintenance_types = Maintenance_Types.objects.all().values('maintenance_type_id', 'maintenance_type_name')

    return Response({
        "status": "success",
        "title": "Maintenance Type",
        "data": maintenance_types
    })

@api_view(['POST'])
def insert_update_maintenance_type(request):
    maintenance_type_id = request.data.get('maintenance_type_id')
    maintenance_type_name = request.data.get('maintenance_type_name')

    if maintenance_type_id:
        maintenance_type = Maintenance_Types.objects.get(maintenance_type_id=maintenance_type_id)
        maintenance_type.maintenance_type_name = maintenance_type_name
        message = "Maintenance type updated successfully."
        maintenance_type.save()
            
    else:
        maintenance_type = Maintenance_Types.objects.create(maintenance_type_name=maintenance_type_name)
        message = "Maintenance type added successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "maintenance_type_id": maintenance_type.maintenance_type_id,
            "maintenance_type_name": maintenance_type.maintenance_type_name,
        }
    })

@api_view(['DELETE'])
def delete_maintenance_type(request):
    maintenance_type_id = request.data.get('maintenance_type_id')
    if maintenance_type_id:
        try:
            maintenance_type = Maintenance_Types.objects.get(maintenance_type_id=maintenance_type_id)
            maintenance_type.delete()
            return Response({"status": "success", "message": "Maintenance type deleted successfully."})
        except Maintenance_Types.DoesNotExist:
            return Response({"status": "error", "message": "Maintenance type not found."}, status=404)
    else:
        return Response({"status": "error", "message": "Maintenance type ID is required."}, status=400)


@api_view(['GET'])
def show_machine_maintenance(request):
    machine_maintenance = Machine_Maintenance.objects.all().values(
        'machine_maintenance_id',
        'machine_maintenance_amount',
        'machine_maintenance_date',
        'machine_maintenance_amount_paid',
        'machine_maintenance_amount_paid_by',
        'machine_maintenance_person',
        'machine_maintenance_contact',
        'machine_maintenance_driver',
        'machine_maintenance_details',
        'machine_maintenance_types_id__maintenance_type_id',
        'machine_maintenance_types_id__maintenance_type_name'
    )
    return Response({
        "status": "success",
        "title": "Maintenance",
        "data": machine_maintenance
    })

@api_view(['POST'])
def insert_update_machine_maintenance(request):
    machine_maintenance_id = request.data.get('machine_maintenance_id')
    machine_maintenance_amount = request.data.get('machine_maintenance_amount')
    machine_maintenance_date = request.data.get('machine_maintenance_date')
    machine_maintenance_amount_paid = request.data.get('machine_maintenance_amount_paid')
    machine_maintenance_amount_paid_by = request.data.get('machine_maintenance_amount_paid_by')
    machine_maintenance_person = request.data.get('machine_maintenance_person')
    machine_maintenance_contact = request.data.get('machine_maintenance_contact')
    machine_maintenance_driver = request.data.get('machine_maintenance_driver')
    machine_maintenance_details = request.data.get('machine_maintenance_details')
    machine_maintenance_types_id = request.data.get('machine_maintenance_types_id')

    maintenance_type_instance = Maintenance_Types.objects.get(maintenance_type_id=machine_maintenance_types_id)
    
    if machine_maintenance_id:
        machine_maintenance = Machine_Maintenance.objects.get(machine_maintenance_id=machine_maintenance_id)
        machine_maintenance.machine_maintenance_amount = machine_maintenance_amount
        machine_maintenance.machine_maintenance_date = machine_maintenance_date
        machine_maintenance.machine_maintenance_amount_paid = machine_maintenance_amount_paid
        machine_maintenance.machine_maintenance_amount_paid_by = machine_maintenance_amount_paid_by
        machine_maintenance.machine_maintenance_person = machine_maintenance_person
        machine_maintenance.machine_maintenance_contact = machine_maintenance_contact
        machine_maintenance.machine_maintenance_driver = machine_maintenance_driver
        machine_maintenance.machine_maintenance_details = machine_maintenance_details
        machine_maintenance.machine_maintenance_types_id = maintenance_type_instance
        machine_maintenance.save()
        message = "Machine maintenance record updated successfully."
    else:
        machine_maintenance = Machine_Maintenance.objects.create(
            machine_maintenance_amount=machine_maintenance_amount,
            machine_maintenance_date=machine_maintenance_date,
            machine_maintenance_amount_paid=machine_maintenance_amount_paid,
            machine_maintenance_amount_paid_by=machine_maintenance_amount_paid_by,
            machine_maintenance_person=machine_maintenance_person,
            machine_maintenance_contact=machine_maintenance_contact,
            machine_maintenance_driver=machine_maintenance_driver,
            machine_maintenance_details=machine_maintenance_details,
            machine_maintenance_types_id=maintenance_type_instance
        )
        message = "Machine maintenance record created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "machine_maintenance_id": machine_maintenance.machine_maintenance_id,
            "machine_maintenance_amount": machine_maintenance.machine_maintenance_amount,
            "machine_maintenance_date": machine_maintenance.machine_maintenance_date,
            "machine_maintenance_amount_paid": machine_maintenance.machine_maintenance_amount_paid,
            "machine_maintenance_amount_paid_by": machine_maintenance.machine_maintenance_amount_paid_by,
            "machine_maintenance_person": machine_maintenance.machine_maintenance_person,
            "machine_maintenance_contact": machine_maintenance.machine_maintenance_contact,
            "machine_maintenance_driver": machine_maintenance.machine_maintenance_driver,
            "machine_maintenance_details": machine_maintenance.machine_maintenance_details,
            "machine_maintenance_types_id": machine_maintenance.machine_maintenance_types_id.maintenance_type_id,
        }
    })

@api_view(['DELETE'])
def delete_machine_maintenance(request):
    machine_maintenance_id = request.data.get('machine_maintenance_id')

    if not machine_maintenance_id:
        return Response({
            "status": "error",
            "message": "Machine maintenance ID is required."
        }, status=400)

    try:
        machine_maintenance = Machine_Maintenance.objects.get(machine_maintenance_id=machine_maintenance_id)
        machine_maintenance.delete()
        return Response({
            "status": "success",
            "message": "Machine maintenance record deleted successfully."
        })
    except Machine_Maintenance.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Machine maintenance record not found."
        }, status=404)


@api_view(['GET'])
def show_project_types(request):
    project_types = Project_Types.objects.all().values(
        'project_type_id', 
        'project_type_name', 
        'project_type_details')

    return Response({
        "status": "success",
        "title": "Project Types",
        "data": project_types
    })

@api_view(['POST'])
def insert_update_project_type(request):
    project_type_id = request.data.get('project_type_id')
    project_type_name = request.data.get('project_type_name')
    project_type_details = request.data.get('project_type_details')

    if project_type_id:
        project_type = Project_Types.objects.get(project_type_id = project_type_id)
        project_type.project_type_name = project_type_name
        project_type.project_type_details = project_type_details
        project_type.save()
        message = "Project type updated successfully."
    
    else:
        project_type = Project_Types.objects.create(project_type_id = project_type_id, project_type_name = project_type_name, project_type_details= project_type_details)
        message = "Project type created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "project_type_id": project_type.project_type_id,
            "project_type_name": project_type.project_type_name,
            "project_type_details": project_type.project_type_details,
        }
    })

@api_view(['DELETE'])
def delete_project_type(request):
    project_type_id = request.data.get('project_type_id')
    if not project_type_id:
        return Response({
            "status": "error",
            "message": "Project type ID is required."
        }, status=400)
    try:
        project_type = Project_Types.objects.get(project_type_id=project_type_id)
        project_type.delete()
        return Response({
            "status": "success",
            "message": "Project type deleted successfully."
        })
    except Project_Types.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Project type not found."
        }, status=404)


@api_view(['GET'])
def show_projects(request):
    projects = Project.objects.all().values(
        'project_id',
        'project_name',
        'project_start_date',
        'project_end_date',
        'project_amount',
        'project_location',
        'project_company_name',
        'project_person_name',
        'project_status',
        'project_types_id__project_type_id',
        'project_types_id__project_type_name'
    )
    return Response({
        "status": "success",
        "title": "Project",
        "data": projects
    })

@api_view(['POST'])
def insert_update_project(request):
    project_id = request.data.get('project_id')
    project_name = request.data.get('project_name')
    project_start_date = request.data.get('project_start_date')
    project_end_date = request.data.get('project_end_date')
    project_amount = request.data.get('project_amount')
    project_location = request.data.get('project_location')
    project_company_name = request.data.get('project_company_name')
    project_person_name = request.data.get('project_person_name')
    project_status = request.data.get('project_status')
    project_types_id = request.data.get('project_types_id')

    project_type_instance = Project_Types.objects.get(project_type_id=project_types_id)
   

    if project_id:
        project = Project.objects.get(project_id=project_id)
        project.project_name = project_name
        project.project_start_date = project_start_date
        project.project_end_date = project_end_date
        project.project_amount = project_amount
        project.project_location = project_location
        project.project_company_name = project_company_name
        project.project_person_name = project_person_name
        project.project_status = project_status
        project.project_types_id = project_type_instance
        project.save()
        message = "Project updated successfully."
    else:
        project = Project.objects.create(
            project_name=project_name,
            project_start_date=project_start_date,
            project_end_date=project_end_date,
            project_amount=project_amount,
            project_location=project_location,
            project_company_name=project_company_name,
            project_person_name=project_person_name,
            project_status=project_status,
            project_types_id=project_type_instance
        )
        message = "Project created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "project_id": project.project_id,
            "project_name": project.project_name,
            "project_start_date": project.project_start_date,
            "project_end_date": project.project_end_date,
            "project_amount": project.project_amount,
            "project_location": project.project_location,
            "project_company_name": project.project_company_name,
            "project_person_name": project.project_person_name,
            "project_status": project.project_status,
            "project_types_id": project.project_types_id.project_type_id
        }
    })

@api_view(['DELETE'])
def delete_project(request):
    project_id = request.data.get('project_id')
    if not project_id:
        return Response({
            "status": "error",
            "message": "Project ID is required."
        }, status=400)
    try:
        project = Project.objects.get(project_id=project_id)
        project.delete()
        return Response({
            "status": "success",
            "message": "Project deleted successfully."
        })
    except Project.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Project not found."
        }, status=404)


@api_view(['GET'])
def show_pay_types(request):
    pay_types = Pay_Types.objects.all().values(
        'pay_type_id',
        'pay_type_name',
        'pay_type_date'
    )
    return Response({
        "status": "success",
        "data": pay_types
    })

@api_view(['POST'])
def insert_update_pay_type(request):
    pay_type_id = request.data.get('pay_type_id')
    pay_type_name = request.data.get('pay_type_name')
    pay_type_date = request.data.get('pay_type_date')

    if pay_type_id:
        pay_type = Pay_Types.objects.get(pay_type_id=pay_type_id)
        pay_type.pay_type_name = pay_type_name
        pay_type.pay_type_date = pay_type_date
        pay_type.save()
        message = "Pay type updated successfully."
    else:
        pay_type = Pay_Types.objects.create(
            pay_type_name=pay_type_name,
            pay_type_date=pay_type_date
        )
        message = "Pay type created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "pay_type_id": pay_type.pay_type_id,
            "pay_type_name": pay_type.pay_type_name,
            "pay_type_date": pay_type.pay_type_date
        }
    })


@api_view(['DELETE'])
def delete_pay_type(request):
    pay_type_id = request.data.get('pay_type_id')

    if not pay_type_id:
        return Response({
            "status": "error",
            "message": "Pay type ID is required."
        }, status=400)
    try:
        pay_type = Pay_Types.objects.get(pay_type_id=pay_type_id)
        pay_type.delete()
        return Response({
            "status": "success",
            "message": "Pay type deleted successfully."
        })
    except Pay_Types.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Pay type not found."
        }, status=404)


@api_view(['GET'])
def show_person_types(request):
    person_types = Person_Type.objects.all().values(
        'person_type_id',
        'person_type_name'
    )
    return Response({
        "status": "success",
        "title": "Person Type",
        "data": person_types
    })


@api_view(['POST'])
def insert_update_person_type(request):
    person_type_id = request.data.get('person_type_id')
    person_type_name = request.data.get('person_type_name')

    if person_type_id:
        person_type = Person_Type.objects.get(person_type_id=person_type_id)
        person_type.person_type_name = person_type_name
        person_type.save()
        message = "Person type updated successfully."
    else:
        person_type = Person_Type.objects.create(
            person_type_name=person_type_name
        )
        message = "Person type created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "person_type_id": person_type.person_type_id,
            "person_type_name": person_type.person_type_name
        }
    })

@api_view(['DELETE'])
def delete_person_type(request):
    person_type_id = request.data.get('person_type_id')

    if not person_type_id:
        return Response({
            "status": "error",
            "message": "Person type ID is required."
        }, status=400)

    try:
        person_type = Person_Type.objects.get(person_type_id=person_type_id)
        person_type.delete()
        return Response({
            "status": "success",
            "message": "Person type deleted successfully."
        })
    except Person_Type.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Person type not found."
        }, status=404)

@api_view(['GET'])
def show_persons(request):
    persons = Person.objects.all().values(
        'person_id',
        'person_name',
        'person_contact_number',
        'person_work_type',
        'person_type_id__person_type_id',
        'person_type_id__person_type_name'
    )
    return Response({
        "status": "success",
        "title": "Person",
        "data": persons
    })


@api_view(['POST'])
def insert_update_person(request):
    person_id = request.data.get('person_id')
    person_name = request.data.get('person_name')
    person_contact_number = request.data.get('person_contact_number')
    person_work_type = request.data.get('person_work_type')
    person_type_id = request.data.get('person_type_id')

    person_type_instance = Person_Type.objects.get(person_type_id=person_type_id)
    
    if person_id:
        person = Person.objects.get(person_id=person_id)
        person.person_name = person_name
        person.person_contact_number = person_contact_number
        person.person_work_type = person_work_type
        person.person_type_id = person_type_instance
        person.save()
        message = "Person updated successfully."
    else:
        person = Person.objects.create(
            person_name=person_name,
            person_contact_number=person_contact_number,
            person_work_type=person_work_type,
            person_type_id=person_type_instance
        )
        message = "Person created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "person_id": person.person_id,
            "person_name": person.person_name,
            "person_contact_number": person.person_contact_number,
            "person_work_type": person.person_work_type,
            "person_type_id": person.person_type_id.person_type_id
        }
    })


@api_view(['DELETE'])
def delete_person(request):
    person_id = request.data.get('person_id')

    if not person_id:
        return Response({
            "status": "error",
            "message": "Person ID is required."
        }, status=400)

    try:
        person = Person.objects.get(person_id=person_id)
        person.delete()
        return Response({
            "status": "success",
            "message": "Person deleted successfully."
        })
    except Person.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Person not found."
        }, status=404)
    

@api_view(['GET'])
def show_work_types(request):
    work_types = Work_Types.objects.all().values(
        'work_type_id',
        'work_type_name',
        'work_type_details'
    )
    return Response({
        "status": "success",
        "data": work_types
    })

@api_view(['POST'])
def insert_update_work_type(request):
    work_type_id = request.data.get('work_type_id')
    work_type_name = request.data.get('work_type_name')
    work_type_details = request.data.get('work_type_details')

    if work_type_id:
        work_type = Work_Types.objects.get(work_type_id=work_type_id)
        work_type.work_type_name = work_type_name
        work_type.work_type_details = work_type_details
        work_type.save()
        message = "Work type updated successfully."
        
    else:
        work_type = Work_Types.objects.create(
            work_type_name=work_type_name,
            work_type_details=work_type_details
        )
        message = "Work type created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "work_type_id": work_type.work_type_id,
            "work_type_name": work_type.work_type_name,
            "work_type_details": work_type.work_type_details
        }
    })

@api_view(['DELETE'])
def delete_work_type(request):
    work_type_id = request.data.get('work_type_id')

    if not work_type_id:
        return Response({
            "status": "error",
            "message": "Work type ID is required."
        }, status=400)

    try:
        work_type = Work_Types.objects.get(work_type_id=work_type_id)
        work_type.delete()
        return Response({
            "status": "success",
            "message": "Work type deleted successfully."
        })
    except Work_Types.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Work type not found."
        }, status=404)


@api_view(['GET'])
def show_material_types(request):
    material_types = Material_Types.objects.all().values(
        'material_type_id',
        'material_type_name'
    )
    return Response({
        "status": "success",
        "title": "Material Types",
        "data": material_types
    })


@api_view(['POST'])
def insert_update_material_type(request):
    material_type_id = request.data.get('material_type_id')
    material_type_name = request.data.get('material_type_name')

    if material_type_id:
        material_type = Material_Types.objects.get(material_type_id=material_type_id)
        material_type.material_type_name = material_type_name
        material_type.save()
        message = "Material type updated successfully."
     
    else:
        material_type = Material_Types.objects.create(
            material_type_name=material_type_name
        )
        message = "Material type created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "material_type_id": material_type.material_type_id,
            "material_type_name": material_type.material_type_name
        }
    })

@api_view(['DELETE'])
def delete_material_type(request):
    material_type_id = request.data.get('material_type_id')

    if not material_type_id:
        return Response({
            "status": "error",
            "message": "Material type ID is required."
        }, status=400)

    try:
        material_type = Material_Types.objects.get(material_type_id=material_type_id)
        material_type.delete()
        return Response({
            "status": "success",
            "message": "Material type deleted successfully."
        })
    except Material_Types.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Material type not found."
        }, status=404)

@api_view(['GET'])
def show_materials(request):
    materials = Materials.objects.all().values(
        'material_id',
        'material_owner_name',
        'material_used_date',
        'material_type_id__material_type_name',
        'work_type_id__work_type_name',
        'material_work_number',
        'material_work_amount',
        'material_work_total_amount',
        'total_material_amount',
        'material_desc',
        'project_id__project_name'
    )
    return Response({
        "status": "success",
        "title": "Materials",
        "data": materials
    })

@api_view(['POST'])
def insert_update_material(request):
    material_id = request.data.get('material_id')
    material_owner_name = request.data.get('material_owner_name')
    material_used_date = request.data.get('material_used_date')
    material_type_id = request.data.get('material_type_id')
    work_type_id = request.data.get('work_type_id')
    material_work_number = request.data.get('material_work_number')
    material_work_amount = request.data.get('material_work_amount')
    material_work_total_amount = request.data.get('material_work_total_amount')
    total_material_amount = request.data.get('total_material_amount')
    material_desc = request.data.get('material_desc')
    project_id = request.data.get('project_id')

    material_type_instance = Material_Types.objects.get(material_type_id=material_type_id)
    work_type_instance = Work_Types.objects.get(work_type_id=work_type_id)
    project_instance = Project.objects.get(project_id=project_id)
   

    if material_id:
        material = Materials.objects.get(material_id=material_id)
        material.material_owner_name = material_owner_name
        material.material_used_date = material_used_date
        material.material_type_id = material_type_instance
        material.work_type_id = work_type_instance
        material.material_work_number = material_work_number
        material.material_work_amount = material_work_amount
        material.material_work_total_amount = material_work_total_amount
        material.total_material_amount = total_material_amount
        material.material_desc = material_desc
        material.project_id = project_instance
        material.save()
        message = "Material updated successfully."
        
    else:
        material = Materials.objects.create(
            material_owner_name=material_owner_name,
            material_used_date=material_used_date,
            material_type_id=material_type_instance,
            work_type_id=work_type_instance,
            material_work_number=material_work_number,
            material_work_amount=material_work_amount,
            material_work_total_amount=material_work_total_amount,
            total_material_amount=total_material_amount,
            material_desc=material_desc,
            project_id=project_instance
        )
        message = "Material created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "material_id": material.material_id,
            "material_owner_name": material.material_owner_name,
            "material_used_date": material.material_used_date,
            "material_type_id": material.material_type_id.material_type_id,
            "work_type_id": material.work_type_id.work_type_id,
            "material_work_number": material.material_work_number,
            "material_work_amount": material.material_work_amount,
            "material_work_total_amount": material.material_work_total_amount,
            "total_material_amount": material.total_material_amount,
            "material_desc": material.material_desc,
            "project_id": material.project_id.project_id
        }
    })

@api_view(['DELETE'])
def delete_material(request):
    material_id = request.data.get('material_id')

    if not material_id:
        return Response({
            "status": "error",
            "message": "Material ID is required."
        }, status=400)

    try:
        material = Materials.objects.get(material_id=material_id)
        material.delete()
        return Response({
            "status": "success",
            "message": "Material deleted successfully."
        })
    except Materials.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Material not found."
        }, status=404)

@api_view(['GET'])
def show_person_work_machine(request):
    person_work_machine = Person_Work_Machine.objects.all().values(
        'pwm_id',
        'pwm_machine_name',
        'pwm_machine_owner_name',
        'pwm_machine_owner_number',
        'working_machine_id__working_machine_name',
        'pwm_person_joining_date',
        'pwm_person_contact_number',
        'pwm_person_payment_by',
        'pwm_person_payment_desc',
        'person_type_id__person_type_name',
        'person_id__person_name',
        'project_type_id__project_type_name',
        'project_id__project_name',
        'work_types_id__work_type_name',
        'pwm_work_number',
        'pwm_work_amount',
        'pwm_total_amount',
        'pwm_work_desc'
    )
    return Response({
        "status": "success",
        "title": "Person",
        "data": person_work_machine
    })


@api_view(['POST'])
def insert_update_person_work_machine(request):
    pwm_id = request.data.get('pwm_id')
    pwm_machine_name = request.data.get('pwm_machine_name')
    pwm_machine_owner_name = request.data.get('pwm_machine_owner_name')
    pwm_machine_owner_number = request.data.get('pwm_machine_owner_number')
    working_machine_id = request.data.get('working_machine_id')
    pwm_person_joining_date = request.data.get('pwm_person_joining_date')
    pwm_person_contact_number = request.data.get('pwm_person_contact_number')
    pwm_person_payment_by = request.data.get('pwm_person_payment_by')
    pwm_person_payment_desc = request.data.get('pwm_person_payment_desc')
    person_type_id = request.data.get('person_type_id')
    person_id = request.data.get('person_id')
    project_type_id = request.data.get('project_type_id')
    project_id = request.data.get('project_id')
    work_types_id = request.data.get('work_types_id')
    pwm_work_number = request.data.get('pwm_work_number')
    pwm_work_amount = request.data.get('pwm_work_amount')
    pwm_total_amount = request.data.get('pwm_total_amount')
    pwm_work_desc = request.data.get('pwm_work_desc')

    working_machine_instance = Working_Machines.objects.get(pk=working_machine_id)
    person_type_instance = Person_Type.objects.get(pk=person_type_id)
    person_instance = Person.objects.get(pk=person_id)
    project_type_instance = Project_Types.objects.get(pk=project_type_id)
    project_instance = Project.objects.get(pk=project_id)
    work_type_instance = Work_Types.objects.get(pk=work_types_id)

    if pwm_id:
        pwm = Person_Work_Machine.objects.get(pwm_id=pwm_id)
        pwm.pwm_machine_name = pwm_machine_name
        pwm.pwm_machine_owner_name = pwm_machine_owner_name
        pwm.pwm_machine_owner_number = pwm_machine_owner_number
        pwm.working_machine_id = working_machine_instance
        pwm.pwm_person_joining_date = pwm_person_joining_date
        pwm.pwm_person_contact_number = pwm_person_contact_number
        pwm.pwm_person_payment_by = pwm_person_payment_by
        pwm.pwm_person_payment_desc = pwm_person_payment_desc
        pwm.person_type_id = person_type_instance
        pwm.person_id = person_instance
        pwm.project_type_id = project_type_instance
        pwm.project_id = project_instance
        pwm.work_types_id = work_type_instance
        pwm.pwm_work_number = pwm_work_number
        pwm.pwm_work_amount = pwm_work_amount
        pwm.pwm_total_amount = pwm_total_amount
        pwm.pwm_work_desc = pwm_work_desc
        pwm.save()
        message = "Person Work Machine updated successfully."

    else:
        pwm = Person_Work_Machine.objects.create(
            pwm_machine_name=pwm_machine_name,
            pwm_machine_owner_name=pwm_machine_owner_name,
            pwm_machine_owner_number=pwm_machine_owner_number,
            working_machine_id=working_machine_instance,
            pwm_person_joining_date=pwm_person_joining_date,
            pwm_person_contact_number=pwm_person_contact_number,
            pwm_person_payment_by=pwm_person_payment_by,
            pwm_person_payment_desc=pwm_person_payment_desc,
            person_type_id=person_type_instance,
            person_id=person_instance,
            project_type_id=project_type_instance,
            project_id=project_instance,
            work_types_id=work_type_instance,
            pwm_work_number=pwm_work_number,
            pwm_work_amount=pwm_work_amount,
            pwm_total_amount=pwm_total_amount,
            pwm_work_desc=pwm_work_desc
        )
        message = "Person Work Machine created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "pwm_id": pwm.pwm_id,
            "pwm_machine_name": pwm.pwm_machine_name,
            "pwm_machine_owner_name": pwm.pwm_machine_owner_name,
            "pwm_machine_owner_number": pwm.pwm_machine_owner_number,
            "working_machine_id": pwm.working_machine_id.working_machine_id,
            "pwm_person_joining_date": pwm.pwm_person_joining_date,
            "pwm_person_contact_number": pwm.pwm_person_contact_number,
            "pwm_person_payment_by": pwm.pwm_person_payment_by,
            "pwm_person_payment_desc": pwm.pwm_person_payment_desc,
            "person_type_id": pwm.person_type_id.person_type_id,
            "person_id": pwm.person_id.person_id,
            "project_type_id": pwm.project_type_id.project_type_id,
            "project_id": pwm.project_id.project_id,
            "work_types_id": pwm.work_types_id.work_type_id,
            "pwm_work_number": pwm.pwm_work_number,
            "pwm_work_amount": pwm.pwm_work_amount,
            "pwm_total_amount": pwm.pwm_total_amount,
            "pwm_work_desc": pwm.pwm_work_desc
        }
    })

@api_view(['DELETE'])
def delete_person_work_machine(request):
    pwm_id = request.data.get('pwm_id')

    if not pwm_id:
        return Response({
            "status": "error",
            "message": "PWM ID is required."
        }, status=400)

    try:
        pwm = Person_Work_Machine.objects.get(pwm_id=pwm_id)
        pwm.delete()
        return Response({
            "status": "success",
            "message": "Person Work Machine deleted successfully."
        })
    except Person_Work_Machine.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Person Work Machine not found."
        }, status=404)
    

@api_view(['GET'])
def show_document_types(request):
    document_types = Document_Types.objects.all().values(
        'document_type_id',
        'document_type_name'
    )
    return Response({
        "status": "success",
        "data": document_types
    })


@api_view(['POST'])
def insert_update_document_type(request):
    document_type_id = request.data.get('document_type_id')
    document_type_name = request.data.get('document_type_name')

    if document_type_id:
            document_type = Document_Types.objects.get(document_type_id=document_type_id)
            document_type.document_type_name = document_type_name
            document_type.save()
            message = "Document type updated successfully."
    else:
        document_type = Document_Types.objects.create(
            document_type_name=document_type_name
        )
        message = "Document type created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "document_type_id": document_type.document_type_id,
            "document_type_name": document_type.document_type_name
        }
    })

@api_view(['DELETE'])
def delete_document_type(request):
    document_type_id = request.data.get('document_type_id')

    if not document_type_id:
        return Response({
            "status": "error",
            "message": "Document type ID is required."
        }, status=400)

    try:
        document_type = Document_Types.objects.get(document_type_id=document_type_id)
        document_type.delete()
        return Response({
            "status": "success",
            "message": "Document type deleted successfully."
        })
    except Document_Types.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Document type not found."
        }, status=404)
    
@api_view(['GET'])
def show_documents(request):
    documents = Documents.objects.all().values(
        'document_id',
        'document_name',
        'document_date',
        'document_unique_code',
        'document_file',
        'document_type_id',
        'document_type_id__document_type_name'
    )
    return Response({
        "status": "success",
        "title": "Documents",
        "data": documents
    })


@api_view(['POST'])
def insert_update_document(request):
    document_id = request.data.get('document_id')
    document_name = request.data.get('document_name')
    document_unique_code = request.data.get('document_unique_code')
    document_type_id = request.data.get('document_type_id')
    document_file = request.FILES.get('document_file')

    document_type = Document_Types.objects.get(document_type_id=document_type_id)
   

    if document_id:
            document = Documents.objects.get(document_id=document_id)
            document.document_name = document_name
            document.document_unique_code = document_unique_code
            document.document_type_id = document_type
            if document_file:
                document.document_file = document_file
            document.save()
            message = "Document updated successfully."
    else:
        document = Documents.objects.create(
            document_name=document_name,
            document_unique_code=document_unique_code,
            document_type_id=document_type,
            document_file=document_file
        )
        message = "Document created successfully."

    return Response({
        "status": "success",
        "message": message,
        "data": {
            "document_id": document.document_id,
            "document_name": document.document_name,
            "document_date": document.document_date,
            "document_unique_code": document.document_unique_code,
            "document_file": document.document_file.url if document.document_file else None,
            "document_type_id": document.document_type_id.document_type_id,
            "document_type_name": document.document_type_id.document_type_name
        }
    })


@api_view(['DELETE'])
def delete_document(request):
    document_id = request.data.get('document_id')

    if not document_id:
        return Response({
            "status": "error",
            "message": "Document ID is required."
        }, status=400)

    try:
        document = Documents.objects.get(document_id=document_id)
        document.delete()
        return Response({
            "status": "success",
            "message": "Document deleted successfully."
        })
    except Documents.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Document not found."
        }, status=404)