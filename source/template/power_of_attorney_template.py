from source.schemas.power_of_attorney import PowerOfAttorneyData

class PowerOfAttorneyTemplate:
    @staticmethod
    def generate_markdown(document: PowerOfAttorneyData) -> str:
        return f"""
Доверенность на управление автомобилем

Город: {document.city or '_____________'}  
Число: {document.date or '_____________'}

Я, {document.principal_full_name or '_____________________________________________'}  
проживающий по адресу {document.principal_address or '_____________________________________________'}

Паспорт серия {document.principal_passport_series or '_____________'} № {document.principal_passport_number or '_____________'}  
Выдан {document.principal_passport_issued_by or '_____________________________________________'}  
Доверяю {document.agent_full_name or '_____________________________________________'}

проживающему по адресу {document.agent_address or '_____________________________________________'}

Паспорт серия {document.agent_passport_series or '_____________'} № {document.agent_passport_number or '_____________'}  
Выдан {document.agent_passport_issued_by or '_____________________________________________'}

управление, принадлежащим мне на праве личной собственности, транспортным средством {document.car_registration_number or '_____________'}

государственный регистрационный номер {document.car_registration_number or '_____________'}  
год выпуска {document.car_year or '_____________'} двигатель № {document.car_engine_number or '_____________'}  
шасси № {document.car_chassis_number or '_____________'}  
идентификационный номер (VIN) {document.car_vin or '_____________'}  
свидетельство о регистрации выдано {document.registration_certificate_issued_by or '_____________'} от {document.registration_certificate_issuer or '_____________'}  
ПТС серия {document.pts_series or '_____________'} № {document.pts_number or '_____________'}

Доверенность выдана сроком на {document.validity_period or '_____________'}

---
Полномочия по настоящей доверенности не могут быть переданы другим лицам.

Подпись Доверителя _______________  
Подпись Доверенного лица _______________
"""
    
    @staticmethod
    def generate_pdf(document: PowerOfAttorneyData) -> bytes:
        # Для будущей реализации функции для генерации PDF
        pass

