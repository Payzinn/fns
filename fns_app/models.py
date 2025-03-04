from django.db import models
from django.utils import timezone
import uuid

def xml_upload_path(instance, filename):
    return f'xml_files/{timezone.now().strftime("%Y%m%d_%H%M%S")}_{filename}'

def pdf_upload_path(instance, filename):
    return f'pdf_files/{timezone.now().strftime("%Y%m%d_%H%M%S")}_{filename}'

class TaxDocument(models.Model):
    name_organ = models.CharField(max_length=1000)  
    inn_organ = models.CharField(max_length=10)  
    kpp_organ = models.CharField(max_length=9)      
    ogrn_organ = models.CharField(max_length=13)   
    nal_per_mes_god = models.CharField(max_length=255)  
    name_org_akt = models.CharField(max_length=255)     
    date_prin_akt = models.DateField()                 
    nom_akt = models.CharField(max_length=50, null=True)  
    date_opub_akt = models.DateField()                   
    date_vstyp_akt = models.DateField()                  
    name_object = models.CharField(max_length=2000, null=True)  
    desc_nal_stav = models.CharField(max_length=1)              
    tax_rate = models.DecimalField(max_digits=16, decimal_places=6, null=True)  
    measure = models.CharField(max_length=1, null=True)         
    per_nal_stav = models.CharField(max_length=1, null=True)   
    category_nal_lgot = models.CharField(max_length=2000, null=True)  
    sved_nal_lgot = models.CharField(max_length=1)                   
    content_nl = models.CharField(max_length=2000, null=True)         
    category_nal_vych = models.CharField(max_length=2000, null=True)  
    sved_nal_vych = models.CharField(max_length=1)                    
    size_nv = models.CharField(max_length=255, null=True)             
    sv_osob_opr = models.CharField(max_length=4, null=True)   
    sv_data_nach = models.CharField(max_length=4, null=True)  
    sv_otm_upl = models.CharField(max_length=4, null=True)    
    kod_ust_srok = models.CharField(max_length=1)            
    ust_srok = models.CharField(max_length=50)               
    id_doc = models.CharField(max_length=50, unique=True, editable=False)  
    type_doc = models.CharField(max_length=1)                 
    type_nal = models.CharField(max_length=1)                 
    type_inf_doc = models.CharField(max_length=1)             
    any_inf = models.CharField(max_length=5000, null=True)    
    id_file = models.CharField(max_length=50, unique=True, editable=False) 
    version = models.CharField(max_length=10)                
    type_inf_file = models.CharField(max_length=50)           
    pre_vers = models.CharField(max_length=40, null=True)     
    kol_doc = models.IntegerField()                           
    nal_period = models.CharField(max_length=255)             
    surname = models.CharField(max_length=60)                
    name = models.CharField(max_length=60)                    
    patronymic = models.CharField(max_length=60, null=True)   
    id_org = models.CharField(max_length=10, null=True)      
    reason_code = models.CharField(max_length=9, null=True)   
    reg_number = models.CharField(max_length=13, null=True)   
    code_ssrf = models.CharField(max_length=2, null=True)     
    code_orktmo = models.CharField(max_length=11, null=True) 
    code_ksono = models.CharField(max_length=4, null=True)    
    code_knd = models.CharField(max_length=2, null=True)     
    date_mg = models.CharField(max_length=7, null=True)       
    date_full = models.CharField(max_length=10, null=True)    
    pdf_file = models.FileField(upload_to='pdf_files/', null=True, blank=True)  
    xml_file = models.FileField(upload_to='xml_files/', null=True, blank=True)  

    def save(self, *args, **kwargs):
            if not self.id_doc:
                self.id_doc = f"doc-uuid-{uuid.uuid4().hex[:10]}"
            if not self.id_file:
                self.id_file = f"file-uuid-{uuid.uuid4().hex[:10]}"
            super().save(*args, **kwargs)

    class Meta:
        db_table = 'tax_documents'