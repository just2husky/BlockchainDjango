"""BlockchainDjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from . import view
from .controller import login_controller
from .controller.block_chain_controller import BlockChainController
from .controller.patient_manager_controller import PatientManagerController
from .controller.doctor_manager_controller import DoctorManagerController
from .controller.medical_record_controller import MedicalRecordController
"""
Django url() 可以接收四个参数，分别是两个必选参数：regex、view 和两个可选参数：kwargs、name，接下来详细介绍这四个参数。
regex: 正则表达式，与之匹配的 URL 会执行对应的第二个参数 view。
view: 用于执行与正则表达式匹配的 URL 请求。
kwargs: 视图使用的字典类型的参数。
name: 用来反向获取 URL
"""
urlpatterns = [
    url(r'^hello$', view.hello),

    url(r'^log-page$', login_controller.log_page),
    url(r'^login$', login_controller.login),
    url(r'^logout$', login_controller.logout),

    url(r'^blockchain-manager$', BlockChainController.manager),
    url(r'^blockchain-init$', BlockChainController.init),

    url(r'^to-add-patient$', BlockChainController.to_add_patient),
    url(r'^add-patient$', BlockChainController.add_patient),
    url(r'^find-patient$', BlockChainController.find_patient),

    url(r'^add-doctor$', BlockChainController.add_doctor),
    url(r'^to-add-doctor$', BlockChainController.to_add_doctor),
    url(r'^find-doctor$', BlockChainController.find_doctor),

    url(r'^to-add-medical-record$', BlockChainController.to_add_medical_record),
    url(r'^add-medical-record$', BlockChainController.add_medical_record),

    url(r'^del-medical-record$', MedicalRecordController.del_medical_record),
    url(r'^to-update-medical-record$', MedicalRecordController.to_update_medical_record),
    url(r'^update-medical-record$', MedicalRecordController.update_medical_record),

    url(r'^to-patient-manager$', PatientManagerController.to_patient_manager),
    url(r'^get-patient-records$', PatientManagerController.get_patient_records),
    url(r'^get-patient-del-records$', PatientManagerController.get_patient_del_records),

    url(r'^to-doctor-manager$', DoctorManagerController.to_doctor_manager),
    url(r'^get-doctor-records$', DoctorManagerController.get_doctor_records),
    url(r'^get-doctor-del-records$', DoctorManagerController.get_doctor_del_records),
]
