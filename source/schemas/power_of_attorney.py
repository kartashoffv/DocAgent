from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class PowerOfAttorneyData(BaseModel):
    """поля сгенерировал gpt на основе картинки """
    city: Optional[str] = None
    date: Optional[str] = None
    
    principal_full_name: Optional[str] = None
    principal_address: Optional[str] = None
    principal_passport_series: Optional[str] = None
    principal_passport_number: Optional[str] = None
    principal_passport_issued_by: Optional[str] = None
    
    agent_full_name: Optional[str] = None
    agent_address: Optional[str] = None
    agent_passport_series: Optional[str] = None
    agent_passport_number: Optional[str] = None
    agent_passport_issued_by: Optional[str] = None
    
    car_registration_number: Optional[str] = None
    car_year: Optional[str] = None
    car_engine_number: Optional[str] = None
    car_chassis_number: Optional[str] = None
    car_body_number: Optional[str] = None
    car_vin: Optional[str] = None
    
    registration_certificate_issued_by: Optional[str] = None
    registration_certificate_issuer: Optional[str] = None
    pts_series: Optional[str] = None
    pts_number: Optional[str] = None
    
    validity_period: Optional[str] = None
    
    def get_missing_fields(self):
        missing = []
        for field_name, field_value in self.dict().items():
            if field_value is None:
                missing.append(field_name)
        return missing
    
    def get_filled_fields(self):
        return {k: v for k, v in self.dict().items() if v is not None}
    
    def get_completion_percentage(self):
        total = len(self.dict())
        filled = len(self.get_filled_fields())
        return (filled / total) * 100
