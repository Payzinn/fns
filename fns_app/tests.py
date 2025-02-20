from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from .models import TaxDocument
from decimal import Decimal

class TaxFormTests(TestCase):
    valid_data = {
        'fio': 'Иванов Иван Иванович',
        'knd': '1190803',
        'docDate': '2025-02-20',
        'NameOrgan': 'УФНС России по г. Москве',
        'INNOrgan': '7701234567',
        'KPPOrgan': '770101001',
        'OGRNOrgan': '1027700123456',
        'NalPerMesGod': 'Решение об установлении налога',
        'NameOrgAkt': 'Московская городская дума',
        'DatePrinAkt': '2025-01-15',
        'NomAkt': '123/2025',
        'DateOpubAkt': '2025-01-20',
        'DateVstypAkt': '2025-02-01',
        'NameObject': 'Жилая недвижимость',
        'DescNalStav': '1',
        'taxRate': '0.015000',
        'measure': '1',
        'PerNalStav': '1',
        'category_nal_lgot': 'Многодетные семьи',
        'SvedNalLgot': '2',
        'ContentNL': 'Снижение ставки на 50%',
        'category_nal_vych': 'Физические лица',
        'SvedNalVych': '1',
        'SizeNV': '50000',
        'KodUstSrok': '1',
        'UstSrok': '31.03.2025',
        'IDdoc': 'doc-uuid-1234567890',
        'TypeDoc': '1',
        'TypeNal': '2',
        'type_inf_doc': '1',
        'AnyInf': 'Порядок уплаты установлен решением №123',
        'IDfile': 'file-uuid-0987654321',
        'version': '4.03',
        'type_inf_file': 'УСТ_ИЗМ_ПРЕКР_НАЛОГ',
        'PreVers': '1.2.3',
        'KolDoc': '5',
        'NalPeriod': '2025 год',
        'surname': 'Иванов',
        'name': 'Иван',
        'patronymic': 'Иванович',
        'IDorg': '7709876543',
        'ReasonCode': '770101001',
        'RegNumber': '1027700987654',
        'CodeSSRF': '77',
        'CodeORKTMO': '45383000',
        'CodeKSONO': '7701',
        'CodeKND': '11',
        'date-mg': '02.2025',
        'date': '20.02.2025'
    }

    def test_successful_form_submission(self):
        """Тест: Успешная отправка формы с полным набором данных"""
        url = reverse('submit_form')
        response = self.client.post(url, self.valid_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('success'))
        self.assertEqual(TaxDocument.objects.count(), 1)

        doc = TaxDocument.objects.first()
        self.assertEqual(doc.fio, 'Иванов Иван Иванович')
        self.assertEqual(doc.knd, '1190803')
        self.assertEqual(doc.name_organ, 'УФНС России по г. Москве')
        self.assertEqual(doc.tax_rate, Decimal("0.015000"))
        self.assertEqual(doc.id_doc, 'doc-uuid-1234567890')

    def test_missing_required_fields(self):
        """Тест: Отправка формы без нескольких обязательных полей"""
        url = reverse('submit_form')
        invalid_data = self.valid_data.copy()
        # Удаляем несколько обязательных полей
        del invalid_data['knd']
        del invalid_data['NameOrgan']
        del invalid_data['INNOrgan']

        response = self.client.post(url, invalid_data)

        self.assertEqual(TaxDocument.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_invalid_inn_format(self):
        """Тест: Отправка формы с некорректным ИНН"""
        url = reverse('submit_form')
        invalid_data = self.valid_data.copy()
        invalid_data['INNOrgan'] = 'abc123'  # Некорректный формат (должен быть 10 цифр)

        response = self.client.post(url, invalid_data)

        self.assertEqual(TaxDocument.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_invalid_date_format(self):
        """Тест: Отправка формы с некорректным форматом даты"""
        url = reverse('submit_form')
        invalid_data = self.valid_data.copy()
        invalid_data['docDate'] = '20-02-2025'  # Неправильный формат (нужен ГГГГ-ММ-ДД)

        response = self.client.post(url, invalid_data)

        self.assertEqual(TaxDocument.objects.count(), 0)
        self.assertEqual(response.status_code, 200)

    def test_max_length_exceeded(self):
        """Тест: Превышение максимальной длины поля"""
        url = reverse('submit_form')
        invalid_data = self.valid_data.copy()
        invalid_data['fio'] = 'А' * 256  # Превышает maxlength=255

        response = self.client.post(url, invalid_data)

        self.assertEqual(TaxDocument.objects.count(), 0)
        self.assertEqual(response.status_code, 200)