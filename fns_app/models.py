from django.db import models
from django.utils import timezone
import uuid

def xml_upload_path(instance, filename):
    return f'xml_files/{timezone.now().strftime("%Y%m%d_%H%M%S")}_{filename}'

def pdf_upload_path(instance, filename):
    return f'pdf_files/{timezone.now().strftime("%Y%m%d_%H%M%S")}_{filename}'

class TaxDocument(models.Model):
    fio = models.CharField(max_length=180, null=True, blank=True)
    knd = models.CharField(max_length=10, null=True, blank=True)
    doc_date = models.DateField(null=True, blank=True) 
    name_organ = models.CharField(max_length=1000, null=True, blank=True)
    inn_organ = models.CharField(max_length=10, null=True, blank=True)
    kpp_organ = models.CharField(max_length=9, null=True, blank=True)
    ogrn_organ = models.CharField(max_length=13, null=True, blank=True)
    nal_per_mes_god = models.CharField(max_length=255, null=True, blank=True)
    name_org_akt = models.CharField(max_length=255, null=True, blank=True)
    date_prin_akt = models.DateField(null=True, blank=True)
    nom_akt = models.CharField(max_length=50, null=True, blank=True)
    date_opub_akt = models.DateField(null=True, blank=True)
    date_vstyp_akt = models.DateField(null=True, blank=True)
    name_object = models.CharField(max_length=2000, null=True, blank=True)
    desc_nal_stav = models.CharField(max_length=1, null=True, blank=True)
    tax_rate = models.DecimalField(max_digits=16, decimal_places=6, null=True, blank=True)
    measure = models.CharField(max_length=1, null=True, blank=True)
    per_nal_stav = models.CharField(max_length=1, null=True, blank=True)
    oktmo_code = models.CharField(max_length=11, null=True, blank=True)  
    category_nal_lgot = models.CharField(max_length=2000, null=True, blank=True)
    sved_nal_lgot = models.CharField(max_length=1, null=True, blank=True)
    content_nl = models.CharField(max_length=2000, null=True, blank=True)
    category_nal_vych = models.CharField(max_length=2000, null=True, blank=True)
    sved_nal_vych = models.CharField(max_length=1, null=True, blank=True)
    size_nv = models.CharField(max_length=255, null=True, blank=True)
    sv_osob_opr = models.CharField(max_length=4, null=True, blank=True)
    sv_data_nach = models.CharField(max_length=4, null=True, blank=True)
    sv_otm_upl = models.CharField(max_length=4, null=True, blank=True)
    kod_ust_srok = models.CharField(max_length=1, null=True, blank=True)
    ust_srok = models.CharField(max_length=50, null=True, blank=True)
    type_inf_doc = models.CharField(max_length=1, null=True, blank=True)
    type_nal = models.CharField(max_length=1, null=True, blank=True)
    type_inf = models.CharField(max_length=1, null=True, blank=True) 
    any_inf = models.CharField(max_length=5000, null=True, blank=True)
    nal_period = models.CharField(max_length=255, null=True, blank=True)
    code_ssrf = models.CharField(max_length=2, null=True, blank=True)
    code_orktmo = models.CharField(max_length=11, null=True, blank=True)
    code_ksono = models.CharField(max_length=4, null=True, blank=True)
    code_knd = models.CharField(max_length=2, null=True, blank=True)
    date_mg = models.CharField(max_length=7, null=True, blank=True)    
    date_full = models.CharField(max_length=10, null=True, blank=True) 
    id_file = models.CharField(max_length=255, unique=True, null=True, blank=True)
    id_doc = models.CharField(max_length=255, unique=True, null=True, blank=True)
    pdf_file = models.FileField(upload_to=pdf_upload_path, null=True, blank=True)
    xml_file = models.FileField(upload_to=xml_upload_path, null=True, blank=True)

    def save(self, *args, **kwargs):
            if not self.id_doc:
                self.id_doc = f"doc-uuid-{uuid.uuid4().hex[:10]}"
            if not self.id_file:
                self.id_file = f"file-uuid-{uuid.uuid4().hex[:10]}"
            super().save(*args, **kwargs)
            
    class Meta:
        db_table = 'tax_documents'
