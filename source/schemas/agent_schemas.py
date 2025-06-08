from pydantic import BaseModel
from typing import Literal, Optional, List
from .power_of_attorney import PowerOfAttorneyData

class UserIntent(BaseModel):
    action: Literal["offtop", "fill_attorney_power"] # пока оставляем только оффтоп и заполнение доверенности
    reasoning: str

class PowerOfAttorneyAction(BaseModel):
    action_type: Literal["skip", "update_field"]
    action_data: Optional[PowerOfAttorneyData] = None
    reasoning: str

class AgentAnswer(BaseModel):
    answer: str
    reasoning: str
