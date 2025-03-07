import os
from django.shortcuts import render, redirect
from .models import TaxDocument
from decimal import Decimal
import xml.etree.ElementTree as ET
from datetime import datetime
from django.utils import timezone
from xml.dom import minidom
from django.core.files import File
from io import BytesIO

def submit_form(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        tax_doc = TaxDocument()
        if data.get('fio'):
            tax_doc.fio = data['fio']
        if data.get('knd'):
            tax_doc.knd = data['knd']
        if data.get('docDate'):
            tax_doc.doc_date = data['docDate']
        if data.get('NameOrgan'):
            tax_doc.name_organ = data['NameOrgan']
        if data.get('INNOrgan'):
            tax_doc.inn_organ = data['INNOrgan']
        if data.get('KPPOrgan'):
            tax_doc.kpp_organ = data['KPPOrgan']
        if data.get('OGRNOrgan'):
            tax_doc.ogrn_organ = data['OGRNOrgan']
        if data.get('NalPerMesGod'):
            tax_doc.nal_per_mes_god = data['NalPerMesGod']
        if data.get('NameOrgAkt'):
            tax_doc.name_org_akt = data['NameOrgAkt']
        if data.get('DatePrinAkt'):
            tax_doc.date_prin_akt = data['DatePrinAkt']
        if data.get('NomAkt'):
            tax_doc.nom_akt = data['NomAkt']
        if data.get('DateOpubAkt'):
            tax_doc.date_opub_akt = data['DateOpubAkt']
        if data.get('DateVstypAkt'):
            tax_doc.date_vstyp_akt = data['DateVstypAkt']
        if data.get('NameObject'):
            tax_doc.name_object = data['NameObject']
        if data.get('DescNalStav') and data.get('DescNalStav') != 'none':
            tax_doc.desc_nal_stav = data['DescNalStav']
        if data.get('taxRate'):
            tax_doc.tax_rate = Decimal(data['taxRate'])
        if data.get('measure'):
            tax_doc.measure = data['measure']
        if data.get('PerNalStav') and data.get('PerNalStav') != 'none':
            tax_doc.per_nal_stav = data['PerNalStav']
        if data.get('CodeORKTMO'):
            tax_doc.oktmo_code = data['CodeORKTMO']
        if data.get('CategoryNalLgot'):
            tax_doc.category_nal_lgot = data['CategoryNalLgot']
        if data.get('SvedNalLgot') and data.get('SvedNalLgot') != 'none':
            tax_doc.sved_nal_lgot = data['SvedNalLgot']
        if data.get('ContentNL'):
            tax_doc.content_nl = data['ContentNL']
        if data.get('CategoryNalVych'):
            tax_doc.category_nal_vych = data['CategoryNalVych']
        if data.get('SvedNalVych') and data.get('SvedNalVych') != 'none':
            tax_doc.sved_nal_vych = data['SvedNalVych']
        if data.get('SizeNV'):
            tax_doc.size_nv = data['SizeNV']
        if data.get('SvOsobOpr'):
            tax_doc.sv_osob_opr = data['SvOsobOpr']
        if data.get('SvDataNach'):
            tax_doc.sv_data_nach = data['SvDataNach']
        if data.get('SvOtmUpl'):
            tax_doc.sv_otm_upl = data['SvOtmUpl']
        if data.get('KodUstSrok') and data.get('KodUstSrok') != 'none':
            tax_doc.kod_ust_srok = data['KodUstSrok']
        if data.get('UstSrok'):
            tax_doc.ust_srok = data['UstSrok']
        if data.get('TypeInfDoc'):
            tax_doc.type_inf_doc = data['TypeInfDoc']
        if data.get('TypeNal'):
            tax_doc.type_nal = data['TypeNal']
        if data.get('TypeInf'):
            tax_doc.type_inf = data['TypeInf']
        if data.get('AnyInf'):
            tax_doc.any_inf = data['AnyInf']
        if data.get('NalPeriod'):
            tax_doc.nal_period = data['NalPeriod']
        if data.get('CodeSSRF'):
            tax_doc.code_ssrf = data['CodeSSRF']
        if data.get('CodeORKTMO'):
            tax_doc.code_orktmo = data['CodeORKTMO']
        if data.get('CodeKSONO'):
            tax_doc.code_ksono = data['CodeKSONO']
        if data.get('CodeKND'):
            tax_doc.code_knd = data['CodeKND']
        if data.get('date-mg'):
            tax_doc.date_mg = data['date-mg']
        if data.get('date'):
            tax_doc.date_full = data['date']
        if files.get('pdf_file'):
            tax_doc.pdf_file = files['pdf_file']
        tax_doc.save()

        root = ET.Element("Файл")
        if tax_doc.id_file:
            root.set("ИдФайл", tax_doc.id_file)
        if data.get('PreVers'):
            root.set("ВерсПрог", data['PreVers'])

        opis_per_sved = ET.SubElement(root, "ОписПерСвед")
        if data.get('CodeKND'):
            opis_per_sved.set("КНД", data['CodeKND'])
        if data.get('date'):
            doc_date = datetime.strptime(data['date'], '%d.%m.%Y').strftime('%d.%m.%Y')
            opis_per_sved.set("ДатаДок", doc_date)

        sv_org_reg = ET.SubElement(root, "СвОргРег")
        if data.get('NameOrgan'):
            sv_org_reg.set("НаимОрг", data['NameOrgan'])
        if data.get('INNOrgan'):
            sv_org_reg.set("ИННЮЛ", data['INNOrgan'])
        if data.get('KPPOrgan'):
            sv_org_reg.set("КПП", data['KPPOrgan'])
        if data.get('OGRNOrgan'):
            sv_org_reg.set("ОГРН", data['OGRNOrgan'])

        doc = ET.SubElement(root, "Документ")
        if tax_doc.id_doc:
            doc.set("ИдДок", tax_doc.id_doc)
        if data.get('TypeNal'):
            doc.set("ВидНал", data['TypeNal'])
        if data.get('TypeInfDoc'):
            doc.set("ВидИнф", data['TypeInfDoc'])
        if data.get('AnyInf'):
            doc.set("ИнаяИнф", data['AnyInf'])

        sv_akt = ET.SubElement(doc, "СвАкт")
        if data.get('NalPerMesGod'):
            sv_akt.set("ВидАкт", data['NalPerMesGod'])
        if data.get('NameOrgAkt'):
            sv_akt.set("НаимОргАкт", data['NameOrgAkt'])
        if data.get('DatePrinAkt'):
            date_prin_akt = datetime.strptime(data['DatePrinAkt'], '%Y-%m-%d').strftime('%d.%m.%Y')
            sv_akt.set("ДатаПринАкт", date_prin_akt)
        if data.get('NomAkt'):
            sv_akt.set("НомАкт", data['NomAkt'])
        if data.get('DateOpubAkt'):
            date_opub_akt = datetime.strptime(data['DateOpubAkt'], '%Y-%m-%d').strftime('%d.%m.%Y')
            sv_akt.set("ДатаОпубАкт", date_opub_akt)
        if data.get('DateVstypAkt'):
            date_vstyp_akt = datetime.strptime(data['DateVstypAkt'], '%Y-%m-%d').strftime('%d.%m.%Y')
            sv_akt.set("ДатаВступАкт", date_vstyp_akt)

        if data.get('date-mg'):
            nal_per_mes_god_xml = ET.SubElement(sv_akt, "НалПерМесГод")
            nal_per_mes_god_xml.text = data['date-mg']
        elif data.get('NalPeriod'):
            nal_per_god = ET.SubElement(sv_akt, "НалПерГод")
            nal_per_god.text = data['NalPeriod'].split()[0]
        else:
            nal_per_god = ET.SubElement(sv_akt, "НалПерГод")
            nal_per_god.text = str(timezone.now().year)

        if data.get('CodeORKTMO'):
            oktmo = ET.SubElement(sv_akt, "ОКТМО")
            oktmo.text = data['CodeORKTMO']
        else:
            oktmo = ET.SubElement(sv_akt, "ОКТМО")
            oktmo.text = "00000000"

        if data.get('DescNalStav') or data.get('NameObject') or data.get('taxRate') or data.get('measure') or data.get('PerNalStav'):
            sv_nal_stav = ET.SubElement(doc, "СвНалСтав")
            if data.get('DescNalStav') and data.get('DescNalStav') != 'none':
                sv_nal_stav.set("СведНалСтав", data['DescNalStav'])
            if data.get('NameObject'):
                sv_nal_stav.set("НаимОбъект", data['NameObject'])
            if data.get('taxRate'):
                sv_nal_stav.set("РазмНалСтав", data['taxRate'])
            if data.get('measure'):
                sv_nal_stav.set("ЕдИзмер", data['measure'])
            if data.get('PerNalStav') and data.get('PerNalStav') != 'none':
                sv_nal_stav.set("ПерНалСтав", data['PerNalStav'])

        if data.get('SvedNalLgot') or data.get('CategoryNalLgot') or data.get('ContentNL'):
            sv_nal_lgot = ET.SubElement(doc, "СвНалЛьгот")
            if data.get('SvedNalLgot') and data.get('SvedNalLgot') != 'none':
                sv_nal_lgot.set("СведНалЛьгот", data['SvedNalLgot'])
            if data.get('CategoryNalLgot'):
                sv_nal_lgot.set("КатегНал", data['CategoryNalLgot'])
            if data.get('ContentNL'):
                sv_nal_lgot.set("СодНалЛьгот", data['ContentNL'])

        if data.get('SvedNalVych') or data.get('CategoryNalVych') or data.get('SizeNV'):
            sv_nal_vych = ET.SubElement(doc, "СвНалВыч")
            if data.get('SvedNalVych') and data.get('SvedNalVych') != 'none':
                sv_nal_vych.set("СведНалВыч", data['SvedNalVych'])
            if data.get('CategoryNalVych'):
                sv_nal_vych.set("КатегНал", data['CategoryNalVych'])
            if data.get('SizeNV'):
                sv_nal_vych.set("РазмНалВыч", data['SizeNV'])

        if data.get('KodUstSrok') or data.get('UstSrok'):
            sv_ust_srok = ET.SubElement(doc, "СвУстСрок")
            if data.get('KodUstSrok') and data.get('KodUstSrok') != 'none':
                sv_ust_srok.set("КодУстСрок", data['KodUstSrok'])
            if data.get('UstSrok'):
                sv_ust_srok.set("УстСрок", data['UstSrok'])

        if data.get('SvOsobOpr'):
            sv_osob_opr_xml = ET.SubElement(doc, "СвОсобОпр")
            sv_osob_opr_xml.text = data['SvOsobOpr']
        if data.get('SvDataNach'):
            sv_data_nach_xml = ET.SubElement(doc, "СвДатаНач")
            sv_data_nach_xml.text = data['SvDataNach']
        if data.get('SvOtmUpl'):
            sv_otm_upl_xml = ET.SubElement(doc, "СвОтмУпл")
            sv_otm_upl_xml.text = data['SvOtmUpl']

        xml_raw = ET.tostring(root, encoding='utf-8', method='xml')
        xml_string = minidom.parseString(xml_raw).toprettyxml(indent="  ")

        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{tax_doc.id_file}_{timestamp}.xml"
        xml_file = BytesIO(xml_string.encode('utf-8'))
        tax_doc.xml_file.save(filename, File(xml_file), save=False)

        tax_doc.save()

        request.session['xml_path'] = tax_doc.xml_file.url
        request.session['xml_data'] = xml_string

        return redirect('success')

    return render(request, 'fns_app/index.html')

def some_success_view(request):
    xml_data = request.session.get('xml_data', 'XML не найден')
    xml_path = request.session.get('xml_path', None)
    request.session.pop('xml_data', None)
    request.session.pop('xml_path', None)
    return render(request, 'fns_app/success.html', {'xml_path': xml_path, 'xml_data': xml_data})