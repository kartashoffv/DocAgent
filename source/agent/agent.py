from source.config import config
from openai import AsyncOpenAI
from typing import Dict, Any, List
import logging
from source.schemas.power_of_attorney import PowerOfAttorneyData
from source.schemas.agent_schemas import UserIntent, PowerOfAttorneyAction, AgentAnswer
from source.template.power_of_attorney_template import PowerOfAttorneyTemplate

from source.utils.llm_invoke import llm_invoke_structured_output

from source.agent.prompts import (
    INTENT_IDENTIFICATION_PROMPT,
    OFFTOP_PROMPT,
    DATA_EXTRACTION_PROMPT_FILL_ATTORNEY_POWER,
    SKIP_LOGICAL_PROMPT,
    SUCCESS_PROMPT_FILL_ATTORNEY_POWER,
    ASK_FOR_DATA
)

logger = logging.getLogger(__name__)

class ContextAwareAgent:
    def __init__(self):
        self.document = PowerOfAttorneyData()
        # self.conversation_history = []
        self.client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

    
    async def analyze_user_intent(self, user_input: str, conversation_history: list[str]):
        """Функция для анализа интента"""
        
        
        try:
            prompt = INTENT_IDENTIFICATION_PROMPT.format(user_input=user_input, conversation_history=conversation_history)
            result = await llm_invoke_structured_output(prompt, user_input, UserIntent)
            if result.action == "offtop":
                prompt = OFFTOP_PROMPT.format(conversation_history=conversation_history)
                result = await llm_invoke_structured_output(prompt, user_input, AgentAnswer)
                return result.answer, "offtop"
            else:
                return await self.extract_data_for_attorney_power(user_input, conversation_history)
            
        except Exception as e:
            logger.error(f"Error in intent analysis: {e}")
            return AgentAnswer(
                answer="Извините, я не могу обработать ваше сообщение. Ошибка в блоке analyze_user_intent",
                reasoning="Due to falling",
                actions=[]
            )
    
    async def extract_data_for_attorney_power(self, user_input: str, conversation_history: list[str]) -> Dict[str, Any]:
        """функция для работы с данными для доверенности"""
        prompt = DATA_EXTRACTION_PROMPT_FILL_ATTORNEY_POWER.format(
            missing_fields=self.document.get_missing_fields(),
            filled_fields=self.document.get_filled_fields(),
            conversation_history=conversation_history
            )

        # пытаемся извлечь сущности из сообщения пользователя и заполнить форму
        try:
            result = await llm_invoke_structured_output(prompt, user_input, PowerOfAttorneyAction)
            if result.action_type == "skip":
                # не обновляем поля, а просто возвращаемся к пользователю с ответом
                prompt = SKIP_LOGICAL_PROMPT.format(
                    filled_fields=self.document.get_filled_fields(),
                    missing_fields=self.document.get_missing_fields(),
                    conversation_history=conversation_history
                )
                
                result = await llm_invoke_structured_output(prompt, user_input, AgentAnswer)
                return result.answer, "fill_attorney_power"
            
            elif result.action_type == "update_field":
                self._update_document(result.action_data)
                if self.document.get_completion_percentage()==100:
                    result = await llm_invoke_structured_output(SUCCESS_PROMPT_FILL_ATTORNEY_POWER, user_input, AgentAnswer)
                    document_markdown = self.generate_final_document()
                    return result.answer + "\n" + document_markdown, "fill_attorney_power"

                answer_prompt = ASK_FOR_DATA.format(
                    filled_fields=self.document.get_filled_fields(),
                    missing_fields=self.document.get_missing_fields(),
                    conversation_history=conversation_history
                )
                
                result = await llm_invoke_structured_output(answer_prompt, user_input, AgentAnswer)
                return result.answer, "fill_attorney_power"

 
            
        except Exception as e:
            logger.error(f"Error in extract_data_for_attorney_power: {e}")
            return {
                "action_type": "skip",
                "reasoning": f"Error processing request: {e}"
            }

    def _update_document(self, new_data: PowerOfAttorneyData):
        """Обновляет текущий документ новыми данными"""
        new_fields = new_data.get_filled_fields()        
        for field_name, field_value in new_fields.items():
            if hasattr(self.document, field_name):
                setattr(self.document, field_name, field_value)
                logger.info(f"upd field {field_name}: {field_value}")

    def get_document_status(self) -> Dict[str, Any]:
        """Возвращает текущее состояние документа"""
        return {
            "filled_fields": self.document.get_filled_fields(),
            "missing_fields": self.document.get_missing_fields(),
            "completion_percentage": self.document.get_completion_percentage()
        }

    def reset_document(self):
        """Сбрасывает документ к пустому состоянию"""
        self.document = PowerOfAttorneyData()

    def generate_final_document(self) -> str:
        return PowerOfAttorneyTemplate.generate_markdown(self.document)

        
        
