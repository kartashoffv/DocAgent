import requests
import logging
from source.config import config

logger = logging.getLogger(__name__)

def save_message_to_api(chat_uuid: str, human_message: str, ai_message: str, intent: str):
    """cохранить сообщение"""
    try:
        response = requests.post(
            f"{config.API_BASE_URL}{config.API_V1_STR}/chats/",
            json={
                "chat_id_uuid": chat_uuid,
                "message_from_human": human_message,
                "message_from_ai_agent": ai_message,
                "message_intent": intent
            }
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"ошибка при сохранении в БД: {e}")
        return None

def load_chats_from_api():
    """загрузить список чатов"""
    try:
        response = requests.get(f"{config.API_BASE_URL}{config.API_V1_STR}/chats/list")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"ошибка при загрузке чатов из API: {e}")
        return []

def load_chat_messages(chat_uuid: str):
    """загрузить сообщения конкретного чата"""
    try:
        response = requests.get(
            f"{config.API_BASE_URL}{config.API_V1_STR}/chats/{chat_uuid}"
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"ошибка при загрузке сообщений чата: {e}")
        return []

def delete_chat_from_api(chat_uuid: str):
    """удалить чат"""
    try:
        response = requests.delete(f"{config.API_BASE_URL}{config.API_V1_STR}/chats/{chat_uuid}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"ошибка при удалении чата: {e}")
        return False
    
    
def get_n_mesage(chat_uuid: str, n: int=1):
    """получить n сообщений из чата"""
    try:
        response = requests.get(f"{config.API_BASE_URL}{config.API_V1_STR}/chats/{chat_uuid}?limit={n}")
        response.raise_for_status()
        return response.json()[::-1]
    except requests.exceptions.RequestException as e:
        logger.error(f"ошибка при получении сообщений из чата: {e}")
        return []