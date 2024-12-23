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
        'work_type_details'
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
            'work_type_details': work_type_obj.work_type_details,    
        }
        })
    
    if request.method == 'POST':
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
    persons = Person.objects.all()
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

    
    person_types = Person_Type.objects.all().values(
        'person_type_id', 
        'person_type_name'
    )     





    
    return Response({
        "status": "success",
        "title": "Person Data",
        "person_types": list(person_types),
        "data": list(persons),
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
        'bank_open_closed',
        'person_id__person_name',
        'person_id__person_contact_number',
    )

    company_person_name = [persons.person_id.person_name for persons in Bank_Details.objects.filter(company_bank_account = True)]

    credit_debit_data = Money_Debit_Credit.objects.filter(money_payment_mode = 'BANK').values('sender_person_id__person_name', 'receiver_person_id__person_name', 'money_amount', 'pay_type_id__pay_type_name', 'money_payment_mode', 'money_date', 'sender_bank_id__bank_name', 'receiver_bank_id__bank_name', 'money_payment_details')

    bank_credit_total = 0
    bank_debit_total = 0
    for credit_debit in credit_debit_data:
        
        if credit_debit['sender_person_id__person_name'] in company_person_name:
            credit_debit['credit_debit'] = 'Debit'
            bank_debit_total += int(credit_debit['money_amount'])
        else:
            credit_debit['credit_debit'] = 'Credit'
            bank_credit_total += int(credit_debit['money_amount'])
    print("de", bank_debit_total)
    print("ce", bank_credit_total)

    persons = Person.objects.all().values(
        'person_id',
        'person_name'
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
    persons = Person.objects.all().values(
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
        'machine_rented_work_price',
        'machine_rented_work_type__work_type_id',

    )
    machine_types_data = Machine_Types.objects.all().values(
        'machine_type_id', 
        'machine_type_name'
    )

    persons_data = Person.objects.all().values('person_id', 'person_name', 'person_contact_number')
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
        machine_rented_work_type = request.data.get('machine_rented_work_type')
        if machine_rented_work_type:
            machine_rented_work_type = Work_Types.objects.get(work_type_id = machine_rented_work_type)
            machine_rented_work_price = request.data.get('machine_rented_work_price')
        else:
            machine_rented_work_type = None
            machine_rented_work_price = None
        machine_buy_date = request.data.get('machine_buy_date')
        machine_sold_price = request.data.get('machine_sold_price')
        machine_sold_out_date = request.data.get('machine_sold_out_date')
        machine_other_details = request.data.get('machine_other_details')

        machine_types_instance = Machine_Types.objects.get(machine_type_id=machine_types_id)
        if machine_owner_id:
            machine_owner_id = Person.objects.get(person_id = machine_owner_id)

        if machine_buy_date:
            pass
        else:
            machine_buy_date = None
        if machine_sold_out_date:
            pass
        else:
            machine_sold_out_date = None

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
                "machine_buy_date": machine_obj.machine_buy_date,
                "machine_sold_price": machine_obj.machine_sold_price,
                "machine_sold_out_date": machine_obj.machine_sold_out_date,
                "machine_other_details": machine_obj.machine_other_details,
                "machine_rented_work_price":machine_obj.machine_rented_work_price,
                "machine_rented_work_type":machine_obj.machine_rented_work_type.work_type_id,
                "machine_rented_work_type_name":machine_obj.machine_rented_work_type.work_type_name,
            },
        })

    if request.method == 'POST':
        if machine_id:
            machine = Machines.objects.get(machine_id=machine_id)
            machine.machine_name = machine_name
            machine.machine_number_plate = machine_number_plate
            machine.machine_register_date = machine_register_date
            machine.machine_own = machine_own
            machine.machine_condition = machine_condition
            machine.machine_working = machine_working
            machine.machine_types_id = machine_types_instance
            machine.machine_details = machine_details
            machine.machine_owner_id = machine_owner_id
            machine.machine_buy_price = machine_buy_price
            machine.machine_buy_date = machine_buy_date
            machine.machine_sold_price = machine_sold_price
            machine.machine_sold_out_date = machine_sold_out_date
            machine.machine_other_details = machine_other_details
            machine.machine_rented_work_price = machine_rented_work_price
            machine_rented_work_type = machine_rented_work_type
            machine.save()
            message = "Machine details updated successfully."
        else:
            machine = Machines.objects.create(
                machine_name=machine_name,
                machine_number_plate=machine_number_plate,
                machine_register_date=machine_register_date,
                machine_own=machine_own,
                machine_condition=machine_condition,
                machine_working=machine_working,
                machine_types_id=machine_types_instance,
                machine_details=machine_details,
                machine_owner_id = machine_owner_id,
                machine_buy_price=machine_buy_price,
                machine_buy_date=machine_buy_date,
                machine_sold_price=machine_sold_price,
                machine_sold_out_date=machine_sold_out_date,
                machine_other_details=machine_other_details,
                machine_rented_work_price = machine_rented_work_price if machine_rented_work_price else None,
                machine_rented_work_type = machine_rented_work_type
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
                "machine_rented_work_price": machine.machine_rented_work_price if machine.machine_rented_work_price else None,
                "machine_rented_work_type":machine.machine_rented_work_type.work_type_id if machine.machine_rented_work_type else None,
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
        'receiver_person_id__person_name',
        'pay_type_id__pay_type_name',
        'money_payment_mode',
        'money_amount',
        'money_date',
        'sender_bank_id__bank_name',
        'money_sender_cheque_no',
        'receiver_bank_id__bank_name',
        'money_payment_details',
        'machine_id__machine_name',
        'project_id__project_name',
    )

    money_credit_data = money_debit_credit_data.filter(sender_person_id__person_name = 'pinak enterprise').values(
        'money_id',
        'sender_person_id__person_name',
        'receiver_person_id__person_name',
        'pay_type_id__pay_type_name',
        'money_amount',
        'money_payment_mode',
        'money_date',
        'sender_bank_id__bank_name',
        'receiver_bank_id__bank_name',
        'machine_id__machine_name',
        'project_id__project_name',
    )

    money_debit_data =  money_debit_credit_data.filter(receiver_person_id__person_name = 'pinak enterprise').values(
        'money_id',
        'sender_person_id__person_name',
        'receiver_person_id__person_name',
        'pay_type_id__pay_type_name',
        'money_amount',
        'money_payment_mode',
        'money_date',
        'sender_bank_id__bank_name',
        'receiver_bank_id__bank_name',
        'machine_id__machine_name',
        'project_id__project_name',
    )

    persons_data = Person.objects.all().values('person_id', 'person_name', 'person_contact_number')
    banks_data = Bank_Details.objects.all().values('bank_id', 'bank_name', 'bank_account_number', 'person_id', 'person_id__person_name')
    pay_types_data = Pay_Types.objects.all().values('pay_type_id', 'pay_type_name')
    machines_data = Machines.objects.all().values('machine_id', 'machine_name')  
    projects_data = Project.objects.all().values('project_id', 'project_name')
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
        "money_debit_data": money_debit_data,
    })  


@api_view(['POST', 'GET'])
def insert_update_money_debit_credit(request):
    persons_data = Person.objects.all().values('person_id', 'person_name', 'person_contact_number')
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
        money_amount = request.data.get('money_amount')
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
    salary_details = Salary.objects.all().values(
        'salary_id',
        'salary_date', 
        'salary_amount',
        'person_id__person_salary',
        'salary_working_days', 
        'salary_details', 
        'person_id__person_name',
        'person_id__person_contact_number'
    )

    money_transaction_data = Money_Debit_Credit.objects.filter(pay_type_id__pay_type_name = 'salary').values(
        'money_id',
        'receiver_person_id__person_name',
        'money_date',
        'money_amount',
        'money_payment_mode',
        'money_payment_details',
    ).annotate(total_money_amount_personwise=Sum('money_amount'))

    # total_money_amount = Money_Debit_Credit.objects.filter(pay_type_id__pay_type_name = 'salary').annotate(
    # money_amount_numeric=Cast('money_amount', FloatField())
    # ).aggregate(total_amount=Sum('money_amount_numeric'))['total_amount']


    persons_data = Person.objects.all().values('person_id', 'person_name', 'person_contact_number')

    return Response({
        "status": "success",
        "title": "Salary Details",
        "persons_data": persons_data,
        'money_data': money_transaction_data,
        # "total_money_amount": total_money_amount,
        "data": salary_details
    })


@api_view(['POST', 'GET'])
def insert_update_salary(request):
    persons_data = Person.objects.all().values('person_id', 'person_name')

    if request.method == 'POST':
        salary_id = request.data.get('salary_id')
        salary_date = request.data.get('salary_date')
        salary_amount = request.data.get('salary_amount')
        salary_working_days = request.data.get('salary_working_days')
        salary_details = request.data.get('salary_details')
        person_id = request.data.get('person_id')

        person_instance = Person.objects.get(person_id=person_id)

        if salary_id:
            salary = Salary.objects.get(salary_id=salary_id)
            salary.salary_date = salary_date
            salary.salary_amount = salary_amount
            salary.salary_working_days = salary_working_days
            salary.salary_details = salary_details
            salary.person_id = person_instance
            salary.save()
            message = "Salary record updated successfully."
            
        else:
            salary = Salary.objects.create(
                salary_date=salary_date,
                salary_amount=salary_amount,
                salary_working_days=salary_working_days,
                salary_details=salary_details,
                person_id=person_instance
            )
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
        print(total_amount)
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
        'machine_maintenance_person_id__person_name',
        'machine_maintenance_details',
        'machine_maintenance_types_id__maintenance_type_name',
        'project_id__project_name',
    )
    maintenance_types_data = Maintenance_Types.objects.all().values('maintenance_type_id', 'maintenance_type_name')
    machines_data = Machines.objects.all().values('machine_id', 'machine_name', 'machine_number_plate')
    maintenance_persons_data = Person.objects.filter(person_type_id__person_type_name = 'maintenance').values('person_id', 'person_name')
    driver_persons_data = Person.objects.filter(person_type_id__person_type_name = 'driver').values('person_id', 'person_name')
    projects_data = Project.objects.all().values('project_id', 'project_name')

    return Response({
        "status": "success",
        "title": "Maintenance",
        "maintenance_types_data": maintenance_types_data,
        "machines_data": machines_data,
        "persons_data": maintenance_persons_data,
        "driver_persons_data": driver_persons_data,
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
        machine_maintenance_driver_id = request.data.get('machine_maintenance_driver_id')
        machine_maintenance_person_id = request.data.get('machine_maintenance_person_id')
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
                "machine_maintenance_driver_id": maintenance_obj.machine_maintenance_driver_id.person_id,
                "machine_maintenance_person_id": maintenance_obj.machine_maintenance_person_id.person_id,
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
            machine_maintenance.machine_maintenance_date = machine_maintenance_date
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
                "machine_maintenance_driver_id": machine_maintenance.machine_maintenance_driver_id.person_id,
                "machine_maintenance_person_id": machine_maintenance.machine_maintenance_person_id.person_id,
                "machine_maintenance_details": machine_maintenance.machine_maintenance_details,
                "machine_maintenance_types_id": machine_maintenance.machine_maintenance_types_id.maintenance_type_id,
                "project_id": machine_maintenance.project_id.project_id if machine_maintenance.project_id else None,
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
    persons_data = Person.objects.all().values('person_name','person_contact_number','person_id')
    agent_persons = Person.objects.all().values('person_name','person_contact_number','person_id')

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

        project_amount = int(request.data.get('project_amount'))
        project_location = request.data.get('project_location')
        project_owner = request.data.get('project_owner_name')
        project_owner_instance = Person.objects.get(person_id = project_owner)
        project_status = request.data.get('project_status')
        project_cgst = request.data.get('project_cgst')
        project_sgst = request.data.get('project_sgst')
        project_tax = request.data.get('project_tax')
        project_discount = request.data.get('project_discount')
        project_types_id = int(request.data.get('project_types_id'))
        project_type_instance = Project_Types.objects.get(project_type_id=project_types_id)

        project_agent = request.data.get('project_agent')
        project_agent_id = request.data.get('project_agent_id')
        project_agent_type = request.data.get('project_agent_type')
        project_agent_percentage = request.data.get('project_agent_percentage')
        project_agent_fixed_amount = request.data.get('project_agent_fixed_amount')

        if project_agent_type == 'Percentage':
            project_final_amount = (((int(project_agent_percentage)/100) * project_amount) + project_amount)
       

        elif project_agent_type == 'Fixed':
            project_final_amount = (int(project_agent_fixed_amount) + project_amount)


        else:
            project_final_amount = project_amount


        if project_agent_id:
            agent_instance = Person.objects.get(person_id = project_agent_id)
        else:
            agent_instance = None
    
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
            project.project_final_amount = project_final_amount

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
                "project_agent_type": project.project_agent_type,
                "project_agent_percentage": project.project_agent_percentage,
                "project_agent_fixed_amount": project.project_agent_fixed_amount,
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
    material_types_data = Material_Types.objects.all().values('material_type_id', 'material_type_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    project_types_data = Project.objects.all().values('project_id', 'project_name')
    perons = Person.objects.all().values('person_id','person_name','person_contact_number')
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
            'material_status': material_obj.material_status,
            'material_buy_date': material_obj.material_buy_date,
            'material_buy_location': material_obj.material_buy_location,
            'material_work_type': material_obj.material_work_type.work_type_id,
            'material_work_no': material_obj.material_work_no,
            'material_price': material_obj.material_price,
            'material_total_price': material_obj.material_total_price,
            'material_is_agent': material_obj.material_is_agent,
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
        material_status = request.data.get('material_status')
        material_buy_date = request.data.get('material_buy_date')
        material_buy_location = request.data.get('material_buy_location')
        material_work_type = request.data.get('material_work_type')
        material_work_no = int(request.data.get('material_work_no'))
        material_price = int(request.data.get('material_price'))
        material_total_price = material_price * material_work_no
        material_is_agent = request.data.get('material_is_agent')
        material_agent_name = request.data.get('material_agent_name')
        material_agent_contact = request.data.get('material_agent_contact')
        material_agent_price_choice = request.data.get('material_agent_price_choice')
        material_agent_percentage = request.data.get('material_agent_percentage')
        if material_agent_percentage:
            material_agent_percentage = int(material_agent_percentage)
        material_agent_amount = request.data.get('material_agent_amount')
        if material_agent_price_choice == "Discount":
            material_agent_amount = material_total_price*material_agent_percentage/100
        
        if material_agent_amount:
            material_final_amount = material_total_price + material_agent_amount
        else:
            material_final_amount = material_total_price
        material_details = request.data.get('material_details')

        material_type_instance = Material_Types.objects.get(material_type_id=material_type_id)
        work_type_instance = Work_Types.objects.get(work_type_id=material_work_type)
        material_owner_instance = Person.objects.get(person_id=material_owner)

        if material_id:
            material = Material.objects.get(material_id=material_id)
            material.material_owner = material_owner_instance
            material.material_buy_date = material_buy_date
            material.material_buy_location = material_buy_location
            material.material_type_id = material_type_instance
            material.material_work_type = work_type_instance
            material.material_work_no = material_work_no
            material.material_price = material_price
            material.material_total_price = material_total_price
            material.material_is_agent = material_is_agent
            material.material_agent_name = material_agent_name
            material.material_agent_contact = material_agent_contact
            material.material_agent_price_choice = material_agent_price_choice
            material.material_agent_percentage = material_agent_percentage
            material.material_agent_amount = material_agent_amount
            material.material_final_amount = material_final_amount
            material.material_details = material_details
            material.material_status = material_status
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
                material_agent_name=material_agent_name,
                material_agent_contact=material_agent_contact,
                material_agent_price_choice=material_agent_price_choice,
                material_agent_percentage=material_agent_percentage,
                material_agent_amount=material_agent_amount,
                material_final_amount=material_final_amount,
                material_details=material_details,
                material_status=material_status,
                material_buy_location=material_buy_location,
            )
            message = "Material created successfully."

        return Response({
            "status": "success",
            "message": message,
            "data": {
                "material_id": material.material_id,
                "material_owner": material.material_owner.person_id,
                "material_buy_date": material.material_buy_date,
                "material_buy_location": material.material_buy_location,
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
        }

        return Response({"status": "success", "data": project_data,"title":project.project_name})
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
        'project_day_detail_work_no',
        'project_day_detail_price',
        'project_day_detail_total_price',
        'project_day_detail_details'
    )

    machine_data = Machines.objects.all().values('machine_id', 'machine_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')

    return Response({
        'status': 'success',
        'title': 'Project Day Details',
        'machines_data': machine_data,
        'work_types_data': work_types_data,
        'data': project_day_details_data,
        'total_amount': total_amount,
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
                    "project_day_detail_machine_id": project_day_detail.project_day_detail_machine_id.machine_id,
                    "project_day_detail_work_type": project_day_detail.project_day_detail_work_type.work_type_id,
                    "project_day_detail_work_no": project_day_detail.project_day_detail_work_no,
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

    if request.method == 'POST':
        project_day_detail_id = request.data.get('project_day_detail_id')
        proejct_day_detail_date = request.data.get('proejct_day_detail_date')
        project_day_detail_machine_id = request.data.get('project_day_detail_machine_id')
        project_day_detail_work_type = request.data.get('project_day_detail_work_type')
        project_day_detail_work_no = int(request.data.get('project_day_detail_work_no'))
        project_day_detail_price = int(request.data.get('project_day_detail_price'))
        project_day_detail_details = request.data.get('project_day_detail_details', '')
        project_id = request.data.get('project_id')

        machine_instance = get_object_or_404(Machines, pk=project_day_detail_machine_id)
        work_type_instance = get_object_or_404(Work_Types, pk=project_day_detail_work_type)
        project_instance = get_object_or_404(Project, pk=project_id)


        if project_day_detail_id:
            project_day_detail = get_object_or_404(Project_Day_Details, project_day_detail_id=project_day_detail_id)
            project_day_detail.proejct_day_detail_date = proejct_day_detail_date
            project_day_detail.project_day_detail_machine_id = machine_instance
            project_day_detail.project_day_detail_work_type = work_type_instance
            project_day_detail.project_day_detail_work_no = project_day_detail_work_no
            project_day_detail.project_day_detail_price = project_day_detail_price
            project_day_detail.project_day_detail_total_price = project_day_detail_work_no * project_day_detail_price
            project_day_detail.project_day_detail_details = project_day_detail_details
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
                project_day_detail_total_price=project_day_detail_work_no * project_day_detail_price,
                project_day_detail_details=project_day_detail_details,
                project_id = project_instance
            )
            message = "Project day detail created successfully"

        return Response({
            "status": "success",
            "message": message,
            "data": {
                "project_day_detail_id": project_day_detail.project_day_detail_id,
                "proejct_day_detail_date": project_day_detail.proejct_day_detail_date,
                "project_day_detail_machine_id": project_day_detail.project_day_detail_machine_id.machine_id,
                "project_day_detail_work_type": project_day_detail.project_day_detail_work_type.work_type_id,
                "project_day_detail_work_no": project_day_detail.project_day_detail_work_no,
                "project_day_detail_price": project_day_detail.project_day_detail_price,
                "project_day_detail_total_price": project_day_detail.project_day_detail_total_price,
                "project_day_detail_details": project_day_detail.project_day_detail_details,
            },
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
        'project_material_material_id__material_owner__person_id',
        'project_material_material_id__material_owner__person_name',
        'project_material_material_type_id__material_type_name',
        'project_material_work_type_id__work_type_name',
        'project_material_work_no',
        'project_material_price',
        'project_material_total_amount',
        'person_material_information'
    )

    materials_data = Material.objects.all().values('material_id', 'material_owner__person_name')
    material_types_data = Material_Types.objects.all().values('material_type_id', 'material_type_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    persons_data = Person.objects.all().values('person_id', 'person_name')

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
    materials_data = Material.objects.all().values('material_id', 'material_owner__person_name')
    material_types_data = Material_Types.objects.all().values('material_type_id', 'material_type_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    persons_data = Person.objects.all().values('person_id', 'person_name')
    
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
                    "project_material_material_id": project_material.project_material_material_id.material_id,
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
        project_id = request.data.get('project_id')
        material_instance = get_object_or_404(Material, pk=project_material_material_id)
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
            message = "Project material data created successfully"

        return Response({
            "status": "success",
            "message": message,
            "data": {
                "project_material_id": project_material.project_material_id,
                "project_material_date": project_material.project_material_date,
                "project_material_material_id": project_material.project_material_material_id.material_id,
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

    machines_data = Machines.objects.all().values('machine_id', 'machine_name','machine_number_plate')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')

    maintenance_types_data = Maintenance_Types.objects.all().values('maintenance_type_id', 'maintenance_type_name')
    machines_data = Machines.objects.all().values('machine_id', 'machine_name', 'machine_number_plate')
    maintenance_persons_data = Person.objects.filter(person_type_id__person_type_name = 'maintenance').values('person_id', 'person_name')
    driver_persons_data = Person.objects.filter(person_type_id__person_type_name = 'driver').values('person_id', 'person_name')
    projects_data = Project.objects.all().values('project_id', 'project_name')

    return Response({
        'status': 'success',
        'title': 'Project Machine',
        'machines_data': machines_data,
        'work_types_data': work_types_data,
        "maintenance_types_data": maintenance_types_data,
        "machines_data": machines_data,
        "persons_data": maintenance_persons_data,
        "driver_persons_data": driver_persons_data,
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
                },
                'machines_data': machines_data,
                'work_types_data': work_types_data,
            })
        return Response({
            "status": "error",
            "message": "Project machine ID not provided"
        }, status=400)

    if request.method == 'POST':
        project_machine_id = request.data.get('project_machine_data_id')
        project_machine_date = request.data.get('project_machine_date')
        machine_project_id = request.data.get('machine_project_id')
        work_type_id = request.data.get('work_type_id')
        project_machine_data_work_number = int(request.data.get('project_machine_data_work_number'))
        project_machine_data_work_price = int(request.data.get('project_machine_data_work_price'))
        project_machine_data_total_amount = project_machine_data_work_price * project_machine_data_work_number
        project_machine_data_work_details = request.data.get('project_machine_data_work_details')
        project_machine_data_more_details = request.data.get('project_machine_data_more_details')
        project_id = request.data.get('project_id')

        machine_instance = get_object_or_404(Machines, pk=machine_project_id)
        work_type_instance = get_object_or_404(Work_Types, pk=work_type_id)
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
                project_id = project_instance
            )
            message = "Project machine data created successfully"

        return Response({
            "status": "success",
            "message": message,
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
            },
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
        }


        total_amount = project_person_data.aggregate(total_amount=Sum('project_person_total_price'))['total_amount']
    else:
        project_data = None
        total_amount = project_person_data.aggregate(total_amount=Sum('project_person_total_price'))['total_amount']

    project_person_data = project_person_data.values(
        'project_person_id',
        'person_id__person_name',
        'project_person_date',
        'work_type_id__work_type_name',
        'project_machine_data_id__machine_project_id__machine_name',
        'project_machine_data_id__machine_project_id__machine_number_plate',
        'project_person_work_num',
        'project_person_price',
        'project_person_total_price',
        'project_person_paid_by',
        'project_person_payment_details','project_person_more_details'
        'project_person_payment_details',
        'project_person_more_details'
    )

    persons_data = Person.objects.all().values('person_id', 'person_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    project_machine_data = Project_Machine_Data.objects.all().values('project_machine_data_id', 'machine_project_id__machine_name')

    return Response({
        'status': 'success',
        'title': 'Project Person',
        'persons_data': persons_data,
        'work_types_data': work_types_data,
        'project_machine_data': project_machine_data,
        'data': project_person_data,
        'total_amount': total_amount,
        'project_data':project_data
    })



@api_view(['POST', 'GET'])
def insert_update_project_person(request):
    persons_data = Person.objects.all().values('person_id', 'person_name')
    work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
    project_machine_data = Project_Machine_Data.objects.all().values('project_machine_data_id', 'machine_project_id__machine_name')

    if request.method == 'GET':
        project_person_id = request.GET.get('getdata_id')
        if project_person_id:
            project_person = get_object_or_404(Project_Person_Data, pk=project_person_id)
            return Response({
                "status": "success",
                "message": "Project person data fetched successfully",
                "data": {
                    "project_person_id": project_person.project_person_id,
                    "person_id": project_person.person_id.person_id,
                    "project_person_date": project_person.project_person_date,
                    "work_type_id": project_person.work_type_id.work_type_id,
                    "project_machine_data_id": project_person.project_machine_data_id.project_machine_data_id,
                    "project_person_work_num": project_person.project_person_work_num,
                    "project_person_price": project_person.project_person_price,
                    "project_person_total_price": project_person.project_person_total_price,
                    "project_person_paid_by": project_person.project_person_paid_by,
                    "project_person_payment_details": project_person.project_person_payment_details,
                    "project_person_more_details": project_person.project_person_more_details,
                },
                'persons_data': persons_data,
                'work_types_data': work_types_data,
                'project_machine_data': project_machine_data,
            })
        return Response({
            "status": "error",
            "message": "Project person ID not provided"
        }, status=400)

    if request.method == 'POST':
        project_person_id = request.data.get('project_person_id')
        person_id = request.data.get('person_id')
        project_person_date = request.data.get('project_person_date')
        work_type_id = request.data.get('work_type_id')
        project_machine_data_id = request.data.get('project_machine_data_id')
        project_person_work_num = int(request.data.get('project_person_work_num'))
        project_person_price = int(request.data.get('project_person_price'))
        project_person_total_price = project_person_work_num * project_person_price
        project_person_paid_by = request.data.get('project_person_paid_by')
        project_person_payment_details = request.data.get('project_person_payment_details')
        project_person_more_details = request.data.get('project_person_more_details')
        project_id = request.data.get('project_id')

        person_instance = get_object_or_404(Person, pk=person_id)
        work_type_instance = get_object_or_404(Work_Types, pk=work_type_id)
        machine_instance = get_object_or_404(Project_Machine_Data, pk=project_machine_data_id)
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
                project_id = project_instance
            )
            message = "Project person data created successfully"

        return Response({
            "status": "success",
            "message": message,
            "data": {
                "project_person_id": project_person.project_person_id,
                "person_id": project_person.person_id.person_id,
                "project_person_date": project_person.project_person_date,
                "work_type_id": project_person.work_type_id.work_type_id,
                "project_machine_data_id": project_person.project_machine_data_id.project_machine_data_id,
                "project_person_work_num": project_person.project_person_work_num,
                "project_person_price": project_person.project_person_price,
                "project_person_total_price": project_person.project_person_total_price,
                "project_person_paid_by": project_person.project_person_paid_by,
                "project_person_payment_details": project_person.project_person_payment_details,
                "project_person_more_details": project_person.project_person_more_details,
            },
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
        'project_name'
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
        print("------------", request.GET.get('project_id'))
        project_expense_data = project_expense_data.filter(project_id__project_id = request.GET.get('project_id'))

        total_amount = project_expense_data.aggregate(
            total_amount=Sum('project_expense_amount')
        )['total_amount']
    else:
        total_amount = project_expense_data.aggregate(
            total_amount=Sum('project_expense_amount')
        )['total_amount']

    project_expense_data = Project_Expense.objects.all().values(
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
    banks_data = Bank_Details.objects.all().values('bank_id', 'bank_name')

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

    if request.method == 'POST':
        project_expense_id = request.data.get('project_expense_id')
        project_expense_name = request.data.get('project_expense_name')
        project_id = request.data.get('project_id')
        project_expense_date = request.data.get('project_expense_date')
        project_expense_amount = request.data.get('project_expense_amount')
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
        "message": "Invalid request method"
    }, status=405)


@api_view(['DELETE'])
def delete_project_expense(request):
    project_expense_id = request.GET.get('project_expense_id')

    if not project_expense_id:
        return Response({
            "status": "error",
            "message": "Project Expense ID is required."
        }, status=400)

    try:
        project_expense = get_object_or_404(Project_Expense, project_expense_id=project_expense_id)
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
    data = Documents.objects.all().values('document_name','document_id','document_date','document_unique_code','document_file')
    for document in data:
        document['document_file_url'] = domain + settings.MEDIA_URL + str(document['document_file'])
        document['data'] = 'hello'

    document_types = Document_Types.objects.all().values('document_type_name','document_type_id')
    return Response({
        'status':True,
        'message': 'Documents Fetched Successfully',
        'data':data,
        'document_types':document_types
    })

# GET, PUT, DELETE a single document
@api_view(['GET','POST', 'PUT', 'DELETE'])
def insert_update_documents(request):
    product_data = request.data
    form = DocumentsSerializer(data = product_data)

    if form.is_valid():
            form.save()
            return Response({
                'status': True,
                'message': 'Product has been added successfully'
            })
    else:
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")

            return Response({
                'status':False,
                'message': " ".join(error_messages)
            })


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
    
    bank_details_data = Bank_Details.objects.filter(person_id__person_name = 'Pinak Enterprise').values(
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
        date = request.data.get('date')
        details = request.data.get('details')

        if bank_id:
            bank_instance = Bank_Details.objects.get(bank_id=bank_id)
        else:
            bank_instance = None

        if bank_cash_id:
            bank_cash_data = bank_cash.objects.get(bank_cash_id=bank_cash_id)
            bank_cash_data.credit_debit = credit_debit
            bank_cash_data.amount = amount
            bank_cash_data.bank_id = bank_instance
            bank_cash_data.date = date
            bank_cash_data.details = details
            bank_cash_data.save()
            message = "Bank cash details updated successfully."

        else:
            bank_cash_data = bank_cash.objects.create(
                credit_debit=credit_debit,
                amount=amount,
                bank_id=bank_instance,
                date=date,
                details=details
            )
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
    data = language.objects.all().values('language_id','gujarati','english')

    settingss = Settingsss.objects.get(settings_field_name = 'language')

    
    if request.GET.get('language_change'):
        settingss.settings_field_value = request.GET.get('language_change')
        settingss.save()

    if settingss.settings_field_value == 'gujarati':
        for x in data:
            x['lang'] = x['gujarati']
    else:
        for x in data:
            x['lang'] = x['english']   


    return Response({
            "status": "success",
            "message": "Language Data Fetched Successfully.",
            'data':data,
            'currentlanguage':settingss.settings_field_value
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
    if request.GET.get('report_date'):
        today_date = request.GET.get('report_date')
        print("---", today_date)
    else:
        today_date = date.today()

    dailywise_credit_report = Money_Debit_Credit.objects.filter(money_date = today_date, receiver_person_id__person_name = 'Pinak Enterprise').values('sender_person_id__person_name', 'receiver_person_id__person_name', 'pay_type_id__pay_type_name', 'money_amount')

    x = Money_Debit_Credit.objects.filter(money_date = today_date, receiver_person_id__person_name = 'Pinak Enterprise').values('sender_person_id__person_name', 'receiver_person_id__person_name', 'pay_type_id__pay_type_name', 'money_amount').aggregate(total_amount_credit=Sum('money_amount'))
    total_credit_amount = x['total_amount_credit'] or 0 

    dailywise_debit_report = Money_Debit_Credit.objects.filter(money_date = today_date, sender_person_id__person_name = 'Pinak Enterprise').values('sender_person_id__person_name' , 'receiver_person_id__person_name', 'pay_type_id__pay_type_name', 'money_amount')

    y = Money_Debit_Credit.objects.filter(money_date = today_date, sender_person_id__person_name = 'Pinak Enterprise').values('sender_person_id__person_name' , 'receiver_person_id__person_name', 'pay_type_id__pay_type_name', 'money_amount').aggregate(total_amount=Sum('money_amount'))
    total_debit_amount = y['total_amount'] or 0


    return Response({
        'status': 'success',
        'title': 'Daily Reports',
        'dailywise_credit_report': dailywise_credit_report,
        'total_credit_amount': total_credit_amount,
        'dailywise_debit_report': dailywise_debit_report,
        'total_debit_amount': total_debit_amount
    })



    






























# @api_view(['GET'])
# def show_person_work_machine(request):
#     person_work_machine = Person_Work_Machine.objects.all().values(
#         'pwm_id',
#         'pwm_machine_name',
#         'pwm_machine_owner_name',
#         'pwm_machine_owner_number',
#         'working_machine_id__working_machine_name',
#         'pwm_person_joining_date',
#         'pwm_person_contact_number',
#         'pwm_person_payment_by',
#         'pwm_person_payment_desc',
#         'person_type_id__person_type_name',
#         'person_id__person_name',
#         'project_type_id__project_type_name',
#         'project_id__project_name',
#         'work_types_id__work_type_name',
#         'pwm_work_number',
#         'pwm_work_amount',
#         'pwm_total_amount',
#         'pwm_work_desc'
#     )
#     working_types_data = Working_Machines.objects.all().values('working_machine_id', 'working_machine_name')
#     person_types_data = Person_Type.objects.all().values('person_type_id', 'person_type_name')
#     person_data = Person.objects.all().values('person_id', 'person_name')
#     project_types_data = Project_Types.objects.all().values('project_type_id', 'project_type_name')
#     work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
#     project_data = Project.objects.all().values('project_id', 'project_name')
#     return Response({
#         "status": "success",
#         "title": "Person",
#         'working_types_data': working_types_data,
#         'person_types_data': person_types_data,
#         'person_data': person_data,
#         'work_types_data': work_types_data,
#         'project_types_data': project_types_data,
#         'project_data': project_data,
#         "data": person_work_machine,
#     })


# @api_view(['POST', 'GET'])
# def insert_update_person_work_machine(request):
#     working_types_data = Working_Machines.objects.all().values('working_machine_id', 'working_machine_name')
#     person_types_data = Person_Type.objects.all().values('person_type_id', 'person_type_name')
#     person_data = Person.objects.all().values('person_id', 'person_name')
#     project_types_data = Project_Types.objects.all().values('project_type_id', 'project_type_name')
#     work_types_data = Work_Types.objects.all().values('work_type_id', 'work_type_name')
#     project_data = Project.objects.all().values('project_id', 'project_name')

#     if request.method == 'POST':
#         pwm_id = request.data.get('pwm_id')
#         pwm_machine_name = request.data.get('pwm_machine_name')
#         pwm_machine_owner_name = request.data.get('pwm_machine_owner_name')
#         pwm_machine_owner_number = request.data.get('pwm_machine_owner_number')
#         working_machine_id = request.data.get('working_machine_id')
#         pwm_person_joining_date = request.data.get('pwm_person_joining_date')
#         pwm_person_contact_number = request.data.get('pwm_person_contact_number')
#         pwm_person_payment_by = request.data.get('pwm_person_payment_by')
#         pwm_person_payment_desc = request.data.get('pwm_person_payment_desc')
#         person_type_id = request.data.get('person_type_id')
#         person_id = request.data.get('person_id')
#         project_type_id = request.data.get('project_type_id')
#         project_id = request.data.get('project_id')
#         work_types_id = request.data.get('work_types_id')
#         pwm_work_number = request.data.get('pwm_work_number')
#         pwm_work_amount = request.data.get('pwm_work_amount')
#         pwm_total_amount = request.data.get('pwm_total_amount')
#         pwm_work_desc = request.data.get('pwm_work_desc')

#         working_machine_instance = Working_Machines.objects.get(pk=working_machine_id)
#         person_type_instance = Person_Type.objects.get(pk=person_type_id)
#         person_instance = Person.objects.get(pk=person_id)
#         project_type_instance = Project_Types.objects.get(pk=project_type_id)
#         project_instance = Project.objects.get(pk=project_id)
#         work_type_instance = Work_Types.objects.get(pk=work_types_id)

#     if request.GET.get('getdata_id'):
#         person_work_machine_obj = Person_Work_Machine.objects.get(pwm_id=request.GET.get('getdata_id'))
#         return Response({
#         "status": "success",
#         "message": 'Data Fetched Successfully',
#         "data": {
#             'pwm_id': person_work_machine_obj.pwm_id,
#             'pwm_machine_name': person_work_machine_obj.pwm_machine_name,
#             'pwm_machine_owner_name': person_work_machine_obj.pwm_machine_owner_name,
#             'pwm_machine_owner_number': person_work_machine_obj.pwm_machine_owner_number,
#             'working_machine_id': person_work_machine_obj.working_machine_id.working_machine_id,
#             'pwm_person_joining_date': person_work_machine_obj.pwm_person_joining_date,
#             'pwm_person_contact_number': person_work_machine_obj.pwm_person_contact_number,
#             'pwm_person_payment_by': person_work_machine_obj.pwm_person_payment_by,
#             'pwm_person_payment_desc': person_work_machine_obj.pwm_person_payment_desc,
#             'person_type_id': person_work_machine_obj.person_type_id.person_type_id,
#             'person_id': person_work_machine_obj.person_id.person_id,
#             'project_type_id': person_work_machine_obj.project_type_id.project_type_id,
#             'project_id': person_work_machine_obj.project_id.project_id,
#             'work_types_id': person_work_machine_obj.work_types_id.work_type_id,
#             'pwm_work_number': person_work_machine_obj.pwm_work_number,
#             'pwm_work_amount': person_work_machine_obj.pwm_work_amount,
#             'pwm_total_amount': person_work_machine_obj.pwm_total_amount,
#             'pwm_work_desc': person_work_machine_obj.pwm_work_desc,  
#         },
#         'working_types_data': working_types_data,
#         'person_types_data': person_types_data,
#         'person_data': person_data,
#         'work_types_data': work_types_data,
#         'project_types_data': project_types_data,
#         'project_data': project_data,
#         })


#     if request.method == 'POST':
#         if pwm_id:
#             pwm = Person_Work_Machine.objects.get(pwm_id=pwm_id)
#             pwm.pwm_machine_name = pwm_machine_name
#             pwm.pwm_machine_owner_name = pwm_machine_owner_name
#             pwm.pwm_machine_owner_number = pwm_machine_owner_number
#             pwm.working_machine_id = working_machine_instance
#             pwm.pwm_person_joining_date = pwm_person_joining_date
#             pwm.pwm_person_contact_number = pwm_person_contact_number
#             pwm.pwm_person_payment_by = pwm_person_payment_by
#             pwm.pwm_person_payment_desc = pwm_person_payment_desc
#             pwm.person_type_id = person_type_instance
#             pwm.person_id = person_instance
#             pwm.project_type_id = project_type_instance
#             pwm.project_id = project_instance
#             pwm.work_types_id = work_type_instance
#             pwm.pwm_work_number = pwm_work_number
#             pwm.pwm_work_amount = pwm_work_amount
#             pwm.pwm_total_amount = pwm_total_amount
#             pwm.pwm_work_desc = pwm_work_desc
#             pwm.save()
#             message = "Person Work Machine updated successfully."

#         else:
#             pwm = Person_Work_Machine.objects.create(
#                 pwm_machine_name=pwm_machine_name,
#                 pwm_machine_owner_name=pwm_machine_owner_name,
#                 pwm_machine_owner_number=pwm_machine_owner_number,
#                 working_machine_id=working_machine_instance,
#                 pwm_person_joining_date=pwm_person_joining_date,
#                 pwm_person_contact_number=pwm_person_contact_number,
#                 pwm_person_payment_by=pwm_person_payment_by,
#                 pwm_person_payment_desc=pwm_person_payment_desc,
#                 person_type_id=person_type_instance,
#                 person_id=person_instance,
#                 project_type_id=project_type_instance,
#                 project_id=project_instance,
#                 work_types_id=work_type_instance,
#                 pwm_work_number=pwm_work_number,
#                 pwm_work_amount=pwm_work_amount,
#                 pwm_total_amount=pwm_total_amount,
#                 pwm_work_desc=pwm_work_desc
#             )
#             message = "Person Work Machine created successfully."

#         return Response({
#             "status": "success",
#             "message": message,
#             "data": {
#                 "pwm_id": pwm.pwm_id,
#                 "pwm_machine_name": pwm.pwm_machine_name,
#                 "pwm_machine_owner_name": pwm.pwm_machine_owner_name,
#                 "pwm_machine_owner_number": pwm.pwm_machine_owner_number,
#                 "working_machine_id": pwm.working_machine_id.working_machine_id,
#                 "pwm_person_joining_date": pwm.pwm_person_joining_date,
#                 "pwm_person_contact_number": pwm.pwm_person_contact_number,
#                 "pwm_person_payment_by": pwm.pwm_person_payment_by,
#                 "pwm_person_payment_desc": pwm.pwm_person_payment_desc,
#                 "person_type_id": pwm.person_type_id.person_type_id,
#                 "person_id": pwm.person_id.person_id,
#                 "project_type_id": pwm.project_type_id.project_type_id,
#                 "project_id": pwm.project_id.project_id,
#                 "work_types_id": pwm.work_types_id.work_type_id,
#                 "pwm_work_number": pwm.pwm_work_number,
#                 "pwm_work_amount": pwm.pwm_work_amount,
#                 "pwm_total_amount": pwm.pwm_total_amount,
#                 "pwm_work_desc": pwm.pwm_work_desc
#             },
#             'working_types_data': working_types_data,
#             'person_types_data': person_types_data,
#             'person_data': person_data,
#             'work_types_data': work_types_data,
#             'project_types_data': project_types_data,
#             'project_data': project_data,
#         })
#     else:
#         return Response({
#             'status': 'False'
#         })

# @api_view(['DELETE'])
# def delete_person_work_machine(request):
#     pwm_id = request.GET.get('pwm_id')

#     if not pwm_id:
#         return Response({
#             "status": "error",
#             "message": "PWM ID is required."
#         }, status=400)

#     try:
#         pwm = Person_Work_Machine.objects.get(pwm_id=pwm_id)
#         pwm.delete()
#         return Response({
#             "status": "success",
#             "message": "Person Work Machine deleted successfully."
#         })
#     except Person_Work_Machine.DoesNotExist:
#         return Response({
#             "status": "error",
#             "message": "Person Work Machine not found."
#         }, status=404)
    

# @api_view(['GET'])
# def show_document_types(request):
#     document_types = Document_Types.objects.all().values(
#         'document_type_id',
#         'document_type_name'
#     )
#     return Response({
#         "status": "success",
#         "data": document_types
#     })


# @api_view(['POST', 'GET'])
# def insert_update_document_type(request):
#     document_type_id = request.data.get('document_type_id')
#     document_type_name = request.data.get('document_type_name')

#     if request.GET.get('getdata_id'):
#         document_type_obj = Document_Types.objects.get(document_type_id=request.GET.get('getdata_id'))
#         return Response({
#         "status": "success",
#         "message": 'Data Fetched Successfully',
#         "data": {
#             'document_type_id': document_type_obj.document_type_id,
#             'document_type_name': document_type_obj.document_type_name,               
#         }
#         })

#     if request.method == 'POST':
#         if document_type_id:
#                 document_type = Document_Types.objects.get(document_type_id=document_type_id)
#                 document_type.document_type_name = document_type_name
#                 document_type.save()
#                 message = "Document type updated successfully."
#         else:
#             document_type = Document_Types.objects.create(
#                 document_type_name=document_type_name
#             )
#             message = "Document type created successfully."

#         return Response({
#             "status": "success",
#             "message": message,
#             "data": {
#                 "document_type_id": document_type.document_type_id,
#                 "document_type_name": document_type.document_type_name
#             }
#         })
#     else:
#         return Response({
#             'status': 'False'
#         })

# @api_view(['DELETE'])
# def delete_document_type(request):
#     document_type_id = request.GET.get('document_type_id')

#     if not document_type_id:
#         return Response({
#             "status": "error",
#             "message": "Document type ID is required."
#         }, status=400)

#     try:
#         document_type = Document_Types.objects.get(document_type_id=document_type_id)
#         document_type.delete()
#         return Response({
#             "status": "success",
#             "message": "Document type deleted successfully."
#         })
#     except Document_Types.DoesNotExist:
#         return Response({
#             "status": "error",
#             "message": "Document type not found."
#         }, status=404)
    
# @api_view(['GET'])
# def show_documents(request):
#     documents = Documents.objects.all().values(
#         'document_id',
#         'document_name',
#         'document_date',
#         'document_unique_code',
#         'document_file',
#         'document_type_id',
#         'document_type_id__document_type_name'
#     )
#     return Response({
#         "status": "success",
#         "title": "Documents",
#         "data": documents
#     })


# @api_view(['POST'])
# def insert_update_document(request):
#     document_types_data = Document_Types.objects.all().values('document_type_id', 'document_type_name')
#     if request.method == 'POST':
#         document_id = request.data.get('document_id')
#         document_name = request.data.get('document_name')
#         document_unique_code = request.data.get('document_unique_code')
#         document_type_id = request.data.get('document_type_id')
#         document_file = request.FILES.get('document_file')
#         document_type = Document_Types.objects.get(document_type_id=document_type_id)
   
#     if request.GET.get('getdata_id'):
#         document_obj = Documents.objects.get(document_id=request.GET.get('getdata_id'))
#         return Response({
#         "status": "success",
#         "message": 'Data Fetched Successfully',
#         "data": {
#             'document_id': document_obj.document_id,
#             'document_name': document_obj.document_name,               
#             'document_date': document_obj.document_date,               
#             'document_unique_code': document_obj.document_unique_code,              
#             'document_file': document_obj.document_file,              
#             'document_type_id': document_obj.document_type_id,              
#         },
#         'document_types_data': document_types_data
#         })
    
#     if request.method == 'POST':
#         if document_id:
#                 document = Documents.objects.get(document_id=document_id)
#                 document.document_name = document_name
#                 document.document_unique_code = document_unique_code
#                 document.document_type_id = document_type
#                 if document_file:
#                     document.document_file = document_file
#                 document.save()
#                 message = "Document updated successfully."
#         else:
#             document = Documents.objects.create(
#                 document_name=document_name,
#                 document_unique_code=document_unique_code,
#                 document_type_id=document_type,
#                 document_file=document_file
#             )
#             message = "Document created successfully."

#         return Response({
#             "status": "success",
#             "message": message,
#             "data": {
#                 "document_id": document.document_id,
#                 "document_name": document.document_name,
#                 "document_date": document.document_date,
#                 "document_unique_code": document.document_unique_code,
#                 "document_file": document.document_file.url if document.document_file else None,
#                 "document_type_id": document.document_type_id.document_type_id,
#                 "document_type_name": document.document_type_id.document_type_name
#             },
#             'document_types_data': document_types_data
#         })
#     else:
#         return Response({
#             'status': 'False'
#         })


# @api_view(['DELETE'])
# def delete_document(request):
#     document_id = request.GET.get('document_id')

#     if not document_id:
#         return Response({
#             "status": "error",
#             "message": "Document ID is required."
#         }, status=400)

#     try:
#         document = Documents.objects.get(document_id=document_id)
#         document.delete()
#         return Response({
#             "status": "success",
#             "message": "Document deleted successfully."
#         })
#     except Documents.DoesNotExist:
#         return Response({
#             "status": "error",
#             "message": "Document not found."
#         }, status=404)
    



# @api_view(['DELETE'])
# def delete_working_machine(request):
#     working_machine_id = request.GET.get('working_machine_id')
#     if not working_machine_id:
#         return Response({
#             "status": "error",
#             "message": "Working machine ID is required."
#         }, status=400)

#     try:
#         working_machine = Working_Machines.objects.get(working_machine_id=working_machine_id)
#         working_machine.delete()
#         return Response({
#             "status": "success",
#             "message": "Working machine deleted successfully."
#         })
#     except Working_Machines.DoesNotExist:
#         return Response({
#             "status": "error",
#             "message": "Working machine not found."
#         }, status=404)