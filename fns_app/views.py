import os
from django.shortcuts import render, redirect
from .models import TaxDocument
from decimal import Decimal
import xml.etree.ElementTree as ET
from datetime import datetime
from django.utils import timezone
from xml.dom import minidom
from django.core.files import File

def submit_form(request):
    if request.method == 'POST':
        data = request.POST
        files = request.FILES

        tax_doc = TaxDocument(
            fio=data.get('fio'),
            knd=data['knd'],
            doc_date=data['docDate'],
            name_organ=data['NameOrgan'],
            inn_organ=data['INNOrgan'],
            kpp_organ=data['KPPOrgan'],
            ogrn_organ=data['OGRNOrgan'],
            nal_per_mes_god=data['NalPerMesGod'],
            name_org_akt=data['NameOrgAkt'],
            date_prin_akt=data['DatePrinAkt'],
            nom_akt=data.get('NomAkt'),
            date_opub_akt=data['DateOpubAkt'],
            date_vstyp_akt=data['DateVstypAkt'],
            name_object=data.get('NameObject'),
            desc_nal_stav=data['DescNalStav'],
            tax_rate=Decimal(data['taxRate']) if data.get('taxRate') else None,
            measure=data.get('measure'),
            per_nal_stav=data.get('PerNalStav'),
            category_nal_lgot=data.get('category_nal_lgot'),
            sved_nal_lgot=data['SvedNalLgot'],
            content_nl=data.get('ContentNL'),
            category_nal_vych=data.get('category_nal_vych'),
            sved_nal_vych=data['SvedNalVych'],
            size_nv=data.get('SizeNV'),
            kod_ust_srok=data['KodUstSrok'],
            ust_srok=data['UstSrok'],
            id_doc=data['IDdoc'],
            type_doc=data['TypeDoc'],
            type_nal=data['TypeNal'],
            type_inf_doc=data['type_inf_doc'],
            any_inf=data.get('AnyInf'),
            id_file=data['IDfile'],
            version=data['version'],
            type_inf_file=data['type_inf_file'],
            pre_vers=data.get('PreVers'),
            kol_doc=data['KolDoc'],
            nal_period=data['NalPeriod'],
            surname=data['surname'],
            name=data['name'],
            patronymic=data.get('patronymic'),
            id_org=data.get('IDorg'),
            reason_code=data.get('ReasonCode'),
            reg_number=data['RegNumber'],
            code_ssrf=data.get('CodeSSRF'),
            code_orktmo=data.get('CodeORKTMO'),
            code_ksono=data.get('CodeKSONO'),
            code_knd=data.get('CodeKND'),
            date_mg=data.get('date-mg'),
            date_full=data.get('date'),
            pdf_file=files.get('pdf_file')
        )

        # Создание XML
        root = ET.Element("Файл")
        root.set("ИдФайл", data['IDfile'])
        root.set("ВерсФорм", data['version'])
        root.set("ТипИнф", data['type_inf_file'])
        if data.get('PreVers'):
            root.set("ВерсПрог", data.get('PreVers'))
        root.set("КолДок", data['KolDoc'])

        if data.get('fio'):
            id_otp = ET.SubElement(root, "ИдОтпр")
            fio_otp = ET.SubElement(id_otp, "ФИООтв")
            fio_parts = data['fio'].split()
            fio_otp.set("Фамилия", fio_parts[0])
            fio_otp.set("Имя", fio_parts[1])
            fio_otp.set("Отчество", fio_parts[2])

        opis_per_sved = ET.SubElement(root, "ОписПерСвед")
        opis_per_sved.set("КНД", data['knd'])
        doc_date = datetime.strptime(data['docDate'], '%Y-%m-%d').strftime('%d.%m.%Y')
        opis_per_sved.set("ДатаДок", doc_date)

        sv_org_reg = ET.SubElement(root, "СвОргРег")
        sv_org_reg.set("НаимОрг", data['NameOrgan'])
        sv_org_reg.set("ИННЮЛ", data['INNOrgan'])
        sv_org_reg.set("КПП", data['KPPOrgan'])
        sv_org_reg.set("ОГРН", data['OGRNOrgan'])

        doc = ET.SubElement(root, "Документ")
        doc.set("ИдДок", data['IDdoc'])
        doc.set("ТипДок", data['TypeDoc'])
        doc.set("ВидНал", data['TypeNal'])
        doc.set("ВидИнф", data['type_inf_doc'])
        if data.get('AnyInf'):
            doc.set("ИнаяИнф", data['AnyInf'])

        sv_akt = ET.SubElement(doc, "СвАкт")
        sv_akt.set("ВидАкт", data['NalPerMesGod'])
        sv_akt.set("НаимОргАкт", data['NameOrgAkt'])
        date_prin_akt = datetime.strptime(data['DatePrinAkt'], '%Y-%m-%d').strftime('%d.%m.%Y')
        sv_akt.set("ДатаПринАкт", date_prin_akt)
        if data.get('NomAkt'):
            sv_akt.set("НомАкт", data['NomAkt'])
        date_opub_akt = datetime.strptime(data['DateOpubAkt'], '%Y-%m-%d').strftime('%d.%m.%Y')
        sv_akt.set("ДатаОпубАкт", date_opub_akt)
        date_vstyp_akt = datetime.strptime(data['DateVstypAkt'], '%Y-%m-%d').strftime('%d.%m.%Y')
        sv_akt.set("ДатаВступАкт", date_vstyp_akt)

        if data.get('date-mg'):
            nal_per_mes_god = ET.SubElement(sv_akt, "НалПерМесГод")
            nal_per_mes_god.text = data['date-mg']
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

        if data.get('NameObject') or data.get('taxRate') or data.get('measure') or data.get('PerNalStav'):
            sv_nal_stav = ET.SubElement(doc, "СвНалСтав")
            sv_nal_stav.set("СведНалСтав", data['DescNalStav'])
            if data.get('NameObject'):
                sv_nal_stav.set("НаимОбъект", data['NameObject'])
            if data.get('taxRate'):
                sv_nal_stav.set("РазмНалСтав", data['taxRate'])
            if data.get('measure'):
                sv_nal_stav.set("ЕдИзмер", data['measure'])
            if data.get('PerNalStav'):
                sv_nal_stav.set("ПерНалСтав", data['PerNalStav'])

        if data.get('category_nal_lgot') or data.get('ContentNL'):
            sv_nal_lgot = ET.SubElement(doc, "СвНалЛьгот")
            sv_nal_lgot.set("СведНалЛьгот", data['SvedNalLgot'])
            if data.get('category_nal_lgot'):
                sv_nal_lgot.set("КатегНал", data['category_nal_lgot'])
            if data.get('ContentNL'):
                sv_nal_lgot.set("СодНалЛьгот", data['ContentNL'])

        if data.get('category_nal_vych') or data.get('SizeNV'):
            sv_nal_vych = ET.SubElement(doc, "СвНалВыч")
            sv_nal_vych.set("СведНалВыч", data['SvedNalVych'])
            if data.get('category_nal_vych'):
                sv_nal_vych.set("КатегНал", data['category_nal_vych'])
            if data.get('SizeNV'):
                sv_nal_vych.set("РазмНалВыч", data['SizeNV'])

        if data.get('UstSrok'):
            sv_ust_srok = ET.SubElement(doc, "СвУстСрок")
            sv_ust_srok.set("КодУстСрок", data['KodUstSrok'])
            sv_ust_srok.set("УстСрок", data['UstSrok'])

        # Форматирование XML
        xml_raw = ET.tostring(root, encoding='utf-8', method='xml')
        xml_string = minidom.parseString(xml_raw).toprettyxml(indent="  ")


        # Сохранение XML в поле xml_file
        timestamp = timezone.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{data['IDfile']}_{timestamp}.xml"
        with open(filename, 'w', encoding='utf-8') as temp_file:
            temp_file.write(xml_string)
        with open(filename, 'rb') as temp_file:
            tax_doc.xml_file.save(filename, File(temp_file), save=False)

        # Сохранение объекта в базу данных
        tax_doc.save()

        # Передача данных через сессию
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