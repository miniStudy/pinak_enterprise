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
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('language_data', views.language_data, name='language_data'),
    path('show_user/', views.show_user, name='show_user'),
    path('user_login/', views.user_login, name='user_login'),
    path('insert_update_user/', views.insert_update_user, name='insert_update_user'),

    path('show_comapny_details/', views.show_comapny_details, name='show_comapny_details'),
    path('insert_update_comapny_detail/', views.insert_update_comapny_detail, name='insert_update_comapny_detail'),


    path('show_person_types/', views.show_person_types, name='show_person_types'),
    path('insert_update_person_type/', views.insert_update_person_type, name='insert_update_person_type'),
    path('delete_person_type/', views.delete_person_type, name='delete_person_type'),


    path('show_machine_types/', views.show_machine_types, name='show_machine_types'),
    path('insert_update_machine_type/', views.insert_update_machine_type, name='insert_update_machine_type'),
    path('delete_machine_type/', views.delete_machine_type, name='delete_machine_type'),


    path('show_project_types/', views.show_project_types, name='show_project_types'),
    path('insert_update_project_type/', views.insert_update_project_type, name='insert_update_project_type'),
    path('delete_project_type/', views.delete_project_type, name='delete_project_type'),


    path('show_work_types/', views.show_work_types, name='show_work_types'),
    path('insert_update_work_type/', views.insert_update_work_type, name='insert_update_work_type'),
    path('delete_work_type/', views.delete_work_type, name='delete_work_type'),

# ================================
    path('show_office_kharch_types/', views.show_office_kharch_types, name='show_office_kharch_types'),
    path('insert_update_office_kharch_types/', views.insert_update_office_kharch_types, name='insert_update_office_kharch_types'),
    path('delete_office_kharch_types/', views.delete_office_kharch_types, name='delete_office_kharch_types'),


    path('show_material_types/', views.show_material_types, name='show_material_types'),
    path('insert_update_material_type/', views.insert_update_material_type, name='insert_update_material_type'),
    path('delete_material_type/', views.delete_material_type, name='delete_material_type'),


    path('show_maintenance_types/', views.show_maintenance_types, name='show_maintenance_types'),
    path('insert_update_maintenance_type/', views.insert_update_maintenance_type, name='insert_update_maintenance_type'),
    path('delete_maintenance_type/', views.delete_maintenance_type, name='delete_maintenance_type'),


    path('show_pay_types/', views.show_pay_types, name='show_pay_types'),
    path('insert_update_pay_type/', views.insert_update_pay_type, name='insert_update_pay_type'),
    path('delete_pay_type/', views.delete_pay_type, name='delete_pay_type'),


    path('show_persons/', views.show_persons, name='show_persons'),
    path('insert_update_person/', views.insert_update_person, name='insert_update_person'),
    path('delete_person/', views.delete_person, name='delete_person'),


    path('show_bank_details/', views.show_bank_details, name='show_bank_details'),
    path('insert_update_bank_detail/', views.insert_update_bank_detail, name='insert_update_bank_detail'),
    path('delete_bank_detail/', views.delete_bank_detail, name='delete_bank_detail'),


    path('show_machines/', views.show_machines, name='show_machines'),
    path('insert_update_machine/', views.insert_update_machine, name='insert_update_machine'),
    path('delete_machine/', views.delete_machine, name='delete_machine'),

    path('show_money_debit_credit/', views.show_money_debit_credit, name='show_money_debit_credit'),
    path('insert_update_money_debit_credit/', views.insert_update_money_debit_credit, name='insert_update_money_debit_credit'),
    path('delete_money_debit_credit/', views.delete_money_debit_credit, name='delete_money_debit_credit'),


    path('show_salary/', views.show_salary, name='show_salary'),
    path('insert_update_salary/', views.insert_update_salary, name='insert_update_salary'),
    path('delete_salary/', views.delete_salary, name='delete_salary'),


    path('show_machine_maintenance/', views.show_machine_maintenance, name='show_machine_maintenance'),
    path('insert_update_machine_maintenance/', views.insert_update_machine_maintenance, name='insert_update_machine_maintenance'),
    path('delete_machine_maintenance/', views.delete_machine_maintenance, name='delete_machine_maintenance'),


    path('show_projects/', views.show_projects, name='show_projects'),
    path('insert_update_project/', views.insert_update_project, name='insert_update_project'),
    path('delete_project/', views.delete_project, name='delete_project'),


    path('show_materials/', views.show_materials, name='show_materials'),
    path('insert_update_material/', views.insert_update_material, name='insert_update_material'),
    path('delete_material/', views.delete_material, name='delete_material'),

    path('material_owner_list/',views.material_owner_list_create, name="material_owner_list_create"),
    path('material_owner_update/',views.material_owner_update_delete, name="material_owner_update_delete"),



    path('show_project_day_details/', views.show_project_day_details, name='show_project_day_details'),
    path('insert_update_project_day_detail/', views.insert_update_project_day_detail, name='insert_update_project_day_detail'),
    path('delete_project_day_detail/', views.delete_project_day_detail, name='delete_project_day_detail'),

    path('show_project_material/', views.show_project_material, name='show_project_material'),
    path('insert_update_project_material/', views.insert_update_project_material, name='insert_update_project_material'),
    path('delete_project_material/', views.delete_project_material, name='delete_project_material'),


    path('show_project_machine/', views.show_project_machine, name='show_project_machine'),
    path('insert_update_project_machine/', views.insert_update_project_machine, name='insert_update_project_machine'),
    path('delete_project_machine/', views.delete_project_machine, name='delete_project_machine'),


    path('show_project_person/', views.show_project_person, name='show_project_person'),
    path('insert_update_project_person/', views.insert_update_project_person, name='insert_update_project_person'),
    path('delete_project_person/', views.delete_project_person, name='delete_project_person'),


    path('show_project_expense/', views.show_project_expense, name='show_project_expense'),
    path('insert_update_project_expense/', views.insert_update_project_expense, name='insert_update_project_expense'),
    path('delete_project_expense/', views.delete_project_expense, name='delete_project_expense'),
    

    path('single_project_data/',views.single_project_data, name='single_project_data'),


    path('show_reports/', views.show_reports, name='show_reports'),

    path('show_documents/', views.show_documents, name='show_documents'),
    path('insert_update_documents/', views.insert_update_documents, name='insert_update_documents'),
    
    
    path('insert_document_date/', views.insert_document_date, name='insert_document_date'),
    path('delete_document_date/', views.delete_document_date, name='delete_document_date'),


    path('show_bank_cash/', views.show_bank_cash, name='show_bank_cash'),
    path('insert_update_bank_cash/', views.insert_update_bank_cash, name='insert_update_bank_cash'),
    path('delete_bank_cash/', views.delete_bank_cash, name='delete_bank_cash'),

    path('show_daily_report/', views.show_daily_report, name='show_daily_report'),
    path('show_material_report/', views.show_material_report, name='show_material_report'),
    path('show_person_report/', views.show_person_report, name='show_person_report'),


    path('show_diary/', views.show_diary, name='show_diary'),
    path('insert_update_diary/', views.insert_update_diary, name='insert_update_diary'),
    path('delete_diary/', views.delete_diary, name='delete_diary'),

    path('show_machine_rent/',views.show_machine_rent, name='show_machine_rent'),
    path('insert_update_machine_rent/',views.insert_update_machine_rent, name='insert_update_machine_rent'),
    path('delete_machine_rent/', views.delete_machine_rent,name='delete_machine_rent'),
    
    path('show_bill/',views.show_bill, name='show_bill'),
    path('overall_report/',views.overall_report, name='overall_report'),
    path('machine_report/',views.machine_report, name='machine_report'),
    path('person_report/',views.person_report, name='person_report'),
    path('person_bhaththu_report/',views.person_bhaththu_report, name='person_bhaththu_report'),
    path('rokad_cash_calculation/',views.rokad_cash_calculation, name="rokad_cash_calculation"),

    path('bank_credit_report/',views.bank_credit_report, name='bank_credit_report'),
    path('bank_debit_report/',views.bank_debit_report, name='bank_debit_report'),
    path('persons_list/',views.persons_list, name='persons_list'),
    path('machines_list/',views.machines_list, name='machines_list'),


    











    # path('show_working_machines/', views.show_working_machines, name='show_working_machines'),
    # path('insert_update_working_machine/', views.insert_update_working_machine, name='insert_update_working_machine'),
    # path('delete_working_machine/', views.delete_working_machine, name='delete_working_machine'),

    # path('show_person_work_machine/', views.show_person_work_machine, name='show_person_work_machine'),
    # path('insert_update_person_work_machine/', views.insert_update_person_work_machine, name='insert_update_person_work_machine'),
    # path('delete_person_work_machine/', views.delete_person_work_machine, name='delete_person_work_machine'),

    # path('show_materials/', views.show_materials, name='show_materials'),
    # path('insert_update_material/', views.insert_update_material, name='insert_update_material'),
    # path('delete_material/', views.delete_material, name='delete_material'),

    # path('show_document_types/', views.show_document_types, name='show_document_types'),
    # path('insert_update_document_type/', views.insert_update_document_type, name='insert_update_document_type'),
    # path('delete_document_type/', views.delete_document_type, name='delete_document_type'),

    # path('show_documents/', views.show_documents, name='show_documents'),
    # path('insert_update_document/', views.insert_update_document, name='insert_update_document'),
    # path('delete_document/', views.delete_document, name='delete_document'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)