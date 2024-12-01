"""pinak URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from pinak_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('show_comapny_details/', views.show_comapny_details, name='show_comapny_details'),
    path('insert_update_comapny_detail/', views.insert_update_comapny_detail, name='insert_update_comapny_detail'),

    path('show_bank_details/', views.show_bank_details, name='show_bank_details'),
    path('insert_update_bank_detail/', views.insert_update_bank_detail, name='insert_update_bank_detail'),
    path('delete_bank_detail/', views.delete_bank_detail, name='delete_bank_detail'),

    path('show_machine_types/', views.show_machine_types, name='show_machine_types'),
    path('insert_update_machine_type/', views.insert_update_machine_type, name='insert_update_machine_type'),
    path('delete_machine_type/', views.delete_machine_type, name='delete_machine_type'),

    path('show_company_machines/', views.show_company_machines, name='show_company_machines'),
    path('insert_update_company_machine/', views.insert_update_company_machine, name='insert_update_company_machine'),
    path('delete_company_machine/', views.delete_company_machine, name='delete_company_machine'),

    path('show_working_machines/', views.show_working_machines, name='show_working_machines'),
    path('insert_update_working_machine/', views.insert_update_working_machine, name='insert_update_working_machine'),
    path('delete_working_machine/', views.delete_working_machine, name='delete_working_machine'),

    path('show_maintenance_types/', views.show_maintenance_types, name='show_maintenance_types'),
    path('insert_update_maintenance_type/', views.insert_update_maintenance_type, name='insert_update_maintenance_type'),
    path('delete_maintenance_type/', views.delete_maintenance_type, name='delete_maintenance_type'),

    path('show_machine_maintenance/', views.show_machine_maintenance, name='show_machine_maintenance'),
    path('insert_update_machine_maintenance/', views.insert_update_machine_maintenance, name='insert_update_machine_maintenance'),
    path('delete_machine_maintenance/', views.delete_machine_maintenance, name='delete_machine_maintenance'),

    path('show_project_types/', views.show_project_types, name='show_project_types'),
    path('insert_update_project_type/', views.insert_update_project_type, name='insert_update_project_type'),
    path('delete_project_type/', views.delete_project_type, name='delete_project_type'),

    path('show_projects/', views.show_projects, name='show_projects'),
    path('insert_update_project/', views.insert_update_project, name='insert_update_project'),
    path('delete_project/', views.delete_project, name='delete_project'),

    path('show_pay_types/', views.show_pay_types, name='show_pay_types'),
    path('insert_update_pay_type/', views.insert_update_pay_type, name='insert_update_pay_type'),
    path('delete_pay_type/', views.delete_pay_type, name='delete_pay_type'),

    path('show_person_types/', views.show_person_types, name='show_person_types'),
    path('insert_update_person_type/', views.insert_update_person_type, name='insert_update_person_type'),
    path('delete_person_type/', views.delete_person_type, name='delete_person_type'),

    path('show_persons/', views.show_persons, name='show_persons'),
    path('insert_update_person/', views.insert_update_person, name='insert_update_person'),
    path('delete_person/', views.delete_person, name='delete_person'),

    path('show_work_types/', views.show_work_types, name='show_work_types'),
    path('insert_update_work_type/', views.insert_update_work_type, name='insert_update_work_type'),
    path('delete_work_type/', views.delete_work_type, name='delete_work_type'),

    path('show_person_work_machine/', views.show_person_work_machine, name='show_person_work_machine'),
    path('insert_update_person_work_machine/', views.insert_update_person_work_machine, name='insert_update_person_work_machine'),
    path('delete_person_work_machine/', views.delete_person_work_machine, name='delete_person_work_machine'),

    path('show_material_types/', views.show_material_types, name='show_material_types'),
    path('insert_update_material_type/', views.insert_update_material_type, name='insert_update_material_type'),
    path('delete_material_type/', views.delete_material_type, name='delete_material_type'),

    path('show_materials/', views.show_materials, name='show_materials'),
    path('insert_update_material/', views.insert_update_material, name='insert_update_material'),
    path('delete_material/', views.delete_material, name='delete_material'),

    path('show_document_types/', views.show_document_types, name='show_document_types'),
    path('insert_update_document_type/', views.insert_update_document_type, name='insert_update_document_type'),
    path('delete_document_type/', views.delete_document_type, name='delete_document_type'),

    path('show_documents/', views.show_documents, name='show_documents'),
    path('insert_update_document/', views.insert_update_document, name='insert_update_document'),
    path('delete_document/', views.delete_document, name='delete_document'),
]
