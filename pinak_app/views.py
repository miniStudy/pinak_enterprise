from django.shortcuts import render
from pinak_app.models import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import Sum, FloatField
from django.db.models.functions import Cast
from django.contrib.auth import authenticate
from rest_framework import status
from .serializers import DocumentsSerializer
from django.conf import settings
from pinak_app.utilities import *
# Create your views here.

@api_view(['GET'])
def show_user(request):
    user_data = User.objects.all().values(
        'user_id',
        'user_name',
        'user_email',
        'user_contact'
    )

    return Response({
        'status': 'success',
        'title': 'User',
        'data': user_data
    })

@api_view(['GET', 'POST'])
def insert_update_user(request):
    if request.GET.get('getdata'):
        getdata = request.GET.get('getdata')
        user_data = User.objects.get(user_id = getdata)
        return Response({
            'status': 'success',
            'message': 'Data fetch successfully',
            'data': {
                'user_id': user_data.user_id,
                'user_name': user_data.user_name,
                'user_email': user_data.user_email,
                'user_password': user_data.user_password,
            }
        })
    
    if request.method == 'POST':
        user_id = request.data.get('user_id')
        user_name = request.data.get('user_name')
        user_email = request.data.get('user_email')
        user_contact = request.data.get('user_contact')
        user_password = request.data.get('user_password')

        if user_id:
            user_data = User.objects.get(user_id = user_id)
            user_data.user_name = user_name
            user_data.user_email = user_email
            user_data.user_contact = user_contact
            user_data.save()
            message = 'User data has been updated successfully'
        else:
            User.objects.create(user_name = user_name,
            user_email = user_email,
            user_contact = user_contact,
            user_password = user_password)
            message = 'User has been created successfully'

            return Response({
            'status': 'success',
            'title': 'User',
            'message': message
            })
    else:
            return Response({
                "status": "False"
            })

@api_view(['POST'])
def user_login(request):
    user_email = request.data.get('user_email')
    user_password = request.data.get('user_password')

    if not user_email or not user_password:
        return Response(
            {"error": "Email and password are required."},
        )

    user = User.objects.get(user_email=user_email, user_password=user_password)
    if user:
        return Response(
            {"message": "Login successful!"},
        )
    else:
        return Response(
            {"error": "Invalid email or password."},
            status=status.HTTP_401_UNAUTHORIZED
        )

@api_view(['GET'])
def show_comapny_details(request):
    comapny_details_data = Company_Details.objects.first()
    comapny_details_data = {'company_contact_number': comapny_details_data.company_contact_number, 'company_owner_name': comapny_details_data.company_owner_name, 'company_owner_contact': comapny_details_data.company_owner_contact, 'company_address': comapny_details_data.company_address,'company_sharuaati_shilak':comapny_details_data.company_sharuaati_shilak}
    
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
    company_sharuaati_shilak = request.data.get('company_sharuaati_shilak')
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
            "company_logo_icon": company_logo_icon,
            "company_sharuaati_shilak":company_sharuaati_shilak
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
            "company_sharuaati_shilak":company_details.company_sharuaati_shilak,
            "company_logo": company_details.company_logo.url if company_details.company_logo else None,
            "company_logo_icon": company_details.company_logo_icon.url if company_details.company_logo_icon else None
        }
    })

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


@api_view(['POST', 'GET'])
def insert_update_person_type(request):
    person_type_id = request.data.get('person_type_id')
    person_type_name = request.data.get('person_type_name')

    if request.GET.get('getdata_id'):
        person_type_obj = Person_Type.objects.get(person_type_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            'person_type_id': person_type_obj.person_type_id,
            'person_type_name': person_type_obj.person_type_name,
        }
        })
    if request.method == 'POST':
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
    else:
        return Response({
            "status": "False"
        })


@api_view(['DELETE'])
def delete_person_type(request):
    person_type_id = request.GET.get('person_type_id')

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
    if request.GET.get('machine_type_id'):
        machine_type_id = request.GET.get('machine_type_id')
        machine_type = Machine_Types.objects.get(machine_type_id=machine_type_id)
        machine_type.delete()

        return Response({
            "status": "success",
            "message": "Machine type deleted successfully."
        })
    else:
        return Response({
            "status": "Error",
            "message": "Something went wrong",
        })
# =========================================================================

@api_view(['GET'])
def show_office_kharch_types(request):
    office_kharch_types_data = Office_kharch_Types.objects.all().values('office_kharch_type_id', 'office_kharch_type_name')
    return Response({
        "status": "success",
        "data": office_kharch_types_data
    })

@api_view(['POST','GET'])
def insert_update_office_kharch_types(request):
    office_kharch_type_id = request.data.get('office_kharch_type_id')
    office_kharch_type_name = request.data.get('office_kharch_type_name')
    message = ''
    if request.GET.get('getdata_id'):
        office_kharch_type_obj = Office_kharch_Types.objects.get(office_kharch_type_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            "office_kharch_type_id": office_kharch_type_obj.office_kharch_type_id,
            "office_kharch_type_name": office_kharch_type_obj.office_kharch_type_name,  
        }
        })

    if request.method == 'POST':
        if office_kharch_type_id:
            office_kharch_type_obj = Office_kharch_Types.objects.get(office_kharch_type_id=office_kharch_type_id)
            office_kharch_type_obj.office_kharch_type_name = office_kharch_type_name
            office_kharch_type_obj.save()
            message = "office_kharch updated successfully."
        
        else:
            office_kharch_type_obj = Office_kharch_Types.objects.create(
                office_kharch_type_name=office_kharch_type_name
            )
            message = "office_kharch created successfully."

    return Response({
        "status": "success",
        "message": message,
    })

@api_view(['DELETE'])
def delete_office_kharch_types(request):
    if request.GET.get('office_kharch_type_id'):
        office_kharch_type_id = request.GET.get('office_kharch_type_id')
        office_kharch_type_obj = Office_kharch_Types.objects.get(office_kharch_type_id=office_kharch_type_id)
        office_kharch_type_obj.delete()

        return Response({
            "status": "success",
            "message": "office_kharch_type deleted successfully."
        })
    else:
        return Response({
            "status": "Error",
            "message": "Something went wrong",
        })


# =========================================================================

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

@api_view(['POST', 'GET'])
def insert_update_project_type(request):
    project_type_id = request.data.get('project_type_id')
    project_type_name = request.data.get('project_type_name')
    project_type_details = request.data.get('project_type_details')


    if request.GET.get('getdata_id'):
        project_type_obj = Project_Types.objects.get(project_type_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            'project_type_id': project_type_obj.project_type_id,
            'project_type_name': project_type_obj.project_type_name,
            'project_type_details': project_type_obj.project_type_details
        }
        })

    if request.method == 'POST':
        if project_type_id:
            project_type = Project_Types.objects.get(project_type_id = project_type_id)
            project_type.project_type_name = project_type_name
            project_type.project_type_details = project_type_details
            project_type.save()
            message = "Project type updated successfully."
        
        else:
            project_type = Project_Types.objects.create(project_type_name = project_type_name, project_type_details= project_type_details)
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
    else:
        return Response({
            "status": "False"
        })

@api_view(['DELETE'])
def delete_project_type(request):
    project_type_id = request.GET.get('project_type_id')
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
def show_work_types(request):
    work_types = Work_Types.objects.all().values(
        'work_type_id',
        'work_type_name',
    )
    return Response({
        "status": "success",
        "data": work_types
    })

@api_view(['POST', 'GET'])
def insert_update_work_type(request):
    work_type_id = request.data.get('work_type_id')
    work_type_name = request.data.get('work_type_name')
    work_type_details = request.data.get('work_type_details')

    if request.GET.get('getdata_id'):
        work_type_obj = Work_Types.objects.get(work_type_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            'work_type_id': work_type_obj.work_type_id,
            'work_type_name': work_type_obj.work_type_name,    
        }
        })
    
    if request.method == 'POST':
        if work_type_id:
            work_type = Work_Types.objects.get(work_type_id=work_type_id)
            work_type.work_type_name = work_type_name
            work_type.save()
            message = "Work type updated successfully."
            
        else:
            work_type = Work_Types.objects.create(
                work_type_name=work_type_name,
            )
            message = "Work type created successfully."

        return Response({
            "status": "success",
            "message": message,
        })
    else:
        return Response({
            'status': 'False'
        })

@api_view(['DELETE'])
def delete_work_type(request):
    work_type_id = request.GET.get('work_type_id')

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


@api_view(['POST', 'GET'])
def insert_update_material_type(request):
    material_type_id = request.data.get('material_type_id')
    material_type_name = request.data.get('material_type_name')

    if request.GET.get('getdata_id'):
        material_type_obj = Material_Types.objects.get(material_type_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            'material_type_id': material_type_obj.material_type_id,
            'material_type_name': material_type_obj.material_type_name,               
        }
        })

    if request.method == 'POST':
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
    else:
        return Response({
            'status': 'False'
        })


@api_view(['DELETE'])
def delete_material_type(request):
    material_type_id = request.GET.get('material_type_id')

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
def show_maintenance_types(request):
    maintenance_types = Maintenance_Types.objects.all().values('maintenance_type_id', 'maintenance_type_name')

    return Response({
        "status": "success",
        "title": "Maintenance Type",
        "data": maintenance_types
    })

@api_view(['POST', 'GET'])
def insert_update_maintenance_type(request):
    maintenance_type_id = request.data.get('maintenance_type_id')
    maintenance_type_name = request.data.get('maintenance_type_name')

    if request.GET.get('getdata_id'):
        maintenance_type_obj = Maintenance_Types.objects.get(maintenance_type_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            "maintenance_type_id": maintenance_type_obj.maintenance_type_id,
            "maintenance_type_name": maintenance_type_obj.maintenance_type_name,
        }
        })

    
    if request.method == 'POST':
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
    else:
        return Response({
            'status': "False"
        })


@api_view(['DELETE'])
def delete_maintenance_type(request):
    maintenance_type_id = request.GET.get('maintenance_type_id')
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
def show_pay_types(request):
    pay_types = Pay_Types.objects.all().values(
        'pay_type_id',
        'pay_type_name',
    )
    return Response({
        "status": "success",
        "data": pay_types
    })

@api_view(['POST', 'GET'])
def insert_update_pay_type(request):
    pay_type_id = request.data.get('pay_type_id')
    pay_type_name = request.data.get('pay_type_name')

    if request.GET.get('getdata_id'):
        pay_type_obj = Pay_Types.objects.get(pay_type_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            'pay_type_id': pay_type_obj.pay_type_id,
            'pay_type_name': pay_type_obj.pay_type_name,
        }
        })

    if request.method == 'POST':
        if pay_type_id:
            pay_type = Pay_Types.objects.get(pay_type_id=pay_type_id)
            pay_type.pay_type_name = pay_type_name
            pay_type.save()
            message = "Pay type updated successfully."
        else:
            pay_type = Pay_Types.objects.create(
                pay_type_name=pay_type_name,

            )
            message = "Pay type created successfully."

        return Response({
            "status": "success",
            "message": message,
            "data": {
                "pay_type_id": pay_type.pay_type_id,
                "pay_type_name": pay_type.pay_type_name,

            }
        })
    else:
        return Response({
            "status": "False"
        })

@api_view(['DELETE'])
def delete_pay_type(request):
    pay_type_id = request.GET.get('pay_type_id')

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
def show_persons(request):
    persons = Person.objects.exclude(person_status=0)
    if request.GET.get('person_id'):
        person_id = request.GET.get('person_id')
        persons = persons.filter(person_id = person_id)


    persons = persons.values(
        'person_id',
        'person_name',
        'person_contact_number',
        'person_salary',
        'person_register_date',
        'person_status',
        'person_address',
        'person_other_details',
        'person_business_job_name',
        'person_business_job_company_num',
        'person_business_job_address',
        'person_gst',
        'person_type_id__person_type_id',
        'person_type_id__person_type_name',
        'person_types_for_project'
    )

    Salary_data = Salary.objects.all()
    maintenance_data = Machine_Maintenance.objects.all()
    daydetail_data = Project_Day_Details.objects.all()
    project_data = Project.objects.all()
    project_machinedata =  Project_Machine_Data.objects.all()
    projectmaterialdata = Project_Material_Data.objects.all()
    manetcreditdebitdata = Money_Debit_Credit.objects.all()
    for x in persons: 
        
        hisabdata = levani_aapvani_rakam(request,x['person_id'])
        x['kul_rakam']=hisabdata['final_rakam']     
        if x['person_id']==1:
            x['kul_rakam'] = '0'
    
    person_types = Person_Type.objects.all().values(
        'person_type_id', 
        'person_type_name'
    )     

    allPersons = Person.objects.exclude(person_status=0).values('person_id','person_name')
    
    return Response({
        "status": "success",
        "title": "Person Data",
        "person_types": list(person_types),
        "data": list(persons),
        "allPersons":allPersons,
    })


@api_view(['POST', 'GET'])
def insert_update_person(request):
    person_types_data = list(Person_Type.objects.all().values('person_type_id', 'person_type_name'))

    if request.method == 'GET':
        person_id = request.GET.get('getdata_id')
        if person_id:
            person_obj = get_object_or_404(Person, person_id=person_id)
            return Response({
                "status": "success",
                "message": "Data fetched successfully",
                "data": {
                    "person_id": person_obj.person_id,
                    "person_name": person_obj.person_name,
                    "person_contact_number": person_obj.person_contact_number,
                    "person_register_date": person_obj.person_register_date,
                    "person_status": person_obj.person_status,
                    "person_address": person_obj.person_address,
                    "person_salary":person_obj.person_salary,
                    "person_other_details": person_obj.person_other_details,
                    "person_business_job_name": person_obj.person_business_job_name,
                    "person_business_job_company_num": person_obj.person_business_job_company_num,
                    "person_business_job_address": person_obj.person_business_job_address,
                    "person_gst": person_obj.person_gst,
                    "person_types_for_project": person_obj.person_types_for_project,
                    "person_type_id": person_obj.person_type_id.person_type_id,
                },
                "person_types": person_types_data
            })

        return Response({
            "status": "failed",
            "message": "No ID provided for fetching data."
        })

    elif request.method == 'POST':
        person_id = request.data.get('person_id')
        person_name = request.data.get('person_name')
        person_contact_number = request.data.get('person_contact_number')
        person_status = request.data.get('person_status', True)
        person_address = request.data.get('person_address')
        person_salary = request.data.get('person_salary')
        person_other_details = request.data.get('person_other_details')
        person_business_job_name = request.data.get('person_business_job_name')
        person_business_job_company_num = request.data.get('person_business_job_company_num')
        person_business_job_address = request.data.get('person_business_job_address')
        person_gst = request.data.get('person_gst')
        person_types_for_project = request.data.get('person_types_for_project')
        person_type_id = request.data.get('person_type_id')

        if not all([person_name, person_contact_number, person_type_id]):
            return Response({
                "status": "failed",
                "message": "All required fields must be provided."
            })

        person_type_instance = get_object_or_404(Person_Type, person_type_id=person_type_id)

        if person_id:
            person = get_object_or_404(Person, person_id=person_id)
            person.person_name = person_name
            person.person_contact_number = person_contact_number
            person.person_status = person_status
            person.person_address = person_address
            person.person_salary = person_salary
            person.person_other_details = person_other_details
            person.person_business_job_name = person_business_job_name
            person.person_business_job_company_num = person_business_job_company_num
            person.person_business_job_address = person_business_job_address
            person.person_gst = person_gst
            person.person_types_for_project = person_types_for_project
            person.person_type_id = person_type_instance
            person.save()
            message = "Person updated successfully."
        else:
            person = Person.objects.create(
                person_name=person_name,
                person_contact_number=person_contact_number,
                person_status=person_status,
                person_address=person_address,
                person_other_details=person_other_details,
                person_business_job_name=person_business_job_name,
                person_business_job_company_num=person_business_job_company_num,
                person_business_job_address=person_business_job_address,
                person_salary = person_salary,
                person_gst=person_gst,
                person_types_for_project=person_types_for_project,
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
                "person_register_date": person.person_register_date,
                "person_status": person.person_status,
                "person_address": person.person_address,
                "person_other_details": person.person_other_details,
                "person_business_job_name": person.person_business_job_name,
                "person_business_job_company_num": person.person_business_job_company_num,
                "person_business_job_address": person.person_business_job_address,
                "person_gst": person.person_gst,
                "person_salary":person.person_salary,
                "person_types_for_project": person.person_types_for_project,
                "person_type_id": person.person_type_id.person_type_id
            },
            "person_types": person_types_data
        })

    return Response({
        "status": "failed",
        "message": "Invalid request method."
    })
        

@api_view(['DELETE'])
def delete_person(request):
    person_id = request.GET.get('person_id')

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
def show_bank_details(request):
    bank_details_data = Bank_Details.objects.filter(company_bank_account = False).values(
        'bank_id',
        'bank_name',
        'bank_branch',
        'bank_account_number',
        'bank_ifsc_code',
        'bank_account_holder',
        'bank_initial_amount',
        'bank_current_amount',
        'bank_open_closed',
        'person_id__person_name',
        'person_id__person_contact_number',
    )

    company_bank_details_data = Bank_Details.objects.filter(company_bank_account = True).values(
        'bank_id',
        'bank_name',
        'bank_branch',
        'bank_account_number',
        'bank_ifsc_code',
        'bank_account_holder',
        'bank_initial_amount',
        'bank_current_amount',
        'bank_open_closed',
        'person_id__person_name',
        'person_id__person_contact_number',
    )
    for x in company_bank_details_data:
        x['bank_current_amount_data'] = currentbank_amount(request, x['bank_id'])

    company_person_name = [persons.person_id.person_name for persons in Bank_Details.objects.filter(company_bank_account = True)]

    credit_debit_data = Money_Debit_Credit.objects.filter(money_payment_mode = 'BANK').values('sender_person_id__person_name','sender_person_id__person_contact_number', 'sender_person_id__person_contact_number', 'receiver_person_id__person_name', 'money_amount', 'pay_type_id__pay_type_name', 'money_payment_mode', 'money_date', 'sender_bank_id__bank_name', 'receiver_bank_id__bank_name', 'money_payment_details')

    bank_credit_total = 0
    bank_debit_total = 0
    for credit_debit in credit_debit_data:
        
        if credit_debit['sender_person_id__person_name'] in company_person_name:
            credit_debit['credit_debit'] = 'Debit'
            bank_debit_total += float(credit_debit['money_amount'])
        else:
            credit_debit['credit_debit'] = 'Credit'
            bank_credit_total += float(credit_debit['money_amount'])

    persons = Person.objects.filter(person_status = True).values(
        'person_id',
        'person_name',
        'person_contact_number',
    )


    bank_cash_data = bank_cash.objects.all().values(
        'bank_cash_id',
        'credit_debit',
        'amount',
        'bank_id__bank_name',
        'date',
        'details'
    )

    return Response({
        "status": "success",
        "title": "Bank",
        "persons": persons,
        "data": bank_details_data,
        "company_bank_details_data": company_bank_details_data,
        "credit_debit_data": credit_debit_data,
        "bank_credit_total": bank_credit_total,
        "bank_debit_total": bank_debit_total,
        "bank_cash_data": bank_cash_data,
    })

@api_view(['POST', 'GET'])
def insert_update_bank_detail(request):
    persons = Person.objects.exclude(person_status=0).values(
        'person_id',
        'person_name'
    )
    if request.method == 'GET':
        getdata_id = request.GET.get('getdata_id')
        if getdata_id:
            bank_obj = Bank_Details.objects.select_related('person_id').get(bank_id=getdata_id)
            return Response({
                "status": "success",
                "message": "Data Fetched Successfully",
                "data": {
                    "bank_id": bank_obj.bank_id,
                    "bank_name": bank_obj.bank_name,
                    "bank_branch": bank_obj.bank_branch,
                    "bank_account_number": bank_obj.bank_account_number,
                    "bank_ifsc_code": bank_obj.bank_ifsc_code,
                    "bank_account_holder": bank_obj.bank_account_holder,
                    "bank_initial_amount": bank_obj.bank_initial_amount,
                    "bank_current_amount":bank_obj.bank_current_amount,
                    "bank_open_closed": bank_obj.bank_open_closed,
                    "person_id": bank_obj.person_id.person_id,
                    "company_bank_account": bank_obj.company_bank_account
                },
                'persons': persons
            })
        return Response({
            "status": "failed",
            "message": "No ID provided for fetching data."
        })

    elif request.method == 'POST':
        bank_id = request.data.get('bank_id')
        bank_name = request.data.get('bank_name')
        bank_branch = request.data.get('bank_branch')
        bank_account_number = request.data.get('bank_account_number')
        bank_ifsc_code = request.data.get('bank_ifsc_code')
        bank_account_holder = request.data.get('bank_account_holder')
        bank_initial_amount = request.data.get('bank_initial_amount')
        bank_open_closed = request.data.get('bank_open_closed')
        person_id = request.data.get('person_id')
        company_bank_account = request.data.get('company_bank_account')

        if not all([bank_name, bank_branch, bank_account_number, bank_ifsc_code, person_id]):
            return Response({
                "status": "failed",
                "message": "All required fields must be provided."
            })

        person_instance = get_object_or_404(Person, person_id=person_id)

        if bank_id:
            bank_detail = get_object_or_404(Bank_Details, bank_id=bank_id)
            bank_detail.bank_name = bank_name
            bank_detail.bank_branch = bank_branch
            bank_detail.bank_account_number = bank_account_number
            bank_detail.bank_ifsc_code = bank_ifsc_code
            bank_detail.bank_account_holder = bank_account_holder
            bank_detail.bank_initial_amount = bank_initial_amount
            bank_detail.bank_open_closed = bank_open_closed
            bank_detail.person_id = person_instance
            bank_detail.company_bank_account = company_bank_account
            bank_detail.save()
            message = "Bank details updated successfully."
        else:
            bank_detail = Bank_Details.objects.create(
                bank_name=bank_name,
                bank_branch=bank_branch,
                bank_account_number=bank_account_number,
                bank_ifsc_code=bank_ifsc_code,
                bank_current_amount = bank_initial_amount,
                bank_account_holder=bank_account_holder,
                bank_initial_amount=bank_initial_amount,
                bank_open_closed=bank_open_closed,
                person_id=person_instance,
                company_bank_account = company_bank_account,
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
                "bank_initial_amount": bank_detail.bank_initial_amount,
                "bank_open_closed": bank_detail.bank_open_closed,
                "person_id": bank_detail.person_id.person_id,
                "person_name": bank_detail.person_id.person_name,
                "person_contact_number": bank_detail.person_id.person_contact_number,
                "person_types_for_project": bank_detail.person_id.person_types_for_project,
                "person_type_name": bank_detail.person_id.person_type_id.person_type_name,
                "company_bank_account": bank_detail.company_bank_account,
            },
            'persons': persons
        })

    return Response({
        "status": "failed",
        "message": "Invalid request method."
    })


@api_view(['DELETE'])
def delete_bank_detail(request):
    if request.GET.get('bank_id'):
        bank_id = request.GET.get('bank_id')
        bank_detail = Bank_Details.objects.get(bank_id=bank_id)     
        bank_detail.delete()
            
        return Response({
            "status": "success",
            "message": "Bank details deleted successfully."
        })
    else:
        return Response({
            "status": "Error",
            "message": "Something went wrong",
        })




@api_view(['GET'])
def show_machines(request):
    company_machines = Machines.objects.all().values(
        'machine_id', 
        'machine_name', 
        'machine_number_plate', 
        'machine_register_date', 
        'machine_own', 
        'machine_condition', 
        'machine_working', 
        'machine_types_id__machine_type_name', 
        'machine_details', 
        'machine_owner_id__person_id',
        'machine_owner_id__person_name',
        'machine_buy_price', 
        'machine_buy_date', 
        'machine_sold_price', 
        'machine_sold_out_date', 
        'machine_other_details',
    )
    machine_types_data = Machine_Types.objects.all().values(
        'machine_type_id', 
        'machine_type_name'
    )

    persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name', 'person_contact_number')
    machine_rented_work_type = Work_Types.objects.all().values('work_type_name','work_type_id')
    return Response({
        "status": "success",
        "title": "Machine",
        "data": company_machines,
        "machine_types": machine_types_data,
        "persons_data":persons_data,
        'machine_rented_work_type':machine_rented_work_type
    })


@api_view(['POST', 'GET'])
def insert_update_machine(request):
    if request.method == 'POST':
        machine_id = request.data.get('machine_id')
        machine_name = request.data.get('machine_name')
        machine_number_plate = request.data.get('machine_number_plate')
        machine_register_date = request.data.get('machine_register_date')
        machine_own = request.data.get('machine_own')
        
        machine_condition = request.data.get('machine_condition')
        machine_working = request.data.get('machine_working')
        machine_types_id = request.data.get('machine_types_id')
        machine_details = request.data.get('machine_details')
        machine_owner_id = request.data.get('machine_owner_id')
        if machine_own == 'Company':
            machine_owner_id = 1
        
        machine_buy_price = request.data.get('machine_buy_price')
        

        machine_buy_date = request.data.get('machine_buy_date')
        machine_sold_price = request.data.get('machine_sold_price')
        machine_sold_out_date = request.data.get('machine_sold_out_date')
        machine_other_details = request.data.get('machine_other_details')

        machine_types_instance = Machine_Types.objects.get(machine_type_id=machine_types_id)
        if machine_owner_id:
            machine_owner_id = Person.objects.get(person_id = machine_owner_id)


    if request.GET.get('getdata_id'):
        machine_obj = Machines.objects.get(machine_id=request.GET.get('getdata_id'))
        return Response({
            "status": "success",
            "message": 'Data Fetched Successfully',
            "data": { 
                "machine_id": machine_obj.machine_id,
                "machine_name": machine_obj.machine_name,
                "machine_number_plate": machine_obj.machine_number_plate,
                "machine_register_date": machine_obj.machine_register_date,
                "machine_own": machine_obj.machine_own,
                "machine_condition": machine_obj.machine_condition,
                "machine_working": machine_obj.machine_working,
                "machine_types_id": machine_obj.machine_types_id.machine_type_id,
                "machine_types_name": machine_obj.machine_types_id.machine_type_name,
                "machine_details": machine_obj.machine_details,
                "machine_owner_id": machine_obj.machine_owner_id.person_id,
                "machine_buy_price": machine_obj.machine_buy_price,
                "machine_buy_date": machine_obj.machine_buy_date if machine_obj.machine_buy_date else None,
                "machine_sold_price": machine_obj.machine_sold_price,
                "machine_sold_out_date": machine_obj.machine_sold_out_date if machine_obj.machine_sold_out_date else None,
                "machine_other_details": machine_obj.machine_other_details,
            },
        })

    if request.method == 'POST':
        if machine_id:
            machine = Machines.objects.get(machine_id=machine_id)
            machine.machine_name = machine_name
            machine.machine_number_plate = machine_number_plate
            machine.machine_register_date = machine_register_date if machine_register_date else None
            machine.machine_own = machine_own
            machine.machine_condition = machine_condition
            machine.machine_working = machine_working
            machine.machine_types_id = machine_types_instance
            machine.machine_details = machine_details
            machine.machine_owner_id = machine_owner_id
            machine.machine_buy_price = machine_buy_price
            machine.machine_buy_date = machine_buy_date if machine_buy_date else None
            machine.machine_sold_price = machine_sold_price
            machine.machine_sold_out_date = machine_sold_out_date if machine_sold_out_date else None
            machine.machine_other_details = machine_other_details
            machine.save()
            message = "Machine details updated successfully."
        else:
            machine = Machines.objects.create(
                machine_name=machine_name,
                machine_number_plate=machine_number_plate,
                machine_register_date=machine_register_date if machine_register_date else None,
                machine_own=machine_own,
                machine_condition=machine_condition,
                machine_working=machine_working,
                machine_types_id=machine_types_instance,
                machine_details=machine_details,
                machine_owner_id = machine_owner_id,
                machine_buy_price=machine_buy_price,
                machine_buy_date=machine_buy_date if machine_buy_date else None,
                machine_sold_price=machine_sold_price,
                machine_sold_out_date=machine_sold_out_date if machine_sold_out_date else None,
                machine_other_details=machine_other_details
            )
            message = "Machine details created successfully."

        return Response({
            "status": "success",
            "message": message,
            "data": {
                "machine_id": machine.machine_id,
                "machine_name": '{} - {}'.format(machine.machine_name,machine_number_plate),
                "machine_number_plate": machine.machine_number_plate,
                "machine_register_date": machine.machine_register_date,
                "machine_own": machine.machine_own,
                "machine_condition": machine.machine_condition,
                "machine_working": machine.machine_working,
                "machine_types_id": machine.machine_types_id.machine_type_id,
                "machine_types_name": machine.machine_types_id.machine_type_name,
                "machine_details": machine.machine_details,
                "machine_owner_id": machine.machine_owner_id.person_id,
                "machine_buy_price": machine.machine_buy_price,
                "machine_buy_date": machine.machine_buy_date,
                "machine_sold_price": machine.machine_sold_price,
                "machine_sold_out_date": machine.machine_sold_out_date,
                "machine_other_details": machine.machine_other_details,
            },
        })
    else:
        return Response({
            'status': "False"
        })


@api_view(['DELETE'])
def delete_machine(request):
    if request.GET.get('machine_id'):
        machine_id = request.GET.get('machine_id')
        if not machine_id:
            return Response({
                "status": "error",
                "message": "No machine ID provided"
            }, status=400)
        try:
            machine = Machines.objects.get(machine_id=machine_id)
            machine.delete()

            return Response({
                "status": "success",
                "message": "Machine deleted successfully."
            })

        except Machines.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Machine with the provided ID not found."
            }, status=404)
    else:
        return Response({
            "status": "Error",
            "message": "Something went wrong",
        })


@api_view(['GET'])
def show_money_debit_credit(request):
    money_debit_credit_data = Money_Debit_Credit.objects.all()

    if request.GET.get('sender_id'):
        sender_id = request.GET.get('sender_id')
        if sender_id:
            money_debit_credit_data = money_debit_credit_data.filter(sender_person_id__person_id = sender_id)

    if request.GET.get('receiver_id'):
        receiver_id = request.GET.get('receiver_id')
        if receiver_id:
            money_debit_credit_data = money_debit_credit_data.filter(receiver_person_id__person_id = receiver_id)

    if request.GET.get('pay_type_id'):
        pay_type_id = request.GET.get('pay_type_id')
        if pay_type_id:
            money_debit_credit_data = money_debit_credit_data.filter(pay_type_id__pay_type_id = pay_type_id)


    money_debit_credit_data = money_debit_credit_data.values(
        'money_id',
        'sender_person_id__person_name',
        'sender_person_id__person_contact_number',
        'receiver_person_id__person_name',
        'receiver_person_id__person_contact_number',
        'pay_type_id__pay_type_name',
        'money_payment_mode',
        'money_amount',
        'money_date',
        'sender_bank_id__bank_name',
        'money_sender_cheque_no',
        'receiver_bank_id__bank_name',
        'money_payment_details',
        'machine_id__machine_name',
        'machine_id__machine_number_plate',
        'project_id__project_name',
    )

    money_credit_data = money_debit_credit_data.filter(sender_person_id__person_name = 'Pinak Enterprise').values(
        'money_id',
        'sender_person_id__person_name',
        'sender_person_id__person_contact_number',
        'receiver_person_id__person_name',
        'receiver_person_id__person_contact_number',
        'pay_type_id__pay_type_name',
        'money_amount',
        'money_payment_mode',
        'money_date',
        'sender_bank_id__bank_name',
        'receiver_bank_id__bank_name',
        'machine_id__machine_name',
        'project_id__project_name',
    )

    money_debit_data =  money_debit_credit_data.filter(receiver_person_id__person_name = 'Pinak Enterprise').values(
        'money_id',
        'sender_person_id__person_name',
        'sender_person_id__person_contact_number',
        'receiver_person_id__person_name',
        'receiver_person_id__person_contact_number',
        'pay_type_id__pay_type_name',
        'money_amount',
        'money_payment_mode',
        'money_date',
        'sender_bank_id__bank_name',
        'receiver_bank_id__bank_name',
        'machine_id__machine_name',
        'project_id__project_name',
    )

    persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name', 'person_contact_number')
    banks_data = Bank_Details.objects.filter(bank_open_closed=True).values('bank_id', 'bank_name', 'bank_account_number', 'person_id', 'person_id__person_name')
    pay_types_data = Pay_Types.objects.all().values('pay_type_id', 'pay_type_name')
    OfficeKharchtypesData = Office_kharch_Types.objects.all().values('office_kharch_type_id', 'office_kharch_type_name')
    machines_data = Machines.objects.all().values('machine_id', 'machine_name', 'machine_number_plate')  
    projects_data = Project.objects.all().values('project_id', 'project_name')
    OfficeKharchtypesData
    return Response({
        "status": "success",
        "title": "Money Transactions",
        "banks_data": banks_data,
        "persons_data": persons_data,
        "pay_types_data": pay_types_data,
        "machines_data": machines_data,
        "projects_data": projects_data,
        "data": money_debit_credit_data,
        "money_credit_data": money_credit_data,
        "OfficeKharchtypesData":OfficeKharchtypesData,
        "money_debit_data": money_debit_data,
    })  


@api_view(['POST', 'GET'])
def insert_update_money_debit_credit(request):
    persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name', 'person_contact_number')
    pay_types_data = Pay_Types.objects.all().values('pay_type_id', 'pay_type_name')
    machines_data = Machines.objects.all().values('machine_id', 'machine_name') 
    projects_data = Project.objects.all().values('project_id', 'project_name')
    bank_data = Bank_Details.objects.all().values('bank_id', 'bank_name', 'bank_account_number', 'person_id', 'person_id__person_name')
    if request.method == 'POST':
        money_id = request.data.get('money_id')
        sender_person_id = request.data.get('sender_person_id')
        receiver_person_id = request.data.get('receiver_person_id')
        pay_type_id = request.data.get('pay_type_id')
        money_payment_mode = request.data.get('money_payment_mode')
        money_amount = float(request.data.get('money_amount'))
        money_date = request.data.get('money_date')
        sender_bank_id = request.data.get('sender_bank_id')
        money_sender_cheque_no = request.data.get('money_sender_cheque_no')
        receiver_bank_id = request.data.get('receiver_bank_id')
        money_payment_details = request.data.get('money_payment_details')
        machine_id = request.data.get('machine_id')
        project_id = request.data.get('project_id')
        if machine_id:
            machine_instance = Machines.objects.get(machine_id=machine_id)
        else:
            machine_instance = None

        if project_id:
            project_instance = Project.objects.get(project_id=project_id)
        else:
            project_instance = None

        sender_person_instance = Person.objects.get(person_id=sender_person_id)
        receiver_person_instance = Person.objects.get(person_id=receiver_person_id)
        pay_type_instance = Pay_Types.objects.get(pay_type_id=pay_type_id)

        if sender_bank_id:
            sender_bank_instance = Bank_Details.objects.get(bank_id=sender_bank_id)
        else :
            sender_bank_instance = None

        if receiver_bank_id:
            receiver_bank_instance = Bank_Details.objects.get(bank_id=receiver_bank_id)
        else:
            receiver_bank_instance = None
        
        
        if money_id:
            money_debit_credit = Money_Debit_Credit.objects.get(money_id=money_id)
            money_debit_credit.sender_person_id = sender_person_instance
            money_debit_credit.receiver_person_id = receiver_person_instance
            money_debit_credit.pay_type_id = pay_type_instance
            money_debit_credit.money_payment_mode = money_payment_mode
            money_debit_credit.money_amount = money_amount
            money_debit_credit.money_date = money_date
            money_debit_credit.sender_bank_id = sender_bank_instance
            money_debit_credit.money_sender_cheque_no = money_sender_cheque_no
            money_debit_credit.receiver_bank_id = receiver_bank_instance
            money_debit_credit.money_payment_details = money_payment_details
            money_debit_credit.machine_id = machine_instance
            money_debit_credit.project_id = project_instance
            money_debit_credit.save()
            message = "Money Debit/Credit record updated successfully."
        else:
            money_debit_credit = Money_Debit_Credit.objects.create(
                sender_person_id = sender_person_instance,
                receiver_person_id = receiver_person_instance,
                pay_type_id=pay_type_instance,
                money_payment_mode=money_payment_mode,
                money_amount=money_amount,
                money_date=money_date,
                sender_bank_id = sender_bank_instance,
                money_sender_cheque_no=money_sender_cheque_no,
                receiver_bank_id = receiver_bank_instance,
                money_payment_details=money_payment_details,
                machine_id=machine_instance,
                project_id = project_instance,
            ) 
            if money_debit_credit.money_payment_mode=='BANK':
                if sender_person_id==1:
                    sender_bank_instance.bank_current_amount = sender_bank_instance.bank_current_amount - money_amount
                    sender_bank_instance.save()
                if receiver_person_id==1:
                    receiver_bank_instance.bank_current_amount = receiver_bank_instance.bank_current_amount + money_amount
            message = "Money Debit/Credit record created successfully."

        if not money_debit_credit.machine_id:
            machine_id = None
        else:
            machine_id = money_debit_credit.machine_id.machine_id

        return Response({
            "status": "success",
            "title": "Money Debit/Credit Transaction",
            "message": message,
            "data": {
                "money_id": money_debit_credit.money_id,
                "sender_person_id": money_debit_credit.sender_person_id.person_id,
                "receiver_person_id": money_debit_credit.receiver_person_id.person_id,
                "pay_type_id": money_debit_credit.pay_type_id.pay_type_id,
                "money_payment_mode": money_debit_credit.money_payment_mode,
                "money_amount": money_debit_credit.money_amount,
                "money_date": money_debit_credit.money_date,
                "sender_bank_id": None if money_debit_credit.sender_bank_id is None else money_debit_credit.sender_bank_id.bank_id,
                "money_sender_cheque_no": money_debit_credit.money_sender_cheque_no,
                "receiver_bank_id": None if money_debit_credit.receiver_bank_id is None else money_debit_credit.receiver_bank_id.bank_id,
                "money_payment_details": money_debit_credit.money_payment_details,
                "machine_id": machine_id,
                "project_id": project_id
            },
            "persons_data": persons_data,
            "pay_types_data": pay_types_data,
            "machines_data": machines_data,
            "banks_data": bank_data,
            "projects_data": projects_data,
        })

    elif request.GET.get('getdata_id'):
        money_debit_credit_obj = Money_Debit_Credit.objects.get(money_id=request.GET.get('getdata_id'))
        if not money_debit_credit_obj.machine_id:
            machine_id = None
        else:
            machine_id = money_debit_credit_obj.machine_id.machine_id
        if not money_debit_credit_obj.project_id:
            project_id = None
        else:
            project_id = money_debit_credit_obj.project_id.project_id
        return Response({
            "status": "success",
            "message": 'Data Fetched Successfully',
            "data": {
                "money_id": money_debit_credit_obj.money_id,
                "sender_person_id": money_debit_credit_obj.sender_person_id.person_id,
                "receiver_person_id": money_debit_credit_obj.receiver_person_id.person_id,
                "pay_type_id": money_debit_credit_obj.pay_type_id.pay_type_id,
                "money_payment_mode": money_debit_credit_obj.money_payment_mode,
                "money_amount": money_debit_credit_obj.money_amount,
                "money_date": money_debit_credit_obj.money_date,
                "sender_bank_id": None if money_debit_credit_obj.sender_bank_id is None else money_debit_credit_obj.sender_bank_id.bank_id,
                "money_sender_cheque_no": money_debit_credit_obj.money_sender_cheque_no,
                "receiver_bank_id": None if money_debit_credit_obj.receiver_bank_id is None else money_debit_credit_obj.receiver_bank_id.bank_id,
                "money_payment_details": money_debit_credit_obj.money_payment_details,
                "machine_id": machine_id,
                "project_id": project_id,
            },
            "persons_data": persons_data,
            "pay_types_data": pay_types_data,
            "machines_data": machines_data,
            "bank_data": bank_data,
            "projects_data": projects_data,
        })

    else:
        return Response({
            "status": "False",
            "message": "Invalid request method."
        })


@api_view(['DELETE'])
def delete_money_debit_credit(request):
    money_id = request.GET.get('money_id')

    if not money_id:
        return Response({
            "status": "error",
            "message": "Money Debit Credit ID is required."
        }, status=400)

    try:
        money_debit_credit_data = Money_Debit_Credit.objects.get(money_id=money_id)
        if money_debit_credit_data.money_payment_mode=='BANK':
            if money_debit_credit_data.sender_person_id.person_id == 1:
                bank_instance = Bank_Details.objects.get(bank_id=money_debit_credit_data.sender_bank_id.bank_id)
                bank_instance.bank_current_amount = float(bank_instance.bank_current_amount) + float(money_debit_credit_data.money_amount)
                print(bank_instance.bank_current_amount)
                bank_instance.save()
            
            if money_debit_credit_data.receiver_person_id.person_id == 1:
                bank_instance = Bank_Details.objects.get(bank_id=money_debit_credit_data.receiver_bank_id.bank_id)
                bank_instance.bank_current_amount = float(bank_instance.bank_current_amount) - float(money_debit_credit_data.money_amount)
                print(bank_instance.bank_current_amount)
                bank_instance.save()

        money_debit_credit_data.delete()
        return Response({
            "status": "success",
            "message": "Money Debit Credit record deleted successfully."
        })
    except Machine_Maintenance.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Money Debit Credit record not found."
        }, status=404)


@api_view(['GET'])
def show_salary(request):
    salary_details = Salary.objects.all()
    money_transaction_data = Money_Debit_Credit.objects.filter(pay_type_id__pay_type_name = 'પગાર')
    person_id = request.GET.get('person_id')
    if person_id != 'null' :
        if person_id != '':
            salary_details = salary_details.filter(person_id__person_id = person_id)
            money_transaction_data = money_transaction_data.filter(receiver_person_id__person_id = person_id)

    salary_details = salary_details.values(
        'salary_id',
        'salary_date', 
        'salary_amount',
        'person_id__person_salary',
        'salary_working_days', 
        'salary_details', 
        'person_id__person_name',
        'person_id__person_contact_number'
    )

    money_transaction_data = money_transaction_data.values(
        'money_id',
        'receiver_person_id__person_name',
        'money_date',
        'money_amount',
        'money_payment_mode',
        'money_payment_details',
    ).annotate(total_money_amount_personwise=Sum('money_amount'))

    worktypes = Work_Types.objects.all().values('work_type_id','work_type_name')
    persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name', 'person_contact_number')

    return Response({
        "status": "success",
        "title": "Salary Details",
        "persons_data": persons_data,
        'money_data': money_transaction_data,
        # "total_money_amount": total_money_amount,
        "data": salary_details,
        "worktypes":worktypes,
    })


@api_view(['POST', 'GET'])
def insert_update_salary(request):
    persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name')

    if request.method == 'POST':
        salary_id = request.data.get('salary_id')
        salary_date = request.data.get('salary_date')
        person_id = request.data.get('person_id')
        work_type = request.data.get('work_type')
        salary_amount = request.data.get('salary_amount')
        salary_working_days = request.data.get('salary_working_days')
        person_instance = Person.objects.get(person_id=person_id)
        if work_type=='Fixed_Salary':
            per_salary = int(person_instance.person_salary)
            salary_amount = int(float((per_salary/30)) * float(salary_working_days))
        else:
            salary_amount = int(float(salary_working_days)*float(salary_amount))
        
        salary_details = request.data.get('salary_details')
        

        

        if salary_id:
            salary = Salary.objects.get(salary_id=salary_id)
            salary.salary_date = salary_date
            salary.salary_amount = salary_amount
            salary.salary_working_days = salary_working_days
            salary.salary_details = salary_details
            salary.person_id = person_instance
            salary.save()

            if person_instance.person_khatu:
                person_instance.person_khatu = 0 + float(salary_amount)
                print(person_instance.person_khatu)
            else:
                person_instance.person_khatu = float(person_instance.person_khatu) + float(salary_amount)
                print(person_instance.person_khatu)
            person_instance.save()

            message = "Salary record updated successfully."
            
        else:
            salary = Salary.objects.create(
                salary_date=salary_date,
                salary_amount=salary_amount,
                salary_working_days=salary_working_days,
                salary_details=salary_details,
                person_id=person_instance
            )

            if person_instance.person_khatu:
                
                person_instance.person_khatu = float(person_instance.person_khatu) + float(salary_amount)
                print(person_instance.person_khatu)
            else:
                person_instance.person_khatu = 0 + float(salary_amount)
                print(person_instance.person_khatu)
                
            person_instance.save()

            message = "Salary record created successfully."

        return Response({
            "status": "success",
            "title": "Salary Transaction",
            "message": message,
            "data": {
                "salary_id": salary.salary_id,
                "salary_date": salary.salary_date,
                "salary_amount": salary.salary_amount,
                "salary_working_days": salary.salary_working_days,
                "salary_details": salary.salary_details,
                "person_id": salary.person_id.person_name,
            },
            "persons_data": persons_data
        })

    elif request.GET.get('getdata_id'):
            salary = Salary.objects.get(salary_id=request.GET.get('getdata_id'))
            return Response({
                "status": "success",
                "message": 'Data fetched successfully',
                "data": {
                    "salary_id": salary.salary_id,
                    "salary_date": salary.salary_date,
                    "salary_amount": salary.salary_amount,
                    "salary_working_days": salary.salary_working_days,
                    "salary_details": salary.salary_details,
                    "person_id": salary.person_id.person_id,
                },
                "persons_data": persons_data
            })
    else:
        return Response({
            "status": "False",
            "message": "Invalid request method."
        })

@api_view(['DELETE'])
def delete_salary(request):
    salary_id = request.GET.get('salary_id')
    
    if not salary_id:
        return Response({
            "status": "error",
            "message": "Salary ID is required."
        }, status=400)

    try:
        salary_data = Salary.objects.get(salary_id=salary_id)
        person_instance = Person.objects.get(person_id=salary_data.person_id.person_id)
        person_instance.person_khatu = float(person_instance.person_khatu) - float(salary_data.salary_amount)
        person_instance.save()
        salary_data.delete()
        return Response({
            "status": "success",
            "message": "Salary record deleted successfully."
        })
    except Salary.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Salary record not found."
        }, status=404)


@api_view(['GET'])
def show_machine_maintenance(request):
    machine_maintenance = Machine_Maintenance.objects.all()
    if request.GET.get('machine_id'):
        machine_maintenance = machine_maintenance.filter(machine_machine_id__machine_id = request.GET.get('machine_id'))

    if request.GET.get('project_id'):
        machine_maintenance = machine_maintenance.filter(project_id__project_id = request.GET.get('project_id'))
        total_amount = machine_maintenance.aggregate(total_amount=Sum('machine_maintenance_amount'))['total_amount']
    else:
        total_amount = machine_maintenance.aggregate(total_amount=Sum('machine_maintenance_amount'))['total_amount']



    machine_maintenance = machine_maintenance.values(
        'machine_maintenance_id',
        'machine_machine_id__machine_name',
        'machine_machine_id__machine_number_plate',
        'machine_machine_id__machine_types_id__machine_type_name',
        'machine_maintenance_amount',
        'machine_maintenance_date',
        'machine_maintenance_amount_paid',
        'machine_maintenance_amount_paid_by',
        'machine_maintenance_driver_id__person_name',
        'machine_maintenance_driver_id__person_contact_number',
        'machine_maintenance_person_id__person_name',
        'machine_maintenance_person_id__person_contact_number',
        'machine_maintenance_details',
        'machine_maintenance_types_id__maintenance_type_name',
        'project_id__project_name',
    )
    maintenance_types_data = Maintenance_Types.objects.all().values('maintenance_type_id', 'maintenance_type_name')
    machines_data = Machines.objects.all().values('machine_id', 'machine_name', 'machine_number_plate')
    maintenance_persons_data = Person.objects.exclude(person_status=0).filter(person_type_id__person_type_name = 'maintenance').values('person_id', 'person_name', 'person_contact_number')
    driver_persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name', 'person_contact_number')
    repair_persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name', 'person_contact_number')   
    projects_data = Project.objects.all().values('project_id', 'project_name')

    return Response({
        "status": "success",
        "title": "Maintenance",
        "maintenance_types_data": maintenance_types_data,
        "machines_data": machines_data,
        "persons_data": maintenance_persons_data,
        "driver_persons_data": driver_persons_data,
        "repair_persons_data": repair_persons_data,
        "projects_data": projects_data,
        "data": machine_maintenance,
        "total_amount": total_amount
    })



@api_view(['POST', 'GET'])
def insert_update_machine_maintenance(request):
    if request.method == 'POST':
        machine_maintenance_id = request.data.get('machine_maintenance_id')
        machine_machine_id = request.data.get('machine_machine_id')
        machine_maintenance_amount = request.data.get('machine_maintenance_amount')
        machine_maintenance_date = request.data.get('machine_maintenance_date')
        machine_maintenance_amount_paid = request.data.get('machine_maintenance_amount_paid')
        machine_maintenance_amount_paid_by = request.data.get('machine_maintenance_amount_paid_by')
        machine_maintenance_driver_id = int(request.data.get('machine_maintenance_driver_id')) if request.data.get('machine_maintenance_driver_id') else None
        machine_maintenance_person_id = int(request.data.get('machine_maintenance_person_id')) if request.data.get('machine_maintenance_person_id') else None
        machine_maintenance_details = request.data.get('machine_maintenance_details')
        machine_maintenance_types_id = request.data.get('machine_maintenance_types_id')
        project_id = request.GET.get('project_id')

        maintenance_type_instance = Maintenance_Types.objects.get(maintenance_type_id=machine_maintenance_types_id)
        machine_instance = Machines.objects.get(machine_id = machine_machine_id)
        if machine_maintenance_person_id:
            person_instance = Person.objects.get(person_id = machine_maintenance_person_id)
        else:
            person_instance = None  
        if  machine_maintenance_driver_id:
            driver_instance = Person.objects.get(person_id = machine_maintenance_driver_id)
        else:
            driver_instance = None
        if project_id:
            project_instance = Project.objects.get(project_id=project_id)
        else:
            project_instance = None

    if request.GET.get('getdata_id'):
        maintenance_obj = Machine_Maintenance.objects.get(machine_maintenance_id=request.GET.get('getdata_id'))
        return Response({
            "status": "success",
            "message": 'Data Fetched Successfully',
            "data": {
                "machine_maintenance_id": maintenance_obj.machine_maintenance_id,
                "machine_machine_id": maintenance_obj.machine_machine_id.machine_id,
                "machine_maintenance_amount": maintenance_obj.machine_maintenance_amount,
                "machine_maintenance_date": maintenance_obj.machine_maintenance_date,
                "machine_maintenance_amount_paid": maintenance_obj.machine_maintenance_amount_paid,
                "machine_maintenance_amount_paid_by": maintenance_obj.machine_maintenance_amount_paid_by,
                "machine_maintenance_driver_id": maintenance_obj.machine_maintenance_driver_id.person_id if maintenance_obj.machine_maintenance_driver_id else None,
                "machine_maintenance_person_id": maintenance_obj.machine_maintenance_person_id.person_id if maintenance_obj.machine_maintenance_person_id else None,
                "machine_maintenance_details": maintenance_obj.machine_maintenance_details,
                "machine_maintenance_types_id": maintenance_obj.machine_maintenance_types_id.maintenance_type_id,
                "project_id": maintenance_obj.project_id.project_id if maintenance_obj.project_id else None,
            }
        })

    if request.method == 'POST':
        if machine_maintenance_id:
            machine_maintenance = Machine_Maintenance.objects.get(machine_maintenance_id=machine_maintenance_id)
            machine_maintenance.machine_machine_id = machine_instance
            machine_maintenance.machine_maintenance_amount = machine_maintenance_amount
            machine_maintenance.machine_maintenance_amount_paid = machine_maintenance_amount_paid
            machine_maintenance.machine_maintenance_amount_paid_by = machine_maintenance_amount_paid_by
            machine_maintenance.machine_maintenance_driver_id = driver_instance
            machine_maintenance.machine_maintenance_person_id = person_instance
            machine_maintenance.machine_maintenance_details = machine_maintenance_details
            machine_maintenance.machine_maintenance_types_id = maintenance_type_instance
            machine_maintenance.project_id = project_instance
            machine_maintenance.save()
            message = "Machine maintenance record updated successfully."
        else:
            machine_maintenance = Machine_Maintenance.objects.create(
                machine_machine_id=machine_instance,
                machine_maintenance_amount=machine_maintenance_amount,
                machine_maintenance_date=machine_maintenance_date,
                machine_maintenance_amount_paid=machine_maintenance_amount_paid,
                machine_maintenance_amount_paid_by=machine_maintenance_amount_paid_by,
                machine_maintenance_driver_id = driver_instance,
                machine_maintenance_person_id=person_instance,
                machine_maintenance_details=machine_maintenance_details,
                machine_maintenance_types_id=maintenance_type_instance,
                project_id=project_instance
            )
            message = "Machine maintenance record created successfully."

        return Response({
            "status": "success",
            "title": "Machine Maintenance",
            "message": message,
            "data": {
                "machine_maintenance_id": machine_maintenance.machine_maintenance_id,
                "machine_machine_id": machine_maintenance.machine_machine_id.machine_id,
                "machine_maintenance_amount": machine_maintenance.machine_maintenance_amount,
                "machine_maintenance_date": machine_maintenance.machine_maintenance_date,
                "machine_maintenance_amount_paid": machine_maintenance.machine_maintenance_amount_paid,
                "machine_maintenance_amount_paid_by": machine_maintenance.machine_maintenance_amount_paid_by,
            }
        })
    else:
        return Response({
            "status": "False"
        })


@api_view(['DELETE'])
def delete_machine_maintenance(request):
    machine_maintenance_id = request.GET.get('machine_maintenance_id')

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
def show_projects(request):
    projects = Project.objects.all().values(
        'project_id',
        'project_name',
        'project_start_date',
        'project_end_date',
        'project_amount',
        'project_location',
        'project_owner_name__person_name',
        'project_owner_name__person_contact_number',
        'project_status',
        'project_cgst',
        'project_sgst',
        'project_tax',
        'project_discount',
        'project_types_id__project_type_id',
        'project_types_id__project_type_name',
    )
    project_types_data = Project_Types.objects.all().values('project_type_id', 'project_type_name')
    persons_data = Person.objects.exclude(person_status=0).values('person_name','person_contact_number','person_id')
    agent_persons = Person.objects.exclude(person_status=0).values('person_name','person_contact_number','person_id')

    return Response({
        "status": "success",
        "title": "Project",
        "project_types_data": project_types_data,
        "data": projects,
        "persons_data":persons_data,
        "agent_persons": agent_persons,
    })


@api_view(['POST', 'GET'])
def insert_update_project(request):
    project_types_data = Project_Types.objects.all().values('project_type_id', 'project_type_name')
    if request.method == 'POST':
        project_id = request.data.get('project_id')
        project_name = request.data.get('project_name')
        project_start_date = request.data.get('project_start_date')
        if project_start_date:
            pass
        else:
            project_start_date = None

        project_end_date = request.data.get('project_end_date')
        if project_end_date:
            pass
        else:
           project_end_date = None

        project_amount = request.data.get('project_amount')
        project_location = request.data.get('project_location')
        project_owner = request.data.get('project_owner_name')
        project_owner_instance = Person.objects.get(person_id = project_owner)
        project_status = request.data.get('project_status')
        project_cgst = int(request.data.get('project_cgst')) if request.data.get('project_cgst') else 0
        project_sgst = int(request.data.get('project_sgst')) if request.data.get('project_sgst') else 0
        project_tax = project_cgst + project_sgst
        project_discount = request.data.get('project_discount')
        project_types_id = int(request.data.get('project_types_id'))
        project_type_instance = Project_Types.objects.get(project_type_id=project_types_id)

        project_agent = request.data.get('project_agent')
        project_agent_id = request.data.get('project_agent_id')
        project_agent_type = request.data.get('project_agent_type')
        project_agent_percentage = request.data.get('project_agent_percentage')
        print('=========',project_agent_percentage)
        project_agent_fixed_amount = request.data.get('project_agent_fixed_amount')

        project_investor = request.data.get('project_investor')
        project_investor_id = request.data.get('project_investor_id')
        print(project_investor_id)
        project_investor_percentage = request.data.get('project_investor_percentage')
        project_investor_amount = request.data.get('project_investor_amount') 
        if project_investor_amount:
            pass
        else:
            project_investor_amount = 0
        # if project_agent_type == 'Percentage':
        #     project_final_amount = (((int(project_agent_percentage)/100) * int(project_amount)) + int(project_amount))
        # elif project_agent_type == 'Fixed':
        #     project_final_amount = (int(project_agent_fixed_amount) + int(project_amount))
        # else:
        #     project_final_amount = project_amount
        project_final_amount=0
        if project_agent_id:
            agent_instance = Person.objects.get(person_id = project_agent_id)
        else:
            agent_instance = None

        
        # if project_investor == True:
        #     project_final_amount = (((int(project_investor_percentage)/100) * int(project_final_amount)) + int(project_final_amount))
        # else:
        #     project_final_amount = project_final_amount
 
        if project_investor_id:
            investor_instance = Person.objects.get(person_id = project_investor_id)
        else:
            investor_instance = None
    
    if request.GET.get('getdata_id'):
        project_obj = Project.objects.get(project_id = request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            'project_id': project_obj.project_id,
            'project_name': project_obj.project_name,
            'project_start_date': project_obj.project_start_date,
            'project_end_date': project_obj.project_end_date,
            'project_amount': project_obj.project_amount,
            'project_location': project_obj.project_location,
            'project_owner_name': project_obj.project_owner_name.person_id,
            'project_status': project_obj.project_status,
            'project_cgst': project_obj.project_cgst,
            'project_sgst': project_obj.project_sgst,
            'project_tax': project_obj.project_tax,
            'project_discount': project_obj.project_discount,
            'project_types_id': project_obj.project_types_id.project_type_id,
            'project_agent': project_obj.project_agent,
            'project_agent_id': project_obj.project_agent_id.person_id if project_obj.project_agent else None,
            'project_agent_type': project_obj.project_agent_type,
            "project_agent_percentage": project_obj.project_agent_percentage,
            "project_agent_fixed_amount": project_obj.project_agent_fixed_amount,
            'project_investor': project_obj.project_investor,
            'project_investor_id': project_obj.project_investor_id.person_id if project_obj.project_investor_id else None,
            "project_investor_percentage": project_obj.project_investor_percentage,
            "project_investor_amount": project_obj.project_investor_amount,
        },
        'project_types_data': project_types_data
        })

    if request.method == 'POST':
        if project_id:
            project = Project.objects.get(project_id=project_id)
            project.project_name = project_name
            project.project_start_date = project_start_date
            project.project_end_date = project_end_date
            project.project_amount = project_amount
            project.project_location = project_location
            project.project_owner_name = project_owner_instance
            project.project_status = project_status
            project.project_cgst = project_cgst
            project.project_tax = project_tax
            project.project_sgst = project_sgst
            project.project_discount = project_discount
            project.project_types_id = project_type_instance
            project.project_agent = project_agent
            project.project_agent_id = agent_instance
            project.project_agent_type = project_agent_type
            project.project_agent_percentage = project_agent_percentage
            project.project_agent_fixed_amount = project_agent_fixed_amount
            project.project_investor = project_investor
            project.project_investor_id = investor_instance
            project.project_investor_percentage = project_investor_percentage
            project.project_investor_amount = project_investor_amount
            project.save()
            message = "Project updated successfully."
        else:
            project = Project.objects.create(
                project_name=project_name,
                project_start_date=project_start_date,
                project_end_date=project_end_date,
                project_amount=project_amount,
                project_location=project_location,
                project_owner_name = project_owner_instance,
                project_status=project_status,
                project_cgst=project_cgst,
                project_sgst=project_sgst,
                project_tax=project_tax,
                project_discount=project_discount,
                project_types_id=project_type_instance,
                project_agent = project_agent,
                project_agent_id = agent_instance,
                project_agent_type = project_agent_type,
                project_agent_percentage = project_agent_percentage,
                project_agent_fixed_amount = project_agent_fixed_amount,
                project_investor = project_investor,
                project_investor_id = investor_instance,
                project_investor_percentage = project_investor_percentage,
                project_investor_amount = project_investor_amount,
                project_final_amount = project_final_amount,

            )
            message = "Project created successfully."

        return Response({
            "status": "success",
            "title": "Projects",
            "message": message,
            "data": {
                "project_id": project.project_id,
                "project_name": project.project_name,
                "project_start_date": project.project_start_date,
                "project_end_date": project.project_end_date,
                "project_amount": project.project_amount,
                "project_location": project.project_location,
                'project_owner_id': project.project_owner_name.person_id,
                'project_owner_name': project.project_owner_name.person_name,
                'project_owner_contact': project.project_owner_name.person_contact_number,
                "project_status": project.project_status,
                "project_cgst": project.project_cgst,
                "project_sgst": project.project_sgst,
                "project_tax": project.project_tax,
                "project_discount": project.project_discount,
                "project_types_id": project.project_types_id.project_type_id,
                "project_agent": project.project_agent,
                "project_agent_id": project.project_agent_id.person_id if project.project_agent else None,
                "project_agent_percentage": project.project_agent_percentage,
                "project_investor_amount": project.project_investor_amount,
                "project_final_amount": project.project_final_amount,
            },
            'project_types_data': project_types_data
        })
    else:
        return Response({
            "status": "False"
        })


@api_view(['DELETE'])
def delete_project(request):
    project_id = request.GET.get('project_id')
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
def show_materials(request):
    materials = Material.objects.all().values(
        'material_id',
        'material_type_id__material_type_id',
        'material_type_id__material_type_name',
        'material_owner__person_id',
        'material_owner__person_name',
        'material_buy_date',
        'material_work_type__work_type_id',
        'material_work_type__work_type_name',
        'material_is_agent',
        'material_agent_person__person_name',
        'material_agent_person__person_id',
        'material_agent_person__person_contact_number',
        'material_agent_price_choice',
        'material_agent_percentage',
        'material_details'
    )
    material_types_data = Material_Types.objects.all().values('material_type_id', 'material_type_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    project_types_data = Project.objects.all().values('project_id', 'project_name')
    perons = Person.objects.exclude(person_status=0).values('person_id','person_name','person_contact_number')
    return Response({
        "status": "success",
        "title": "Materials",
        'material_types_data': material_types_data,
        'work_types_data': work_types_data,
        'project_types_data': project_types_data,
        'perons':perons,
        "data": materials
    })

@api_view(['POST', 'GET'])
def insert_update_material(request):
    material_types_data = Material_Types.objects.all().values('material_type_id', 'material_type_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    project_types_data = Project.objects.all().values('project_id', 'project_name')

    if request.method == 'GET' and request.GET.get('getdata_id'):
        material_obj = Material.objects.get(material_id=request.GET.get('getdata_id'))
        return Response({
            "status": "success",
            "message": 'Data Fetched Successfully',
            "data": {
            'material_id': material_obj.material_id,
            'material_type_id': material_obj.material_type_id.material_type_id,
            'material_owner': material_obj.material_owner.person_id,
            'material_buy_date': material_obj.material_buy_date,
            'material_work_type': material_obj.material_work_type.work_type_id,
            'material_work_no': material_obj.material_work_no,
            'material_price': material_obj.material_price,
            'material_total_price': material_obj.material_total_price,
            'material_is_agent': material_obj.material_is_agent,
            'material_agent_person':material_obj.material_agent_person.person_id if material_obj.material_agent_person else None,
            'material_agent_name': material_obj.material_agent_name,
            'material_agent_contact': material_obj.material_agent_contact,
            'material_agent_price_choice': material_obj.material_agent_price_choice,
            'material_agent_percentage': material_obj.material_agent_percentage,
            'material_agent_amount': material_obj.material_agent_amount,
            'material_final_amount': material_obj.material_final_amount,
            'material_details': material_obj.material_details
            },
            'material_types_data': material_types_data,
            'work_types_data': work_types_data,
            'project_types_data': project_types_data
        })

    if request.method == 'POST':
        material_id = request.data.get('material_id')
        material_owner = request.data.get('material_owner')
        material_type_id = request.data.get('material_type_id')
        material_buy_date = request.data.get('material_buy_date')
        material_work_type = request.data.get('material_work_type')
        material_work_no = int(request.data.get('material_work_no') if request.data.get('material_work_no') else 0)
        material_price = int(request.data.get('material_price') if request.data.get('material_price') else 0)
        
        material_is_agent = request.data.get('material_is_agent')
        material_agent_name = request.data.get('material_agent_name')
        material_agent_contact = request.data.get('material_agent_contact')
        material_agent_price_choice = request.data.get('material_agent_price_choice')
        material_agent_percentage = request.data.get('material_agent_percentage')
        print('============',request.data.get('material_agent_person'))
        material_agent_person = Person.objects.get(person_id = request.data.get('material_agent_person')) if request.data.get('material_agent_person') else None
        
        material_type_instance = Material_Types.objects.get(material_type_id=material_type_id)
        work_type_instance = Work_Types.objects.get(work_type_id=material_work_type)
        material_owner_instance = Person.objects.get(person_id=material_owner)
        material_total_price = material_price * material_work_no

    
        material_agent_amount = request.data.get('material_agent_amount',0)
        if material_agent_amount == '':
            material_agent_amount = 0

        if material_is_agent:
            if material_agent_price_choice == "Fixed_Amount":
                material_agent_amount = int(material_agent_amount)
            else:
                material_agent_percentage = int(material_agent_percentage)
                material_agent_amount = material_total_price*material_agent_percentage/100
                

            
        if material_agent_amount:
            material_final_amount = int(material_total_price) + int(material_agent_amount)
        else:
            material_final_amount = material_total_price
        material_details = request.data.get('material_details')

        

        if material_id:
            material = Material.objects.get(material_id=material_id)
            material.material_owner = material_owner_instance
            material.material_buy_date = material_buy_date
            material.material_type_id = material_type_instance
            material.material_work_type = work_type_instance
            material.material_work_no = material_work_no
            material.material_price = material_price
            material.material_total_price = material_total_price
            material.material_is_agent = material_is_agent
            material.material_agent_person = material_agent_person
            material.material_agent_name = material_agent_name
            material.material_agent_contact = material_agent_contact
            material.material_agent_price_choice = material_agent_price_choice
            material.material_agent_percentage = material_agent_percentage
            material.material_agent_amount = material_agent_amount
            material.material_final_amount = material_final_amount
            material.material_details = material_details
            material.save()
            message = "Material updated successfully."
        else:
            material = Material.objects.create(
                material_owner=material_owner_instance,
                material_buy_date=material_buy_date,
                material_type_id=material_type_instance,
                material_work_type=work_type_instance,
                material_work_no=material_work_no,
                material_price=material_price,
                material_total_price=material_total_price,
                material_is_agent=material_is_agent,
                material_agent_person = material_agent_person,
                material_agent_name=material_agent_name,
                material_agent_contact=material_agent_contact,
                material_agent_price_choice=material_agent_price_choice,
                material_agent_percentage=material_agent_percentage,
                material_agent_amount=material_agent_amount,
                material_final_amount=material_final_amount,
                material_details=material_details,
            )
            message = "Material created successfully."

        return Response({
            "status": "success",
            "message": message,
            "data": {
                "material_id": material.material_id,
                "material_owner": material.material_owner.person_id,
                "material_buy_date": material.material_buy_date,
                "material_type_id": material.material_type_id.material_type_id,
                "material_work_type": material.material_work_type.work_type_id,
                "material_work_no": material.material_work_no,
                "material_price": material.material_price,
                "material_total_price": material.material_total_price,
                "material_is_agent": material.material_is_agent,
                "material_agent_name": material.material_agent_name,
                "material_agent_contact": material.material_agent_contact,
                "material_agent_price_choice": material.material_agent_price_choice,
                "material_agent_percentage": material.material_agent_percentage,
                "material_agent_amount": material.material_agent_amount,
                "material_final_amount": material.material_final_amount,
                "material_details": material.material_details
            },
            'material_types_data': material_types_data,
            'work_types_data': work_types_data,
            'project_types_data': project_types_data
        })

    return Response({
        'status': 'false',
        'message': 'Invalid request method.'
    })



@api_view(['DELETE'])
def delete_material(request):
    material_id = request.GET.get('material_id')
    if not material_id:
        return Response({
            "status": "error",
            "message": "Material ID is required."
        }, status=400)

    try:
        material = Material.objects.get(material_id=material_id)
        material.delete()
        return Response({
            "status": "success",
            "message": "Material deleted successfully."
        })
    except Material.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Material not found."
        }, status=404)
    







@api_view(['GET','POST'])
def material_owner_list_create(request):
    if request.method == 'GET':
        material_owners = Material_Owner_data.objects.all().values(
            'Material_Owner_id',
            'material_owner_person_id',
            'Material_Owner_status',
            'Material_Owner_location',
            'Material_Owner_details',
            'material_owner_person_id__person_id',
            'material_owner_person_id__person_name'  # Get related person name
        )
        persons_data = Person.objects.exclude(person_status=0).values('person_id','person_name','person_contact_number')
        return Response({'data':material_owners,'persons_data':persons_data})
    
    if request.method == 'POST':
        try:
            print("Going inside")
            material_owner = Material_Owner_data.objects.create(
                material_owner_person_id=Person.objects.get(person_id=int(request.data.get('person_id'))),
                Material_Owner_status=request.data.get('status', True),
                Material_Owner_location=request.data.get('location'),
                Material_Owner_details=request.data.get('details')
            )
            return Response({'success': True, 'id': material_owner.Material_Owner_id})
        except Exception as e:
            return Response({'success': False, 'error': str(e)}, status=400)

@api_view(['GET','POST','DELETE'])
def material_owner_update_delete(request):
    pk = request.GET.get('pk')
    print(pk)
    if pk:
        print(pk)
        material_owner = Material_Owner_data.objects.get(pk=int(pk))
        print(material_owner)
        print(request.data.get('status'))
        if request.method == 'POST':
            print("going to post")
            print(request.data.get('person_id'))
            print(Person.objects.get(person_id=int(request.data.get('person_id'))).person_address)
            material_owner.material_owner_person_id = Person.objects.get(person_id=int(request.data.get('person_id')))
            if request.data.get('status') == True:
                material_owner.Material_Owner_status = True
            else:
                material_owner.Material_Owner_status = False

            material_owner.Material_Owner_location = request.data.get('location')
            material_owner.Material_Owner_details = request.data.get('details')
            material_owner.save()
            return JsonResponse({'success': True})

        if request.method == 'DELETE':
            material_owner.delete()
            return Response({'success': True})
    else:
        return Response({'success': False}, status=400)
    








@api_view(['GET'])
def single_project_data(request):
    try:
        # Fetch the project object
        project = Project.objects.get(project_id=request.GET.get('project_id'))
        
        # Construct a dictionary with all data, including related fields
        project_data = {
            "project_id": project.project_id,
            "project_name": project.project_name,
            "project_amount": project.project_amount,
            "project_location": project.project_location,
            "project_types_id": project.project_types_id_id,
            "project_type_name": project.project_types_id.project_type_name,
            "project_status": project.project_status,
            "project_start_date": project.project_start_date,
            "project_end_date": project.project_end_date,
            "project_owner_name_id": project.project_owner_name_id,
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
        )['total_amount'] or 0
        day_detail_total_amt = day_detail_total_amt if day_detail_total_amt else 0

        project_material_total_amount = Project_Material_Data.objects.filter(project_id__project_id = project.project_id).aggregate(
            total_amount=Sum('project_material_total_amount')
        )['total_amount'] or 0
        project_material_total_amount = project_material_total_amount if project_material_total_amount else 0

        project_expense_total_amount = Project_Expense.objects.filter(project_id__project_id = project.project_id).aggregate(
            total_amount=Sum('project_expense_amount')
        )['total_amount'] or 0
        project_expense_total_amount = project_expense_total_amount if project_expense_total_amount else 0


        project_machine_total_amount = Project_Machine_Data.objects.filter(project_id__project_id = project.project_id).aggregate(
            total_amount=Sum('project_machine_data_total_amount')
        )['total_amount'] or 0
        project_machine_total_amount = project_machine_total_amount if project_machine_total_amount else 0


        project_machine_maintenance_total_amount = Machine_Maintenance.objects.filter(project_id__project_id = project.project_id).aggregate(
            total_amount=Sum('machine_maintenance_amount')
        )['total_amount'] or 0
        project_machine_maintenance_total_amount = project_machine_maintenance_total_amount if project_machine_maintenance_total_amount else 0

        project_person_total_amount = Project_Person_Data.objects.filter(project_id__project_id = project.project_id).aggregate(
            total_amount=Sum('project_person_total_price')
        )['total_amount'] or 0
        project_person_total_amount = project_person_total_amount if project_person_total_amount else 0


        grahak_paid_amount_for_project = Money_Debit_Credit.objects.filter(project_id__project_id = project.project_id, receiver_person_id__person_id=1).aggregate(
            total_amount=Sum('money_amount')
        )['total_amount'] or 0
        print(grahak_paid_amount_for_project)
        grahak_paid_amount_for_project = grahak_paid_amount_for_project if grahak_paid_amount_for_project else 0


        dalali_amt = 0
        print("day_detail_total_amt",day_detail_total_amt)
        print("project.project_agent_percentage",project.project_agent_percentage)
        if project.project_agent:
            if project.project_agent_type == 'Percentage':
                dalali_amt = (float(project.project_agent_percentage)*int(day_detail_total_amt))/100
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

        return Response({"status": "success", "data": project_data,"title":project.project_name,"project_saransh":project_saransh})
    except Project.DoesNotExist:
        return Response({"status": "error", "message": "Project not found."}, status=404)



@api_view(['GET'])
def show_project_day_details(request):
    project_day_details_data = Project_Day_Details.objects.all()

    if request.GET.get('project_id'):
        project_day_details_data = project_day_details_data.filter(project_id__project_id = request.GET.get('project_id'))

        total_amount = project_day_details_data.aggregate(
            total_amount=Sum('project_day_detail_total_price')
        )['total_amount']

    else:
        total_amount = project_day_details_data.aggregate(
            total_amount=Sum('project_day_detail_total_price')
        )['total_amount']


    project_day_details_data = project_day_details_data.values(
        'project_day_detail_id',
        'proejct_day_detail_date',
        'project_day_detail_machine_id__machine_name',
        'project_day_detail_machine_id__machine_number_plate',
        'project_day_detail_work_type__work_type_name',
        'project_day_detail_total_tyres',
        'project_day_detail_work_no',
        'project_day_detail_price',
        'project_day_detail_total_price',
        'project_day_detail_details'
    )

    machine_data = Machines.objects.all().values('machine_id', 'machine_name', 'machine_number_plate')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')


    short_day_detail_data = []
    for xx in work_types_data:
        pddd = Project_Day_Details.objects.filter(project_id__project_id = request.GET.get('project_id'), project_day_detail_work_type__work_type_id = xx['work_type_id'])
        total_on_10_tyre = 0
        total_on_12_tyre = 0
        total_on_10_tyre_amount = 0
        total_on_12_tyre_amount = 0
        total_on_any_tyre = 0
        total_on_any_tyre_amount = 0


        if pddd:
            xdataa = []
            for y in pddd:
                xdataa.append({'work_type':y.project_day_detail_work_type.work_type_name,'work_no':y.project_day_detail_work_no,'tyre':y.project_day_detail_total_tyres})
                if y.project_day_detail_total_tyres == '10-Tyres':
                    total_on_10_tyre = round(total_on_10_tyre + float(y.project_day_detail_work_no),2)
                    total_on_10_tyre_amount = round(total_on_10_tyre_amount+float(y.project_day_detail_total_price),2)

                if y.project_day_detail_total_tyres == '12-Tyres':
                    total_on_12_tyre = round(total_on_12_tyre + float(y.project_day_detail_work_no),2)
                    total_on_12_tyre_amount = round(total_on_12_tyre_amount+float(y.project_day_detail_total_price),2)
                
                if y.project_day_detail_total_tyres == 'અન્ય':
                    total_on_any_tyre = round(total_on_any_tyre + float(y.project_day_detail_work_no),2)
                    total_on_any_tyre_amount = round(total_on_any_tyre_amount+float(y.project_day_detail_total_price),2) 

            short_day_detail_data.append({'data':xdataa,'tyre_10_total':total_on_10_tyre,'tyre_12_total':total_on_12_tyre,'work_type_id':xx['work_type_id'],'work_type_name':xx['work_type_name'],'tyre_10_total_amount':total_on_10_tyre_amount,'tyre_12_total_amount':total_on_12_tyre_amount,'total_on_any_tyre':total_on_any_tyre,'tyre_any_total_amount':total_on_any_tyre_amount})

    print(short_day_detail_data)

    return Response({
        'status': 'success',
        'title': 'Project Day Details',
        'machines_data': machine_data,
        'work_types_data': work_types_data,
        'data': project_day_details_data,
        'total_amount': total_amount,
        'short_day_detail_data':short_day_detail_data,
    })


@api_view(['POST', 'GET'])
def insert_update_project_day_detail(request):
    machines_data = Machines.objects.all().values('machine_id', 'machine_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')

    if request.method == 'GET':
        project_day_detail_id = request.GET.get('getdata_id')
        if project_day_detail_id:
            project_day_detail = get_object_or_404(Project_Day_Details, project_day_detail_id=project_day_detail_id)
            return Response({
                "status": "success",
                "message": "Project day detail fetched successfully",
                "data": {
                    "project_day_detail_id": project_day_detail.project_day_detail_id,
                    "proejct_day_detail_date": project_day_detail.proejct_day_detail_date,
                    "project_day_detail_machine_id": project_day_detail.project_day_detail_machine_id.machine_id if project_day_detail.project_day_detail_machine_id else None,
                    "project_day_detail_work_type": project_day_detail.project_day_detail_work_type.work_type_id,
                    "project_day_detail_work_no": project_day_detail.project_day_detail_work_no,
                    "project_day_detail_total_tyres": project_day_detail.project_day_detail_total_tyres,
                    "project_day_detail_price": project_day_detail.project_day_detail_price,
                    "project_day_detail_total_price": project_day_detail.project_day_detail_total_price,
                    "project_day_detail_details": project_day_detail.project_day_detail_details,
                },
                'machines_data': machines_data,
                'work_types_data': work_types_data,
            })
        return Response({
            "status": "error",
            "message": "Project day detail ID not provided"
        }, status=400)


    if request.GET.get('proj_id'):
        proj_id = request.GET.get('proj_id')
    else:
        None
    if request.method == 'POST':
        project_day_detail_id = request.data.get('project_day_detail_id')
        proejct_day_detail_date = request.data.get('proejct_day_detail_date')
        project_day_detail_machine_id = request.data.get('project_day_detail_machine_id')
        print(project_day_detail_machine_id)
        project_day_detail_work_type = request.data.get('project_day_detail_work_type')
        project_day_detail_work_no = float(request.data.get('project_day_detail_work_no'))
        project_day_detail_total_tyres = request.data.get('project_day_detail_total_tyres')
        project_day_detail_price = float(request.data.get('project_day_detail_price'))
        project_day_detail_details = request.data.get('project_day_detail_details', '')
        project_id = proj_id
        print('working==================================================')
        if project_day_detail_machine_id:
            machine_instance = get_object_or_404(Machines, pk=project_day_detail_machine_id)
            print(machine_instance)
        else: 
            machine_instance = None

        work_type_instance = get_object_or_404(Work_Types, pk=project_day_detail_work_type)
        if work_type_instance.work_type_name == 'કલાક':
            totalprice = round((int(project_day_detail_work_no)*project_day_detail_price)+(((project_day_detail_work_no - int(project_day_detail_work_no))/0.60)*project_day_detail_price))
        else:
            totalprice = project_day_detail_price*project_day_detail_work_no
        print(project_id)
        project_instance = get_object_or_404(Project, pk=project_id)

        
        if project_day_detail_id:
            project_day_detail = get_object_or_404(Project_Day_Details, project_day_detail_id=project_day_detail_id)
            project_day_detail.proejct_day_detail_date = proejct_day_detail_date
            project_day_detail.project_day_detail_machine_id = machine_instance
            project_day_detail.project_day_detail_work_type = work_type_instance
            project_day_detail.project_day_detail_work_no = project_day_detail_work_no
            project_day_detail.project_day_detail_price = project_day_detail_price
            project_day_detail.project_day_detail_total_price = totalprice
            project_day_detail.project_day_detail_details = project_day_detail_details
            project_day_detail.project_day_detail_total_tyres = project_day_detail_total_tyres
            project_day_detail.project_id = project_instance

            project_day_detail.save()
            message = "Project day detail updated successfully"
        else:
            project_day_detail = Project_Day_Details.objects.create(
                proejct_day_detail_date=proejct_day_detail_date,
                project_day_detail_machine_id=machine_instance,
                project_day_detail_work_type=work_type_instance,
                project_day_detail_work_no=project_day_detail_work_no,
                project_day_detail_price=project_day_detail_price,
                project_day_detail_total_price=totalprice,
                project_day_detail_details=project_day_detail_details,
                project_day_detail_total_tyres=project_day_detail_total_tyres,
                project_id = project_instance
            )
            message = "Project day detail created successfully"

        project_day_details_data = Project_Day_Details.objects.filter(project_id__project_id = project_id)
        total_day_detail_amount = int(project_day_details_data.aggregate(
            total_amount=Sum('project_day_detail_total_price')
        )['total_amount'])
        discount = int(project_instance.project_discount) if project_instance.project_discount else 0
        grahak_amount = total_day_detail_amount-discount
        project_instance.project_grahak_amount = grahak_amount
        project_instance.save()

        return Response({
            "status": "success",
            "message": message,
            'machines_data': machines_data,
            'work_types_data': work_types_data,
        })

    return Response({
        "status": "error",
        "message": "Invalid request method"
    }, status=405)


@api_view(['DELETE'])
def delete_project_day_detail(request):
    project_day_detail_id = request.GET.get('project_day_detail_id')

    if not project_day_detail_id:
        return Response({
            "status": "error",
            "message": "Project day detail ID is required."
        }, status=400)

    try:
        project_day_detail = get_object_or_404(Project_Day_Details, project_day_detail_id=project_day_detail_id)
        project_day_detail.delete()

        return Response({
            "status": "success",
            "message": f"Project day detail with ID {project_day_detail_id} deleted successfully."
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }, status=500)


@api_view(['GET'])
def show_project_material(request):
    project_material_data = Project_Material_Data.objects.all()
    if request.GET.get('project_id'):
        project_material_data = project_material_data.filter(project_id__project_id = request.GET.get('project_id'))

        total_amount = project_material_data.aggregate(
            total_amount=Sum('project_material_total_amount')
        )['total_amount']
    else:
        total_amount = project_material_data.aggregate(
            total_amount=Sum('project_material_total_amount')
        )['total_amount']

    project_material_data = project_material_data.values(
        'project_material_id',
        'project_material_date',
        'project_material_material_id__material_owner_person_id__person_id',
        'project_material_material_id__material_owner_person_id__person_name',
        'project_material_material_type_id__material_type_name',
        'project_material_work_type_id__work_type_name',
        'project_material_work_no',
        'project_material_price',
        'project_material_total_amount',
        'person_material_information'
    )

    materials_data = Material_Owner_data.objects.all().values('Material_Owner_id', 'material_owner_person_id__person_name')
    material_types_data = Material_Types.objects.all().values('material_type_id', 'material_type_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name')

    return Response({
        'status': 'success',
        'title': 'Project Material Details',
        'materials_data': materials_data,
        'material_types_data': material_types_data,
        'work_types_data': work_types_data,
        'persons_data': persons_data,
        "total_amount": total_amount,
        'data': project_material_data
    })


@api_view(['POST', 'GET'])
def insert_update_project_material(request):
    materials_data = Material_Owner_data.objects.all().values('Material_Owner_id', 'material_owner_person_id__person_name')
    material_types_data = Material_Types.objects.all().values('material_type_id', 'material_type_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name')
    
    if request.method == 'GET':
        project_material_id = request.GET.get('getdata_id')
        if project_material_id:
            project_material = get_object_or_404(Project_Material_Data, project_material_id=project_material_id)
            return Response({
                "status": "success",
                "message": "Project material data fetched successfully",
                "data": {
                    "project_material_id": project_material.project_material_id,
                    "project_material_date": project_material.project_material_date,
                    "project_material_material_id": project_material.project_material_material_id.Material_Owner_id,
                    "project_material_material_type_id": project_material.project_material_material_type_id.material_type_id,
                    "project_material_work_type_id": project_material.project_material_work_type_id.work_type_id,
                    "project_material_work_no": project_material.project_material_work_no,
                    "project_material_price": project_material.project_material_price,
                    "project_material_total_amount": project_material.project_material_total_amount,
                    "person_material_information": project_material.person_material_information,
                },
                'materials_data': materials_data,
                'material_types_data': material_types_data,
                'work_types_data': work_types_data,
                'persons_data': persons_data,
            })
        return Response({
            "status": "error",
            "message": "Project material ID not provided"
        }, status=400)



    if request.GET.get('proj_id'):
        proj_id = request.GET.get('proj_id')
    else:
        None
    if request.method == 'POST':
        
        
        project_material_id = request.data.get('project_material_id')
        project_material_date = request.data.get('project_material_date')
        project_material_material_id = request.data.get('project_material_material_id')
        project_material_material_type_id = request.data.get('project_material_material_type_id')
        project_material_work_type_id = request.data.get('project_material_work_type_id')
        project_material_work_no = int(request.data.get('project_material_work_no'))
        project_material_price = int(request.data.get('project_material_price'))
        project_material_total_amount = project_material_work_no*project_material_price
        person_material_information = request.data.get('person_material_information')
        project_id = proj_id
        material_instance = get_object_or_404(Material_Owner_data, pk=project_material_material_id)

        material_type_instance = get_object_or_404(Material_Types, pk=project_material_material_type_id)
        work_type_instance = get_object_or_404(Work_Types, pk=project_material_work_type_id)
        
        project_instance = get_object_or_404(Project, pk=project_id)
        
        if project_material_id:
            project_material = get_object_or_404(Project_Material_Data, project_material_id=project_material_id)
            project_material.project_material_date = project_material_date
            project_material.project_material_material_id = material_instance
            project_material.project_material_material_type_id = material_type_instance
            project_material.project_material_work_type_id = work_type_instance
            project_material.project_material_work_no = project_material_work_no
            project_material.project_material_price = project_material_price
            project_material.project_material_total_amount = project_material_total_amount
            project_material.person_material_information = person_material_information
            project_material.project_id = project_instance
            project_material.save()
            message = "Project material data updated successfully"
        else:
            project_material = Project_Material_Data.objects.create(
                project_material_date=project_material_date,
                project_material_material_id=material_instance,
                project_material_material_type_id=material_type_instance,
                project_material_work_type_id=work_type_instance,
                project_material_work_no=project_material_work_no,
                project_material_price=project_material_price,
                project_material_total_amount=project_material_total_amount,
                person_material_information=person_material_information,
                project_id = project_instance,
            )
            material_instance.save()
            message = "Project material data created successfully"

        return Response({
            "status": "success",
            "message": message,
           
            'materials_data': materials_data,
            'material_types_data': material_types_data,
            'work_types_data': work_types_data,
            'persons_data': persons_data,
        })

    return Response({
        "status": "error",
        "message": "Invalid request method"
    }, status=405)


@api_view(['DELETE'])
def delete_project_material(request):
    project_material_id = request.GET.get('project_material_id')

    if not project_material_id:
        return Response({
            "status": "error",
            "message": "Project Material ID is required."
        }, status=400)

    try:
        project_material_data = get_object_or_404(Project_Material_Data, project_material_id=project_material_id)
        project_material_data.delete()

        return Response({
            "status": "success",
            "message": f"Project Material deleted successfully."
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }, status=500)


@api_view(['GET'])
def show_project_machine(request):
    project_machines_data = Project_Machine_Data.objects.all()
    machine_maintenance_data = Machine_Maintenance.objects.all()
    if request.GET.get('machine_id'):
        project_machines_data = project_machines_data.filter(machine_project_id__machine_id = request.GET.get('machine_id'))

    if request.GET.get('project_id'):
        project_machines_data = project_machines_data.filter(project_id__project_id = request.GET.get('project_id'))
        machine_maintenance_data = machine_maintenance_data.filter(project_id__project_id = request.GET.get('project_id'))
        
        total_amount = project_machines_data.aggregate(
            total_amount=Sum('project_machine_data_total_amount')
        )['total_amount']

        maintenance_total_amount = machine_maintenance_data.aggregate(
            total_amount=Sum('machine_maintenance_amount')
        )['total_amount']

    else:
        total_amount = project_machines_data.aggregate(
            total_amount=Sum('project_machine_data_total_amount')
        )['total_amount']

        maintenance_total_amount = machine_maintenance_data.aggregate(
            total_amount=Sum('machine_maintenance_amount')
        )['total_amount']


    project_machines_data = project_machines_data.values(
        'project_machine_data_id',
        'project_machine_date',
        'machine_project_id__machine_name',
        'machine_project_id__machine_number_plate',
        'work_type_id__work_type_name',
        'project_machine_data_work_number',
        'project_machine_data_work_price',
        'project_machine_data_total_amount',
        'project_machine_data_work_details',
        'project_machine_data_more_details',
        'project_machine_data_km',
    )

    machine_maintenance_data = machine_maintenance_data.values(
        'machine_maintenance_id',
        'machine_machine_id__machine_name',
        'machine_machine_id__machine_number_plate',
        'machine_machine_id__machine_types_id__machine_type_name',
        'machine_maintenance_amount',
        'machine_maintenance_date',
        'machine_maintenance_amount_paid',
        'machine_maintenance_amount_paid_by',
        'machine_maintenance_driver_id__person_name',
        'machine_maintenance_person_id__person_name',
        'machine_maintenance_details',
        'machine_maintenance_types_id__maintenance_type_name',
        'project_id__project_name',
    )

    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')

    maintenance_types_data = Maintenance_Types.objects.all().values('maintenance_type_id', 'maintenance_type_name')
    machines_data = Machines.objects.all().values('machine_id', 'machine_name', 'machine_number_plate')
    maintenance_persons_data = Person.objects.filter(person_type_id__person_type_name = 'maintenance').values('person_id', 'person_name')
 
    driver_persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name')
    repair_persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name')
    projects_data = Project.objects.all().values('project_id', 'project_name')

    return Response({
        'status': 'success',
        'title': 'Project Machine',
        'work_types_data': work_types_data,
        "maintenance_types_data": maintenance_types_data,
        "machines_data": machines_data,
        "persons_data": maintenance_persons_data,
        "driver_persons_data": driver_persons_data,
        "repair_persons_data": repair_persons_data,
        "projects_data": projects_data,
        'data': project_machines_data,
        'total_amount': total_amount,
        'machine_maintenance_data': machine_maintenance_data,
        'maintenance_total_amount': maintenance_total_amount
    })


@api_view(['POST', 'GET'])
def insert_update_project_machine(request):
    machines_data = Machines.objects.all().values('machine_id', 'machine_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    if request.method == 'GET':
        project_machine_id = request.GET.get('getdata_id')
        if project_machine_id:
            project_machine = get_object_or_404(Project_Machine_Data, project_machine_data_id=project_machine_id)
            return Response({
                "status": "success",
                "message": "Project machine data fetched successfully",
                "data": {
                    "project_machine_data_id": project_machine.project_machine_data_id,
                    "project_machine_date": project_machine.project_machine_date,
                    "machine_project_id": project_machine.machine_project_id.machine_id,
                    "work_type_id": project_machine.work_type_id.work_type_id,
                    "project_machine_data_work_number": project_machine.project_machine_data_work_number,
                    "project_machine_data_work_price": project_machine.project_machine_data_work_price,
                    "project_machine_data_total_amount": project_machine.project_machine_data_total_amount,
                    "project_machine_data_work_details": project_machine.project_machine_data_work_details,
                    "project_machine_data_more_details": project_machine.project_machine_data_more_details,
                    "project_machine_data_km":project_machine.project_machine_data_km,
                },
                'machines_data': machines_data,
                'work_types_data': work_types_data,
            })
        return Response({
            "status": "error",
            "message": "Project machine ID not provided"
        }, status=400)

    if request.GET.get('proj_id'):
        proj_id = request.GET.get('proj_id')
    else:
        None
    if request.method == 'POST':
        project_machine_id = request.data.get('project_machine_data_id')
        project_machine_date = request.data.get('project_machine_date')
        machine_project_id = request.data.get('machine_project_id')
        work_type_id = request.data.get('work_type_id')
        project_machine_data_work_number = float(request.data.get('project_machine_data_work_number'))
        project_machine_data_km = float(request.data.get('project_machine_data_km')) or 0
        project_machine_data_work_price = int(request.data.get('project_machine_data_work_price'))
        
        project_machine_data_work_details = request.data.get('project_machine_data_work_details')
        project_machine_data_more_details = request.data.get('project_machine_data_more_details')
        project_id = proj_id
        print("-----", project_id)

        machine_instance = get_object_or_404(Machines, pk=machine_project_id)
        work_type_instance = get_object_or_404(Work_Types, pk=work_type_id)
        if work_type_instance.work_type_name == 'કલાક':
            project_machine_data_total_amount = round((int(project_machine_data_work_number)*project_machine_data_work_price)+(((project_machine_data_work_number - int(project_machine_data_work_number))/0.60)*project_machine_data_work_price))
        else:
            project_machine_data_total_amount = project_machine_data_work_price*project_machine_data_work_number
        project_instance = get_object_or_404(Project, pk=project_id)

        if project_machine_id:
            project_machine = get_object_or_404(Project_Machine_Data, pk=project_machine_id)
            project_machine.project_machine_date = project_machine_date
            project_machine.machine_project_id = machine_instance
            project_machine.work_type_id = work_type_instance
            project_machine.project_machine_data_work_number = project_machine_data_work_number
            project_machine.project_machine_data_work_price = project_machine_data_work_price
            project_machine.project_machine_data_total_amount = project_machine_data_total_amount
            project_machine.project_machine_data_work_details = project_machine_data_work_details
            project_machine.project_machine_data_more_details = project_machine_data_more_details
            project_machine.project_machine_data_km = project_machine_data_km
            project_machine.project_id = project_instance
            project_machine.save()
            message = "Project machine data updated successfully"
        else:
            project_machine = Project_Machine_Data.objects.create(
                project_machine_date=project_machine_date,
                machine_project_id=machine_instance,
                work_type_id=work_type_instance,
                project_machine_data_work_number=project_machine_data_work_number,
                project_machine_data_work_price=project_machine_data_work_price,
                project_machine_data_total_amount=project_machine_data_total_amount,
                project_machine_data_work_details=project_machine_data_work_details,
                project_machine_data_more_details=project_machine_data_more_details,
                project_machine_data_km = project_machine_data_km,
                project_id = project_instance
            )
            message = "Project machine data created successfully"

        return Response({
            "status": "success",
            "message": message,
            'machines_data': machines_data,
            'work_types_data': work_types_data,
        })

    return Response({
        "status": "error",
        "message": "Invalid request method"
    }, status=405)


@api_view(['DELETE'])
def delete_project_machine(request):
    project_machine_data_id = request.GET.get('project_machine_data_id')

    if not project_machine_data_id:
        return Response({
            "status": "error",
            "message": "Project Machine ID is required."
        }, status=400)

    try:
        project_machine_data = get_object_or_404(Project_Machine_Data, project_machine_data_id=project_machine_data_id)
        project_machine_data.delete()

        return Response({
            "status": "success",
            "message": f"Project Machine deleted successfully."
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }, status=500)


@api_view(['GET'])
def show_project_person(request):
    project_person_data = Project_Person_Data.objects.all()
    bankData = Bank_Details.objects.filter(person_id__person_id = 1).values('bank_id','bank_name','bank_account_number')
    if request.GET.get('person_id'):
        project_person_data = project_person_data.filter(person_id__person_id = request.GET.get('person_id'))

    if request.GET.get('project_id'):

        project_person_data = project_person_data.filter(project_id__project_id = request.GET.get('project_id'))

        # for showcasing projectdata in reports
        project = get_object_or_404(Project, project_id=request.GET.get('project_id'))
        project_data = {
        'project_name': project.project_name,
        'project_amount': project.project_amount,
        'project_location': project.project_location,
        'project_type': project.project_types_id.project_type_name,
        'project_status': project.project_status,
        'project_start_date': project.project_start_date,
        'project_end_date': project.project_end_date,
        'owner_name': project.project_owner_name.person_name,
        'owner_contact_number': project.project_owner_name.person_contact_number,
        'project_discount':project.project_discount,
        }


        total_amount = project_person_data.aggregate(total_amount=Sum('project_person_total_price'))['total_amount']
    else:
        project_data = None
        total_amount = project_person_data.aggregate(total_amount=Sum('project_person_total_price'))['total_amount']

    project_person_data = project_person_data.values(
        'project_person_id',
        'person_id__person_name',
        'person_id__person_contact_number',
        'project_person_date',
        'work_type_id__work_type_name',
        'project_machine_data_id__machine_name',
        'project_machine_data_id__machine_number_plate',
        'project_person_work_num',
        'project_person_price',
        'project_person_total_price',
        'project_person_paid_by',
        'project_person_payment_details',
        'project_person_more_details',
        'bank_id__bank_name',
        'bank_id__bank_id',
        'person_payment_mode',
    )

    persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name', 'person_contact_number')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    project_machine_data = Machines.objects.all().values('machine_id', 'machine_name', 'machine_number_plate')

    return Response({
        'status': 'success',
        'title': 'Project Person',
        'persons_data': persons_data,
        'work_types_data': work_types_data,
        'project_machine_data': project_machine_data,
        'data': project_person_data,
        'total_amount': total_amount,
        'project_data':project_data,
        'bankData':bankData,
    })



@api_view(['POST', 'GET'])
def insert_update_project_person(request):
    persons_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    project_machine_data = Machines.objects.all().values('machine_id', 'machine_name')

    if request.method == 'GET':
        project_person_id = request.GET.get('getdata_id')
        if project_person_id:
            project_person = get_object_or_404(Project_Person_Data, pk=project_person_id)
            return Response({
                "status": "success",
                "message": "Project person data fetched successfully",
                "data": {
                    "project_person_id": project_person.project_person_id,
                    "person_id": project_person.person_id.person_id if project_person.person_id else None,
                    "project_person_date": project_person.project_person_date,
                    "work_type_id": project_person.work_type_id.work_type_id,
                    "project_machine_data_id": project_person.project_machine_data_id.machine_id if project_person.project_machine_data_id else None,
                    "project_person_work_num": project_person.project_person_work_num,
                    "project_person_price": project_person.project_person_price,
                    "project_person_total_price": project_person.project_person_total_price,
                    "project_person_paid_by": project_person.project_person_paid_by,
                    "project_person_payment_details": project_person.project_person_payment_details,
                    "project_person_more_details": project_person.project_person_more_details,
                    "bank_id":project_person.bank_id,
                    "person_payment_mode":project_person.person_payment_mode,
                },
                'persons_data': persons_data,
                'work_types_data': work_types_data,
                'project_machine_data': project_machine_data,
            })
        return Response({
            "status": "error",
            "message": "Project person ID not provided"
        }, status=400)


    if request.GET.get('proj_id'):
        proj_id = request.GET.get('proj_id')
    else:
        None
    if request.method == 'POST':
        project_person_id = request.data.get('project_person_id')
        person_id = request.data.get('person_id')
        project_person_date = request.data.get('project_person_date')
        work_type_id = request.data.get('work_type_id')
        project_machine_data_id = request.data.get('project_machine_data_id')
        if project_machine_data_id:
            machine_instance = get_object_or_404(Machines, pk=project_machine_data_id)
        else:
            machine_instance = None
        project_person_work_num = int(request.data.get('project_person_work_num'))
        project_person_price = int(request.data.get('project_person_price'))
        project_person_total_price = project_person_work_num * project_person_price
        project_person_paid_by = request.data.get('project_person_paid_by')
        project_person_payment_details = request.data.get('project_person_payment_details')
        project_person_more_details = request.data.get('project_person_more_details')
        project_id = proj_id

        bank_instance = Bank_Details.objects.get(bank_id = request.data.get('bank_id')) if request.data.get('bank_id') else None
        person_payment_mode = request.data.get('person_payment_mode')
        person_instance = get_object_or_404(Person, pk=person_id) if person_id else None
        work_type_instance = get_object_or_404(Work_Types, pk=work_type_id)
        
        project_instance = get_object_or_404(Project, pk=project_id)

        if project_person_id:
            project_person = get_object_or_404(Project_Person_Data, pk=project_person_id)
            project_person.person_id = person_instance
            project_person.project_person_date = project_person_date
            project_person.work_type_id = work_type_instance
            project_person.project_machine_data_id = machine_instance
            project_person.project_person_work_num = project_person_work_num
            project_person.project_person_price = project_person_price
            project_person.project_person_total_price = project_person_total_price
            project_person.project_person_paid_by = project_person_paid_by
            project_person.project_person_payment_details = project_person_payment_details
            project_person.project_person_more_details = project_person_more_details
            project_person.project_id = project_instance
            project_person.bank_id = bank_instance
            project_person.person_payment_mode = person_payment_mode

            project_person.save()
            message = "Project person data updated successfully"
        else:
            project_person = Project_Person_Data.objects.create(
                person_id=person_instance,
                project_person_date=project_person_date,
                work_type_id=work_type_instance,
                project_machine_data_id=machine_instance,
                project_person_work_num=project_person_work_num,
                project_person_price=project_person_price,
                project_person_total_price=project_person_total_price,
                project_person_paid_by=project_person_paid_by,
                project_person_payment_details=project_person_payment_details,
                project_person_more_details=project_person_more_details,
                project_id = project_instance,
                bank_id = bank_instance,
                person_payment_mode = person_payment_mode
            )
            message = "Project person data created successfully"

        return Response({
            "status": "success",
            "message": message,
            'persons_data': persons_data,
            'work_types_data': work_types_data,
            'project_machine_data': project_machine_data,
        })

    return Response({
        "status": "error",
        "message": "Invalid request method"
    }, status=405)



@api_view(['DELETE'])
def delete_project_person(request):
    project_person_id = request.GET.get('project_person_id')
    
    if not project_person_id:
        return Response({
            "status": "error",
            "message": "Project person ID is required"
        }, status=400)

    try:
        project_person = get_object_or_404(Project_Person_Data, project_person_id=project_person_id)
        project_person.delete()
        return Response({
            "status": "success",
            "message": "Project person deleted successfully"
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Failed to delete project person: {str(e)}"
        }, status=500)



@api_view(['GET'])
def show_reports(request):
    project_data = Project.objects.all().values(
        'project_id',
        'project_name',
        'project_discount'
    )

    return Response({
        'status': 'success',
        'title': 'Reports',
        'data': project_data
    })



@api_view(['GET'])
def show_project_expense(request):
    project_expense_data = Project_Expense.objects.all()
    if request.GET.get('project_id'):
        project_expense_data = project_expense_data.filter(project_id__project_id = request.GET.get('project_id'))

        total_amount = project_expense_data.aggregate(
            total_amount=Sum('project_expense_amount')
        )['total_amount']
    else:
        total_amount = project_expense_data.aggregate(
            total_amount=Sum('project_expense_amount')
        )['total_amount']

    project_expense_data = project_expense_data.values(
        'project_expense_id',
        'project_expense_name',
        'project_id__project_name',
        'project_expense_date',
        'project_expense_amount',
        'project_payment_mode',
        'bank_id__bank_name',
        'project_expense_desc',
    )

    projects_data = Project.objects.all().values('project_id', 'project_name')
    banks_data = Bank_Details.objects.filter(bank_open_closed=True).values('bank_id', 'bank_name')


    return Response({
        'status': 'success',
        'title': 'Project Expense',
        'projects_data': projects_data,
        'banks_data': banks_data,
        'total_amount': total_amount,
        'data': project_expense_data,
    })


@api_view(['POST', 'GET'])
def insert_update_project_expense(request):

    if request.method == 'GET':
        project_expense_id = request.GET.get('getdata_id')
        if project_expense_id:
            project_expense = get_object_or_404(Project_Expense, pk=project_expense_id)
            return Response({
                "status": "success",
                "message": "Project expense data fetched successfully",
                "data": {
                    "project_expense_id": project_expense.project_expense_id,
                    "project_expense_name": project_expense.project_expense_name,
                    "project_id": project_expense.project_id.project_id,
                    "project_expense_date": project_expense.project_expense_date,
                    "project_expense_amount": project_expense.project_expense_amount,
                    "project_payment_mode": project_expense.project_payment_mode,
                    "bank_id": project_expense.bank_id.bank_id if project_expense.bank_id else None,
                    "project_expense_desc": project_expense.project_expense_desc,
                }
            })
        return Response({
            "status": "error",
            "message": "Project expense ID not provided"
        }, status=400)

    if request.GET.get('proj_id'):
        proj_id = request.GET.get('proj_id')
    else:
        None
    if request.method == 'POST':
        project_expense_id = request.data.get('project_expense_id')
        project_expense_name = request.data.get('project_expense_name')
        project_id = proj_id
        project_expense_date = request.data.get('project_expense_date')
        project_expense_amount = float(request.data.get('project_expense_amount'))   
        project_payment_mode = request.data.get('project_payment_mode')
        bank_id = request.data.get('bank_id')
        project_expense_desc = request.data.get('project_expense_desc')

        project_instance = get_object_or_404(Project, pk=project_id)
        if bank_id:
            bank_instance = get_object_or_404(Bank_Details, pk=bank_id)
        else:
            bank_instance = None

        if project_expense_id:
            project_expense = get_object_or_404(Project_Expense, pk=project_expense_id)
            project_expense.project_expense_name = project_expense_name
            project_expense.project_id = project_instance
            project_expense.project_expense_date = project_expense_date
            project_expense.project_expense_amount = project_expense_amount
            project_expense.project_payment_mode = project_payment_mode
            project_expense.bank_id = bank_instance
            project_expense.project_expense_desc = project_expense_desc

            project_expense.save()
            message = "Project expense data updated successfully"
        else:
            project_expense = Project_Expense.objects.create(
                project_expense_name=project_expense_name,
                project_id=project_instance,
                project_expense_date=project_expense_date,
                project_expense_amount=project_expense_amount,
                project_payment_mode=project_payment_mode,
                bank_id=bank_instance,
                project_expense_desc=project_expense_desc
            )
            
            message = "Project expense data created successfully"

        return Response({
            "status": "success",
            "message": message,
           
        })

    return Response({
        "status": "error",
        "message": "Invalid request method"
    }, status=405)


@api_view(['GET'])
def delete_project_expense(request):
    project_expense_id = request.GET.get('project_expense_id')
    if not project_expense_id:
        return Response({
            "status": "error",
            "message": "Project Expense ID is required."
        }, status=400)

    try:
        project_expense = get_object_or_404(Project_Expense, project_expense_id=project_expense_id)
        print(project_expense)
        project_expense.delete()

        return Response({
            "status": "success",
            "message": f"Project Expense deleted successfully."
        })

    except Exception as e:
        return Response({
            "status": "error",
            "message": f"An unexpected error occurred: {str(e)}"
        }, status=500)



from rest_framework.response import Response
from rest_framework import status

# GET all documents, POST a new document
@api_view(['GET', 'POST'])
def show_documents(request):
    domain = request.get_host()
    data = Documents.objects.all().values('document_name','document_id','document_date','document_unique_code','document_file', 'person_id__person_name', 'machine_id__machine_name', 'project_id__project_name')
    for document in data:
        document['document_file_url'] = domain + settings.MEDIA_URL + str(document['document_file'])
        document['data'] = 'hello'

    document_types = Document_Types.objects.all().values('document_type_name','document_type_id')
    person_data = Person.objects.exclude(person_status=0).values('person_id', 'person_name')
    machine_data = Machines.objects.all().values('machine_id', 'machine_name')
    project_data = Project.objects.all().values('project_id', 'project_name')


    return Response({
        'status':True,
        'message': 'Documents Fetched Successfully',
        'data':data,
        'document_types':document_types,
        'person_data': person_data,
        'machine_data': machine_data,
        'project_data': project_data

    })

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def insert_update_documents(request, document_id=None):
    if request.method == 'GET':
        # Fetch all documents
        documents = Documents.objects.all()
        serializer = DocumentsSerializer(documents, many=True)
        return Response({
            'status': True,
            'message': 'Documents fetched successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        # Insert a new document
        form = DocumentsSerializer(data=request.data)
        if form.is_valid():
            form.save()
            return Response({
                'status': True,
                'message': 'Document has been added successfully'
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': False,
                'message': form.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT' and document_id:
        # Update an existing document
        try:
            document = Documents.objects.get(document_id=document_id)
        except Documents.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Document not found'
            }, status=status.HTTP_404_NOT_FOUND)

        form = DocumentsSerializer(instance=document, data=request.data, partial=True)
        if form.is_valid():
            form.save()
            return Response({
                'status': True,
                'message': 'Document updated successfully'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': False,
                'message': form.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE' and document_id:
        # Delete a document
        try:
            document = Documents.objects.get(document_id=document_id)
        except Documents.DoesNotExist:
            return Response({
                'status': False,
                'message': 'Document not found'
            }, status=status.HTTP_404_NOT_FOUND)

        document.delete()
        return Response({
            'status': True,
            'message': 'Document deleted successfully'
        }, status=status.HTTP_200_OK)

    return Response({
        'status': False,
        'message': 'Invalid request method'
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','DELETE'])
def delete_document(request):
    document_id = request.GET.get('document_id')
    
    if not document_id:
        return Response({
            "status": "error",
            "message": "document_id is required"
        }, status=400)

    try:
        document = get_object_or_404(Documents, document_id=document_id)
        document.delete()
        return Response({
            "status": "success",
            "message": "Document deleted successfully"
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Failed to delete Document: {str(e)}"
        }, status=500)


@api_view(['GET'])
def show_bank_cash(request):
    bank_cash_data = bank_cash.objects.all().values(
        'bank_cash_id',
        'credit_debit',
        'amount',
        'bank_id__bank_name',
        'date',
        'details'
    )
    
    bank_details_data = Bank_Details.objects.filter(person_id__person_name = 'Pinak Enterprise', bank_open_closed = True).values(
        'bank_id',
        'bank_name'
    )

    return Response({
        "status": "success",
        "title": "Bank Cash",
        "data": bank_cash_data,
        "bank_details_data": bank_details_data
    })


@api_view(['POST', 'GET'])
def insert_update_bank_cash(request):
    bank_details_data = Bank_Details.objects.all().values(
        'bank_id',
        'bank_name'
    )

    if request.method == 'POST':
        bank_cash_id = request.data.get('bank_cash_id')
        credit_debit = request.data.get('credit_debit')
        amount = request.data.get('amount')
        bank_id = request.data.get('bank_id')
        details = request.data.get('details')

        if bank_id:
            bank_instance = Bank_Details.objects.get(bank_id=bank_id)
        else:
            bank_instance = None

        if bank_cash_id:
            bank_cash_data = bank_cash.objects.get(bank_cash_id=bank_cash_id)
            if credit_debit=='Credit':
                bank_instance.bank_current_amount = bank_instance.bank_current_amount - float(bank_cash_data.amount)
                bank_instance.save()
            if credit_debit=='Debit':
                bank_instance.bank_current_amount = bank_instance.bank_current_amount + float(bank_cash_data.amount)
                bank_instance.save()
            bank_cash_data.credit_debit = credit_debit
            bank_cash_data.amount = amount
            bank_cash_data.bank_id = bank_instance
            bank_cash_data.date = date
            bank_cash_data.details = details
            bank_cash_data.save()
            if credit_debit=='Credit':
                bank_instance.bank_current_amount = bank_instance.bank_current_amount + float(amount)
                bank_instance.save()
            if credit_debit=='Debit':
                bank_instance.bank_current_amount = bank_instance.bank_current_amount - float(amount)
                bank_instance.save()
            message = "Bank cash details updated successfully."

        else:
            bank_cash_data = bank_cash.objects.create(
                credit_debit=credit_debit,
                amount=amount,
                bank_id=bank_instance,
                details=details
            )
            if credit_debit=='Credit':
                bank_instance.bank_current_amount = bank_instance.bank_current_amount + float(amount)
                bank_instance.save()
            if credit_debit=='Debit':
                bank_instance.bank_current_amount = bank_instance.bank_current_amount - float(amount)
                bank_instance.save()
            message = "Bank cash details created successfully."

        return Response({
            "status": "success",
            "message": message,
            "data": {
                "bank_cash_id": bank_cash_data.bank_cash_id,
                "credit_debit": bank_cash_data.credit_debit,
                "amount": bank_cash_data.amount,
                "bank_id": bank_cash_data.bank_id.bank_id,
                "date": bank_cash_data.date,
                "details": bank_cash_data.details,
            },
            "bank_details_data": bank_details_data
        })

    if request.GET.get('getdata_id'):
        bank_cash_id = request.GET.get('getdata_id')
        try:
            bank_cash_data = bank_cash.objects.get(bank_cash_id=bank_cash_id)
            return Response({
                "status": "success",
                "message": "Data fetched successfully.",
                "data": {
                    "bank_cash_id": bank_cash_data.bank_cash_id,
                    "credit_debit": bank_cash_data.credit_debit,
                    "amount": bank_cash_data.amount,
                    "bank_id": bank_cash_data.bank_id.bank_id,
                    "bank_name": bank_cash_data.bank_id.bank_name,
                    "date": bank_cash_data.date,
                    "details": bank_cash_data.details,
                },
                "bank_details_data": bank_details_data
            })
        except bank_cash.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Bank cash ID does not exist."
            }, status=404)

    return Response({
        "status": "error",
        "message": "Invalid request method."
    }, status=405)



@api_view(['GET','DELETE'])
def delete_bank_cash(request):
    bank_cash_id = request.GET.get('bank_cash_id')
    
    if not bank_cash_id:
        return Response({
            "status": "error",
            "message": "bank_cash_id is required"
        }, status=400)
    try:
        bank_cash_data = get_object_or_404(bank_cash, bank_cash_id=bank_cash_id)
        bank_instance = Bank_Details.objects.get(bank_id=bank_cash_data.bank_id.bank_id)
        if bank_cash_data.credit_debit=='Credit':
                bank_instance.bank_current_amount = bank_instance.bank_current_amount - float(bank_cash_data.amount)
                bank_instance.save()
        if bank_cash_data.credit_debit=='Debit':
                bank_instance.bank_current_amount = bank_instance.bank_current_amount + float(bank_cash_data.amount)
                bank_instance.save()
        bank_cash_data.delete()
        return Response({
            "status": "success",
            "message": "Bank Cash deleted successfully"
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Failed to delete Bank Cash: {str(e)}"
        }, status=500)




@api_view(['GET'])
def language_data(request):
    # data = language.objects.all().values('language_id','gujarati','english')
    # settingss = Settingsss.objects.get(settings_field_name = 'language')

    
    # if request.GET.get('language_change'):
    #     settingss.settings_field_value = request.GET.get('language_change')
    #     settingss.save()

    # if settingss.settings_field_value == 'gujarati':
    #     for x in data:
    #         x['lang'] = x['gujarati']
    # else:
    #     for x in data:
    #         x['lang'] = x['english']   


    # return Response({
    #         "status": "success",
    #         "message": "Language Data Fetched Successfully.",
    #         'data':data,
    #         'currentlanguage':settingss.settings_field_value
    #     })
    return Response({
        'status':True
    })


api_view(['GET', 'POST'])
def insert_document_date(request):
    pass



api_view(['DELETE'])
def delete_document_date(request):
    dd_id = request.GET.get('dd_id')
    if not dd_id:
        return Response({
            "status": "error",
            "message": "dd_id is required"
        }, status=400)
    try:
        document_date_data = get_object_or_404(Document_Dates, dd_id=dd_id)
        document_date_data.delete()
        return Response({
            "status": "success",
            "message": "Document Date deleted successfully"
        })
    except Exception as e:
        return Response({
            "status": "error",
            "message": f"Failed to delete Document Date: {str(e)}"
        }, status=500)

from datetime import date
@api_view(['GET'])
def show_daily_report(request):
    unique_project_names = Project_Day_Details.objects.values_list('project_id__project_name', flat=True).distinct()

    if request.GET.get('report_date'):
        today_date = request.GET.get('report_date')
    else:
        today_date = date.today()

    dailywise_credit_report = Money_Debit_Credit.objects.filter(money_date = today_date, receiver_person_id__person_name = 'Pinak Enterprise').values('sender_person_id__person_name', 'receiver_person_id__person_name', 'pay_type_id__pay_type_name', 'money_amount')

    x = Money_Debit_Credit.objects.filter(money_date = today_date, receiver_person_id__person_name = 'Pinak Enterprise').values('sender_person_id__person_name', 'receiver_person_id__person_name', 'pay_type_id__pay_type_name', 'money_amount').aggregate(total_amount_credit=Sum('money_amount'))
    total_credit_amount = x['total_amount_credit'] or 0 

    dailywise_debit_report = Money_Debit_Credit.objects.filter(money_date = today_date, sender_person_id__person_name = 'Pinak Enterprise').values('sender_person_id__person_name' , 'receiver_person_id__person_name', 'pay_type_id__pay_type_name', 'money_amount')

    y = Money_Debit_Credit.objects.filter(money_date = today_date, sender_person_id__person_name = 'Pinak Enterprise').values('sender_person_id__person_name' , 'receiver_person_id__person_name', 'pay_type_id__pay_type_name', 'money_amount').aggregate(total_amount=Sum('money_amount'))
    total_debit_amount = y['total_amount'] or 0

    project_day_detail_data = Project_Day_Details.objects.filter(proejct_day_detail_date = today_date).values(
        'project_day_detail_id',
        'project_id__project_name',
        'proejct_day_detail_date',
        'project_day_detail_machine_id__machine_name',
        'project_day_detail_machine_id__machine_number_plate',
        'project_day_detail_work_type__work_type_name',
        'project_day_detail_total_tyres',
        'project_day_detail_work_no',
        'project_day_detail_price',
        'project_day_detail_total_price',
        'project_day_detail_details'
    )

    z = Project_Day_Details.objects.filter(proejct_day_detail_date = today_date).values(
        'project_day_detail_id',
        'project_id__project_name',
        'proejct_day_detail_date',
        'project_day_detail_machine_id__machine_name',
        'project_day_detail_machine_id__machine_number_plate',
        'project_day_detail_work_type__work_type_name',
        'project_day_detail_total_tyres',
        'project_day_detail_work_no',
        'project_day_detail_price',
        'project_day_detail_total_price',
        'project_day_detail_details'
    ).aggregate(project_day_total_amount=Sum('project_day_detail_total_price'))
    total_project_day_detail_amount = z['project_day_total_amount'] or 0

    project_expense_data = Project_Expense.objects.filter(project_expense_date = today_date).values(
        'project_expense_id',
        'project_expense_name',
        'project_id__project_name',
        'project_expense_date',
        'project_expense_amount',
        'project_payment_mode',
        'bank_id__bank_name',
        'project_expense_desc',
    )

    materials_data = Material.objects.filter(material_buy_date = today_date).values(
        'material_id',
        'material_type_id__material_type_id',
        'material_type_id__material_type_name',
        'material_owner__person_id',
        'material_owner__person_name',
        'material_status',
        'material_buy_date',
        'material_buy_location',
        'material_work_type__work_type_id',
        'material_work_type__work_type_name',
        'material_work_no',
        'material_price',
        'material_total_price',
        'material_is_agent',
        'material_agent_name',
        'material_agent_contact',
        'material_agent_price_choice',
        'material_agent_percentage',
        'material_agent_amount',
        'material_final_amount',
        'material_details'
    )

    machine_maintenance_data = Machine_Maintenance.objects.filter(machine_maintenance_date = today_date).values(
        'machine_maintenance_id',
        'machine_machine_id__machine_name',
        'machine_machine_id__machine_number_plate',
        'machine_machine_id__machine_types_id__machine_type_name',
        'machine_maintenance_amount',
        'machine_maintenance_date',
        'machine_maintenance_amount_paid',
        'machine_maintenance_amount_paid_by',
        'machine_maintenance_driver_id__person_name',
        'machine_maintenance_driver_id__person_contact_number',
        'machine_maintenance_person_id__person_name',
        'machine_maintenance_person_id__person_contact_number',
        'machine_maintenance_details',
        'machine_maintenance_types_id__maintenance_type_name',
        'project_id__project_name',
    )


    return Response({
        'status': 'success',
        'title': 'Daily Reports',
        'dailywise_credit_report': dailywise_credit_report,
        'total_credit_amount': total_credit_amount,
        'dailywise_debit_report': dailywise_debit_report,
        'project_day_detail_data': project_day_detail_data,
        'total_project_day_detail_amount': total_project_day_detail_amount,
        'project_expense_data': project_expense_data,
        'unique_project_names': unique_project_names,
        'materials_data': materials_data,
        'machine_maintenance_data': machine_maintenance_data,
        'total_debit_amount': total_debit_amount,
    })

# @api_view(['GET'])
# def show_material_report(request):
#     materials_data = Material.objects.all().values(
#         'material_id',
#         'material_type_id__material_type_id',
#         'material_type_id__material_type_name',
#         'material_owner__person_id',
#         'material_owner__person_name',
#         'material_status',
#         'material_buy_date',
#         'material_buy_location',
#         'material_work_type__work_type_id',
#         'material_work_type__work_type_name',
#         'material_work_no',
#         'material_price',
#         'material_total_price',
#         'material_is_agent',
#         'material_agent_name',
#         'material_agent_contact',
#         'material_agent_price_choice',
#         'material_agent_percentage',
#         'material_agent_amount',
#         'material_final_amount',
#         'material_details'
#     )

#     total_material_amount = Material.objects.all().values(
#         'material_id',
#         'material_type_id__material_type_id',
#         'material_type_id__material_type_name',
#         'material_owner__person_id',
#         'material_owner__person_name',
#         'material_status',
#         'material_buy_date',
#         'material_buy_location',
#         'material_work_type__work_type_id',
#         'material_work_type__work_type_name',
#         'material_work_no',
#         'material_price',
#         'material_total_price',
#         'material_is_agent',
#         'material_agent_name',
#         'material_agent_contact',
#         'material_agent_price_choice',
#         'material_agent_percentage',
#         'material_agent_amount',
#         'material_final_amount',
#         'material_details'
#     ).aggregate(total_amount=Sum('material_total_price'))
#     total_material_amount = total_material_amount['total_amount'] or 0

#     materials = Material.objects.values(
#         'material_work_type__work_type_name'
#     ).annotate(
#         total_price=Sum('material_price')
#     )

#     work_type_data = []
#     for material in materials:
#         work_type_name = material['material_work_type__work_type_name']
#         individual_prices = list(
#             Material.objects.filter(
#                 material_work_type__work_type_name=work_type_name
#             ).values_list('material_price', flat=True)
#         )
        
#         work_type_data.append({
#             'work_type_name': work_type_name,
#             'individual_prices': individual_prices,
#             'total_price': material['total_price']
#         })
    
#     return Response({
#         'status': 'success',
#         'title': 'Material Reports',
#         'materials_data': materials_data,
#         'total_material_amount': total_material_amount,
#         'work_type_data': work_type_data,
#     })




@api_view(['GET'])
def show_material_report(request):
    material_owner_data = Material_Owner_data.objects.all()
    context={}
    for x in material_owner_data:
        total_material_avak = Project_Material_Data.objects.filter(project_material_material_id=x).aggregate(total=Sum('project_material_total_amount'))['total'] or 0
        padatar_rakam = Material.objects.filter(material_owner=x.material_owner_person_id).aggregate(total=Sum('material_final_amount'))['total'] or 0
        material_agent_amount = Material.objects.filter(material_owner=x.material_owner_person_id,material_is_agent=1).aggregate(total=Sum('material_agent_amount'))['total'] or 0 
        profit_loss = total_material_avak - padatar_rakam - material_agent_amount
        projectwiseData = []
        for proj in Project.objects.all():
            Project_par_fera = Project_Material_Data.objects.filter(project_material_material_id=x,project_id = proj).values('project_material_work_no','project_material_price','project_material_total_amount','person_material_information')
            counter = Project_Material_Data.objects.filter(project_material_material_id=x,project_id = proj).count()
            data = {'Project_par_fera':Project_par_fera,'project_name':proj.project_name,'rows':counter}
            projectwiseData.append(data)
        context.update({'Material Owner Name':x.material_owner_person_id.person_name,'location':x.Material_Owner_location,'total_aavak':total_material_avak,'padatar_rakam':padatar_rakam,'dalali_rakam':material_agent_amount,'profit_loss':profit_loss,'projectwiseData':projectwiseData})

    return Response(context)

@api_view(['GET'])
def show_person_report(request):
    person_id = request.GET.get('person_id')
    persons_data = Person.objects.get(person_id=int(person_id))
    context = {}
    data = {}
    
    data.update({'person_data':{'person_name':persons_data.person_name,'person_id':persons_data.person_id},'person_details_data':person_report_data(persons_data.person_id)})
    context.update({'data':data})
    return Response(context)


@api_view(['GET'])
def show_diary(request):
    diary_data = diary.objects.all().values('diary_id','diary_text')

    return Response({
        'status': 'success',
        'title': 'Diary',
        'data': diary_data,
    })



@api_view(['POST', 'GET'])
def insert_update_diary(request):
    diary_text = request.data.get('diary_text')
    diary_id = request.data.get('diary_id')

    if request.GET.get('getdata_id'):
        diary_obj = diary.objects.get(diary_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            'diary_id': diary_obj.diary_id,
            'diary_text': diary_obj.diary_text,
        }
        })
    if request.method == 'POST':
        if diary_id:
            diary_obj = diary.objects.get(diary_id=diary_id)
            diary_obj.diary_text = diary_text
            diary_obj.save()
            message = "Diary updated successfully."
        else:
            diary_obj = diary.objects.create(
                diary_text=diary_text
            )
            message = "Data created successfully."

        return Response({
            "status": "success",
            "message": message,
        })
    else:
        return Response({
            "status": "False"
        })


@api_view(['DELETE'])
def delete_diary(request):
    diary_id = request.GET.get('diary_id')

    if not diary_id:
        return Response({
            "status": "error",
            "message": "Diary is required."
        }, status=400)

    try:
        diary_obj = diary.objects.get(diary_id=diary_id)
        diary_obj.delete()
        return Response({
            "status": "success",
            "message": "Diary deleted successfully."
        })
    except diary_obj.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Diary not found."
        }, status=404)

    

@api_view(['GET'])
def show_machine_rent(request):
    Rented_machines = machine_rent.objects.all().values(
        'machine_rent_id',
        'machine_rent_machine_id__machine_id',
        'machine_rent_machine_id__machine_name',
        'machine_rent_machine_id__machine_types_id__machine_type_name',
        'machine_rent_machine_id__machine_number_plate',
        'machine_rent_machine_id__machine_id',
        'machine_rented_work_type__work_type_name',
        'machine_rented_work_type__work_type_id',
        'machine_rented_work_price',
        'machine_km',
        'rent_start_date',
        'rent_end_date',
        'rent_amount',
    )
    machinedata = Machines.objects.all().values('machine_name', 'machine_id','machine_number_plate','machine_types_id__machine_type_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    return Response({
        "status": "success",
        "title": "Rented Machine",
        'machinedata': machinedata,
        'work_types_data': work_types_data,
        'data':Rented_machines,
    })



@api_view(['POST', 'GET'])
def insert_update_machine_rent(request):
    machine_rent_machine_id = request.data.get('machine_rent_machine_id')
    machine_rented_work_type = request.data.get('machine_rented_work_type')
    machine_rented_work_price = request.data.get('machine_rented_work_price')
    machine_km = request.data.get('machine_km')
    machine_rent_id = request.data.get('machine_rent_id')
    rent_start_date = request.data.get('rent_start_date')
    rent_end_date = request.data.get('rent_end_date') if request.data.get('rent_end_date') else None
    

        

    if request.GET.get('getdata_id'):
        machine_rent_data = machine_rent.objects.get(machine_rent_id=request.GET.get('getdata_id'))
        return Response({
        "status": "success",
        "message": 'Data Fetched Successfully',
        "data": {
            'machine_rent_id': machine_rent_data.machine_rent_id,
            'machine_rent_machine_id': machine_rent_data.machine_rent_machine_id.machine_id,
            'machine_rented_work_type': machine_rent_data.machine_rented_work_type.work_type_id,
            'machine_rented_work_price':machine_rent_data.machine_rented_work_price,
            'machine_km':machine_rent_data.machine_km,
            'rent_start_date':machine_rent_data.rent_start_date,
            'rent_end_date':machine_rent_data.rent_end_date,
        }
        })
    if request.method == 'POST':
        if machine_rent_id:
            machine_rent_data = machine_rent.objects.get(machine_rent_id=machine_rent_id)
            rented_work_amount= 0

            if rent_end_date:
                machine_work_data = Project_Machine_Data.objects.filter(
                    machine_project_id = machine_rent_data.machine_rent_machine_id,
                    project_machine_date__gte=rent_start_date,
                    project_machine_date__lte=rent_end_date
                ).aggregate(total_work=Sum('project_machine_data_work_number'))['total_work']
                machine_work_data = machine_work_data if machine_work_data else 0
            machine_rent_data.rent_amount =int(machine_rent_data.machine_rented_work_price)* machine_work_data
            machine_rent_data.machine_rented_work_type = Work_Types.objects.get(work_type_id = machine_rented_work_type)
            machine_rent_data.machine_rented_work_price = machine_rented_work_price
            machine_rent_data.machine_km = machine_km
            machine_rent_data.machine_rent_machine_id = Machines.objects.get(machine_id = machine_rent_machine_id)
            machine_rent_data.rent_start_date = rent_start_date
            machine_rent_data.rent_end_date = rent_end_date
            machine_rent_data.save()
            message = "Machine Rented updated successfully."
        else:
            diary_obj = machine_rent.objects.create(
                machine_rented_work_type = Work_Types.objects.get(work_type_id = machine_rented_work_type),
                machine_rented_work_price = machine_rented_work_price,
                machine_km = machine_km,
                machine_rent_machine_id = Machines.objects.get(machine_id = machine_rent_machine_id),
                rent_start_date = rent_start_date,
                rent_end_date = rent_end_date
            )
            message = "Data created successfully."

        return Response({
            "status": "success",
            "message": message,
        })
    else:
        return Response({
            "status": "False"
        })


@api_view(['DELETE'])
def delete_machine_rent(request):
    rentedmachine_id = request.GET.get('rentedmachine_id')

    if not rentedmachine_id:
        return Response({
            "status": "error",
            "message": "Rented Machine id is required."
        }, status=400)

    try:
        machine_rent_obj = machine_rent.objects.get(machine_rent_id=rentedmachine_id)
        machine_rent_obj.delete()
        return Response({
            "status": "success",
            "message": "Data deleted successfully."
        })
    except machine_rent_obj.DoesNotExist:
        return Response({
            "status": "error",
            "message": "Data not found."
        }, status=404)

    



@api_view(['GET'])
def show_bill(request):

    project_id = int(request.GET.get('project_id'))
    print(project_id)
    bill_data = Bill.objects.filter(Project_id__project_id=project_id).values(
        'bill_id',
        'invoice_number',
        'is_tax',
        'Project_id__project_id',
        'Project_id__project_discount',
        'Project_id__project_cgst',
        'Project_id__project_sgst',
        'Project_id__project_tax',
        'Project_id__project_name',
        'Project_id__project_location',
        'Project_id__project_types_id__project_type_name',
        'Project_id__project_owner_name__person_name',
        'Project_id__project_owner_name__person_contact_number',
        'Project_id__project_owner_name__person_address',
        'Project_id__project_owner_name__person_gst',
        'invoice_date',
    )
    print(bill_data)
    if bill_data:
        pass
    else:
        return Response({
            'message':'Bill is not Available'
        })
    day_details_data = Project_Day_Details.objects.filter(project_id=project_id)

    project_day_details_data = day_details_data.values(
        'project_day_detail_id',
        'proejct_day_detail_date',
        'project_day_detail_machine_id__machine_name',
        'project_day_detail_machine_id__machine_number_plate',
        'project_day_detail_work_type__work_type_name',
        'project_day_detail_total_tyres',
        'project_day_detail_work_no',
        'project_day_detail_price',
        'project_day_detail_total_price',
        'project_day_detail_details'
    )

    total_amount = project_day_details_data.aggregate(
            total_amount=Sum('project_day_detail_total_price')
        )['total_amount']
    
    discount = bill_data[0]['Project_id__project_discount']
    print(bill_data[0]['Project_id__project_tax'])

    return Response({
        "status": "success",
        "title": "Invoice",
        'data':bill_data,
        'project_day_details_data':project_day_details_data,
        'total_amount':total_amount,
        'discount':int(discount) if discount else 0,

    })



from django.http import JsonResponse

@api_view(['GET'])
def overall_report(request):
    # Salary Data
    salary_data = Salary.objects.all()
    total_salary = salary_data.aggregate(total_salary=Sum('salary_amount'))
    salary_data = salary_data.values(
        'salary_date', 'salary_amount', 'salary_working_days', 'salary_details',
        'person_id__person_id', 'person_id__person_name', 'person_id__person_contact_number'
    )

    # Machine Rent Data
    machine_rent_data = machine_rent.objects.all()
    total_machine_rent = machine_rent_data.aggregate(total_rent=Sum('rent_amount'))
    machine_rent_data = machine_rent_data.values(
        'machine_rent_id', 'machine_rent_machine_id__machine_name', 
        'machine_rent_machine_id__machine_id', 'machine_rent_machine_id__machine_number_plate',
        'machine_rented_work_type__work_type_name', 'machine_rented_work_price', 'rent_amount'
    )

    # Machine Maintenance Data
    Machine_Maintenance_data = Machine_Maintenance.objects.all()
    total_maintenance = Machine_Maintenance_data.aggregate(total_maintenance=Sum('machine_maintenance_amount'))
    Machine_Maintenance_data = Machine_Maintenance_data.values(
        'machine_maintenance_id', 'machine_machine_id', 'machine_machine_id__machine_name',
        'machine_machine_id__machine_number_plate', 'machine_maintenance_amount', 'machine_maintenance_date',
        'machine_maintenance_person_id__person_id', 'machine_maintenance_person_id__person_name',
        'machine_maintenance_person_id__person_contact_number'
    )

    # Project Data
    Project_data = Project.objects.all()
    total_project_amount = Project_data.aggregate(total_project=Sum('project_amount'))
    Project_data = Project_data.values(
        'project_id', 'project_name', 'project_location', 'project_amount', 
        'project_status', 'project_owner_name__person_name', 'project_owner_name__person_contact_number'
    )

    # Material Data
    material_data = Project_Material_Data.objects.all()
    total_material_amount = material_data.aggregate(total_material=Sum('project_material_total_amount'))

    material_data = material_data.values(
        'project_material_date', 'project_material_material_id__material_owner__person_name',
        'project_material_material_id__material_owner__person_contact_number',
        'project_material_material_id__material_owner__person_id', 'project_material_material_id__material_details','project_material_total_amount'
    )

    # Person Data
    person_data = Project_Person_Data.objects.all()
    total_person_price = person_data.aggregate(total_person_price=Sum('project_person_total_price'))
    person_data = person_data.values(
        'person_id__person_name', 'person_id__person_id', 'person_id__person_contact_number',
        'work_type_id__work_type_name', 'project_person_work_num', 'project_person_price',
        'project_person_total_price', 'project_person_paid_by', 'project_id__project_name',
        'project_id__project_owner_name__person_name'
    )

    # Money Debit Data
    money_debit_data = Money_Debit_Credit.objects.filter(sender_person_id__person_id=1)
    total_money_debit = money_debit_data.aggregate(total_debit=Sum('money_amount'))
    money_debit_data = money_debit_data.values(
        'receiver_person_id__person_id', 'receiver_person_id__person_name', 
        'receiver_person_id__person_contact_number', 'pay_type_id__pay_type_name', 
        'money_payment_mode', 'money_amount', 'money_date', 'sender_bank_id__bank_name', 
        'money_sender_cheque_no', 'money_payment_details', 'machine_id__machine_name',
        'machine_id__machine_number_plate', 'project_id__project_name'
    )

    # Money Credit Data
    money_credit_data = Money_Debit_Credit.objects.filter(receiver_person_id__person_id=1)
    total_money_credit = money_credit_data.aggregate(total_credit=Sum('money_amount'))
    money_credit_data = money_credit_data.values(
        'sender_person_id__person_id', 'sender_person_id__person_name', 
        'sender_person_id__person_contact_number', 'pay_type_id__pay_type_name', 
        'money_payment_mode', 'money_amount', 'money_date', 'sender_bank_id__bank_name', 
        'money_sender_cheque_no', 'money_payment_details', 'machine_id__machine_name',
        'machine_id__machine_number_plate', 'project_id__project_name'
    )

    # Combine totals into a single dictionary
    totals = {
        'total_salary': total_salary,
        'total_machine_rent': total_machine_rent,
        'total_maintenance': total_maintenance,
        'total_project_amount': total_project_amount,
        'total_person_price': total_person_price,
        'total_money_debit': total_money_debit,
        'total_money_credit': total_money_credit,
        'total_material_amount':total_material_amount,
    }

    response = {
        'salary_data': salary_data,
        'machine_rent_data': machine_rent_data,
        'Machine_Maintenance_data': Machine_Maintenance_data,
        'Project_data': Project_data,
        'material_data': material_data,
        'person_data': person_data,
        'money_debit_data': money_debit_data,
        'money_credit_data': money_credit_data,
        'totals': totals,
    }
    return Response(response)



from django.forms.models import model_to_dict

@api_view(['GET'])
def machine_report(request):
    machine_id = request.GET.get('machine_id')
    machine_obj = Machines.objects.get(machine_id=machine_id)
    all_projects = Project.objects.all()
    machine_detailed_data = {}
    if True:
        machine_info={'machine_id':machine_obj.machine_id,'machine_name':machine_obj.machine_name,'machine_number_plate':machine_obj.machine_number_plate,'machine_register_date':machine_obj.machine_register_date,'machine_own':machine_obj.machine_own,'machine_types_name':machine_obj.machine_types_id.machine_type_name,'machine_details':machine_obj.machine_details,'machine_owner':machine_obj.machine_owner_id.person_name,'Owner_contact':machine_obj.machine_owner_id.person_contact_number,'machine_buy_price':machine_obj.machine_buy_price,'machine_buy_date':machine_obj.machine_buy_date,'machine_other_details':machine_obj.machine_other_details}
        projectwisedata = []
        for y in all_projects:
            
            project_info = {'project_name':y.project_name,'project_amount':y.project_amount,'project_location':y.project_location,'project_owner_name':y.project_owner_name.person_name}
            project_machine_data = Project_Machine_Data.objects.filter(machine_project_id = machine_obj,project_id = y).values('project_machine_date','work_type_id__work_type_name','project_machine_data_work_number','project_machine_data_work_price','project_machine_data_total_amount','project_machine_data_work_details')
            project_machine_data_total = Project_Machine_Data.objects.filter(machine_project_id = machine_obj,project_id = y).aggregate(total=Sum('project_machine_data_total_amount'))['total'] or 0
            machine_maramat_data = Machine_Maintenance.objects.filter(project_id = y,machine_machine_id=machine_obj).values('machine_maintenance_amount','machine_maintenance_date','machine_maintenance_amount_paid_by','machine_maintenance_amount_paid','machine_maintenance_types_id__maintenance_type_name','machine_maintenance_types_id__maintenance_type_id','machine_maintenance_details','machine_maintenance_person_id__person_name','machine_maintenance_person_id__person_id','machine_maintenance_driver_id__person_name','machine_maintenance_driver_id__person_id')
            machine_maramat_data_total = Machine_Maintenance.objects.filter(project_id = y,machine_machine_id=machine_obj).aggregate(total=Sum('machine_maintenance_amount'))['total'] or 0
            projectwisedata.append({'project_info':project_info,'project_machine_data':project_machine_data,'maintenance_data':machine_maramat_data,'project_machine_data_total':project_machine_data_total,'machine_maramat_data_total':machine_maramat_data_total})
        
        other_maintenance_data = Machine_Maintenance.objects.filter(machine_machine_id=machine_obj).values('machine_maintenance_amount','machine_maintenance_date','machine_maintenance_amount_paid_by','machine_maintenance_amount_paid','machine_maintenance_types_id__maintenance_type_name','machine_maintenance_types_id__maintenance_type_id','machine_maintenance_details','machine_maintenance_person_id__person_name','machine_maintenance_person_id__person_id','machine_maintenance_driver_id__person_name','machine_maintenance_driver_id__person_id')
        other_maintenance_data_total = Machine_Maintenance.objects.filter(machine_machine_id=machine_obj).aggregate(total=Sum('machine_maintenance_amount'))['total'] or 0
        machine_total_deasel_amount = Machine_Maintenance.objects.filter(machine_maintenance_types_id__maintenance_type_name='ડીઝલ').aggregate(total=Sum('machine_maintenance_amount'))['total'] or 0
        machine_detailed_data.update({'machine_info':machine_info,'projectwisedata':projectwisedata,'other_maintenance_data':other_maintenance_data,'other_maintenance_data_total':other_maintenance_data_total,'machine_total_deasel_amount':machine_total_deasel_amount})

    return Response({
        'data':machine_detailed_data,
        'message':'Success'
    })



@api_view(['GET'])
def person_report(request):
    # Fetch all persons
    all_persons = Person.objects.exclude(person_status=0)
    
    person_detailed_data = []

    for person in all_persons:
        # Gather basic person information
        person_info = {
            'person_name': person.person_name,
            'person_contact_number': person.person_contact_number,
            'person_register_date': person.person_register_date,
            'person_salary': person.person_salary
        }

        projectwisedata = []

        # ================= For Project Owners =================
        # Fetch projects where the person is the owner
        owned_projects = Project.objects.filter(project_owner_name__person_id=person.person_id)
        for project in owned_projects:
            project_info = {
                'project_name': project.project_name,
                'project_amount': project.project_amount,
                'project_location': project.project_location,
                'project_owner_name': project.project_owner_name.person_name,
                'project_grahak_amount': project.project_grahak_amount
            }
            projectwisedata.append({'project_info': project_info})

        # ================= For Bhatthu Data =================
        # Fetch all projects and check if the person is involved in them
        all_projects = Project.objects.all()
        for project in all_projects:
            project_info = {
                'project_name': project.project_name,
                'project_amount': project.project_amount,
                'project_location': project.project_location,
                'project_owner_name': project.project_owner_name.person_name,
                'project_grahak_amount': project.project_grahak_amount
            }
            project_person_data = Project_Person_Data.objects.filter(
                project_id=project.project_id,
                person_id=person.person_id
            ).values(
                'work_type_id__work_type_name',
                'project_person_work_num',
                'project_person_price',
                'project_person_total_price'
            )
            if project_person_data.exists():
                projectwisedata.append({
                    'project_info': project_info,
                    'project_person_data': list(project_person_data)  # Convert to list for JSON serialization
                })

        # ================= For Maintenance Data =================
        maintenance_data = Machine_Maintenance.objects.filter(
            machine_maintenance_person_id__person_id=person.person_id
        )
        maintenancee = []
        for maintenance in maintenance_data:
            maintenancee.append({
                'machine_maintenance_amount': maintenance.machine_maintenance_amount,
                'machine_machine_name': f"{maintenance.machine_machine_id.machine_name} ({maintenance.machine_machine_id.machine_number_plate})",
                'machine_maintenance_date': maintenance.machine_maintenance_date,
                'machine_maintenance_types_name': maintenance.machine_maintenance_types_id.maintenance_type_name,
                'machine_maintenance_details': maintenance.machine_maintenance_details
            })

        # Append person info and associated data
        person_detailed_data.append({
            'person_info': person_info,
            'projectwisedata': projectwisedata,
            'maintenance_data': maintenancee
        })

    return Response({
        'data': person_detailed_data,
        'message': 'Success'
    })






@api_view(['GET'])
def person_bhaththu_report(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    # Fetch all persons
    personindaydetail = Project_Person_Data.objects.values_list('person_id__person_id',flat=True)
    all_persons = Person.objects.exclude(person_status=0).filter(person_id__in = personindaydetail)
    
    person_detailed_data = []

    for person in all_persons:
        # Gather basic person information
        person_info = {
            'person_name': person.person_name,
            'person_contact_number': person.person_contact_number,
            'person_register_date': person.person_register_date,
            'person_salary': person.person_salary
        }

        projectwisedata = []
        total_kharch = 0
        # ================= For Bhatthu Data =================
        # Fetch all projects and check if the person is involved in them
        all_projects = Project.objects.all()
        for project in all_projects:
            project_info = {
                'project_name': project.project_name,
                'project_amount': project.project_amount,
                'project_location': project.project_location,
                'project_owner_name': project.project_owner_name.person_name,
                'project_grahak_amount': project.project_grahak_amount
            }
            project_persons_data = Project_Person_Data.objects.filter(
                project_id=project.project_id,
                person_id=person.person_id
            )

            if start_date and end_date:
                project_person_data = project_persons_data.filter(project_person_date__range=[start_date, end_date]).values(
                    'work_type_id__work_type_name',
                    'project_person_work_num',
                    'project_person_price',
                    'project_person_total_price'
                )
                total_amount = project_persons_data.filter(project_person_date__range=[start_date, end_date]).aggregate(
                total_amount=Sum('project_person_total_price')
                )['total_amount']
                
            else:
                project_person_data = project_persons_data.values(
                    'work_type_id__work_type_name',
                    'project_person_work_num',
                    'project_person_price',
                    'project_person_total_price'
                )
                total_amount = project_persons_data.aggregate(
                total_amount=Sum('project_person_total_price')
                )['total_amount']
            
            total_kharch = (total_amount if total_amount else 0) + total_kharch
            
            
            if project_person_data.exists():
                projectwisedata.append({
                    'project_info': project_info,
                    'project_person_data': list(project_person_data),  # Convert to list for JSON serialization
                    'total_amount':int(total_amount) if total_amount else 0,
                })


        # Append person info and associated data
        person_detailed_data.append({
            'person_info': person_info,
            'projectwisedata': projectwisedata,
            'total_kharch':total_kharch,
        })

    return Response({
        'data': person_detailed_data,
        'message': 'Success'
    })



from django.db.models import Q, Sum
@api_view(['GET'])
def rokad_cash_calculation(request):
    
    initial_rokad = Company_Details.objects.first().company_sharuaati_shilak
    print(initial_rokad)
    total_maintenance_amount = Machine_Maintenance.objects.filter(Q(machine_maintenance_amount_paid = True) | Q(machine_maintenance_amount_paid_by = 'Pinak') | Q(machine_maintenance_amount_paid_by = 'Company_Owner')).aggregate(
                total_amount=Sum('machine_maintenance_amount')
                )['total_amount'] or 0
    total_maintenance_amount = int(total_maintenance_amount) if total_maintenance_amount else 0


    total_project_person_amount = Project_Person_Data.objects.filter(
        (Q(project_person_paid_by='Pinak') | Q(project_person_paid_by='Project_Owner')) & Q(person_payment_mode='Cash')
    ).aggregate(
        total_amount=Sum('project_person_total_price')
    )['total_amount'] or 0
    total_project_person_amount = int(total_project_person_amount) if total_project_person_amount else 0


    total_project_expense_amount = Project_Expense.objects.filter(project_payment_mode='Cash').aggregate(
        total_amount=Sum('project_expense_amount')
    )['total_amount'] or 0
    total_project_expense_amount = int(total_project_expense_amount) if total_project_expense_amount else 0

    total_credit_debit_amount_javak = Money_Debit_Credit.objects.filter(money_payment_mode='CASH',sender_person_id__person_id = 1).aggregate(
        total_amount=Sum('money_amount')
    )['total_amount'] or 0
    total_credit_debit_amount_javak = int(total_credit_debit_amount_javak) if total_credit_debit_amount_javak else 0

    total_credit_debit_amount_aavak = Money_Debit_Credit.objects.filter(money_payment_mode='CASH',receiver_person_id__person_id = 1).aggregate(
        total_amount=Sum('money_amount')
    )['total_amount'] or 0
    total_credit_debit_amount_aavak = int(total_credit_debit_amount_aavak) if total_credit_debit_amount_aavak else 0

    kul_rokad_amount = initial_rokad - total_maintenance_amount - total_project_person_amount - total_project_expense_amount - total_credit_debit_amount_javak + total_credit_debit_amount_aavak


    # =================================================bank calculation =====================================
    
    initial_Bank_amount = Bank_Details.objects.filter(company_bank_account=True).aggregate(
        total_amount=Sum('bank_initial_amount')
    )['total_amount'] or 0

    bank_total_project_person_amount = Project_Person_Data.objects.filter(
        (Q(project_person_paid_by='Pinak') | Q(project_person_paid_by='Project_Owner')) & Q(person_payment_mode='Bank')
    ).aggregate(
        total_amount=Sum('project_person_total_price')
    )['total_amount'] or 0
    bank_total_project_person_amount = int(bank_total_project_person_amount) if bank_total_project_person_amount else 0


    bank_total_project_expense_amount = Project_Expense.objects.filter(project_payment_mode='Bank').aggregate(
        total_amount=Sum('project_expense_amount')
    )['total_amount'] or 0
    bank_total_project_expense_amount = int(bank_total_project_expense_amount) if bank_total_project_expense_amount else 0

    bank_total_credit_debit_amount_javak = Money_Debit_Credit.objects.filter(money_payment_mode='BANK',sender_person_id__person_id = 1).aggregate(
        total_amount=Sum('money_amount')
    )['total_amount'] or 0
    bank_total_credit_debit_amount_javak = int(bank_total_credit_debit_amount_javak) if bank_total_credit_debit_amount_javak else 0

    bank_total_credit_debit_amount_aavak = Money_Debit_Credit.objects.filter(money_payment_mode='BANK',receiver_person_id__person_id = 1).aggregate(
        total_amount=Sum('money_amount')
    )['total_amount'] or 0
    bank_total_credit_debit_amount_aavak = int(bank_total_credit_debit_amount_aavak) if bank_total_credit_debit_amount_aavak else 0

    kul_bank_amount = initial_Bank_amount - bank_total_project_person_amount - bank_total_project_person_amount - bank_total_project_expense_amount - bank_total_credit_debit_amount_javak + bank_total_credit_debit_amount_aavak


    current_rokad_amount = rokad_amount(request)
    kul_bank_amount = totalbank_amount(request)

    return Response({
        'status' : True,
        'total_project_person_amount':total_project_person_amount,
        'total_maintenance_amount':total_maintenance_amount,
        'total_project_expense_amount':total_project_expense_amount,
        'total_credit_debit_amount_javak':total_credit_debit_amount_javak,
        'total_credit_debit_amount_aavak':total_credit_debit_amount_aavak,
        'kul_rokad_amount':kul_rokad_amount,
        'current_rokad_amount':current_rokad_amount,

        'bank_total_project_person_amount':bank_total_project_person_amount,
        'bank_total_project_expense_amount':bank_total_project_expense_amount,
        'bank_total_credit_debit_amount_javak':bank_total_credit_debit_amount_javak,
        'bank_total_credit_debit_amount_aavak':bank_total_credit_debit_amount_aavak,
        'kul_bank_amount':kul_bank_amount,
        'kul_levani_baki_rakam':kul_rakam_hisab(request)['kul_levani_baki_rakam'],
        'kul_aapvani_baki_rakam':kul_rakam_hisab(request)['kul_aapvani_baki_rakam'],
        'kul_rakam':kul_rakam_hisab(request)['kul_rakam']

    })







@api_view(['GET'])
def bank_credit_report(request):
    bank_id = request.GET.get('bank_id')
    data = bank_credit_report_data(int(bank_id))
    return Response({'data':data,'message':'success'})



@api_view(['GET'])
def bank_debit_report(request):
    bank_id = request.GET.get('bank_id')
    data = bank_debit_report_data(int(bank_id))
    return Response({'data':data,'message':'success'})