import streamlit as st
import uuid
import asyncio
from source.utils.crud import load_chats_from_api, load_chat_messages, delete_chat_from_api, save_message_to_api
from source.agent.agent import ContextAwareAgent
import time
GREETING_MESSAGE = "Привет! Я AI-агент, который поможет с заполнением документов. Сейчас умею заполнять только доверенность на управление автомобилем. Начнем?"


def initialize_chats():
    """инициализация чатов"""
    if "chats_loaded" not in st.session_state:
        api_chats_list = load_chats_from_api()
        
        st.session_state["chats"] = {}
        st.session_state["chat_uuids"] = {}
        st.session_state["agents"] = {}
        
        if api_chats_list:
            for chat_item in api_chats_list:
                chat_uuid = str(chat_item["chat_id_uuid"])
                messages = load_chat_messages(chat_uuid)
                
                if messages:
                    messages.sort(key=lambda x: x["created_at"])
                    
                    chat_messages = []
                    agent = ContextAwareAgent()
                    for msg in messages:
                        chat_messages.append({"role": "user", "content": msg["message_from_human"]})
                        chat_messages.append({"role": "assistant", "content": msg["message_from_ai_agent"]})
                        agent.conversation_history.append("Предыдущий запрос пользователя: " + msg["message_from_human"])
                        agent.conversation_history.append("Ответ агента: " + msg["message_from_ai_agent"])

                    st.session_state["chats"][chat_uuid] = chat_messages
                    st.session_state["chat_uuids"][chat_uuid] = chat_uuid
                    st.session_state["agents"][chat_uuid] = agent
                else:
                    st.session_state["chats"][chat_uuid] = [{"role": "assistant", "content": f"{GREETING_MESSAGE}"}]
                    st.session_state["chat_uuids"][chat_uuid] = chat_uuid
                    st.session_state["agents"][chat_uuid] = ContextAwareAgent()

        if not st.session_state["chats"]:
            new_chat_uuid = str(uuid.uuid4())
            st.session_state["chats"] = {new_chat_uuid: [{"role": "assistant", "content": f"{GREETING_MESSAGE}"}]}
            st.session_state["chat_uuids"] = {new_chat_uuid: new_chat_uuid}
            st.session_state["agents"] = {new_chat_uuid: ContextAwareAgent()}

        if "current_chat" not in st.session_state:
            st.session_state["current_chat"] = list(st.session_state["chats"].keys())[0]
        
        st.session_state["chats_loaded"] = True


initialize_chats()

with st.sidebar:
    # vibe code. check later
    st.title("DocAgent")
    
    if st.button("➕ Новый чат", use_container_width=True):
        new_chat_uuid = str(uuid.uuid4())
        st.session_state.chats[new_chat_uuid] = [{"role": "assistant", "content": f"{GREETING_MESSAGE}"}]
        st.session_state.chat_uuids[new_chat_uuid] = new_chat_uuid
        st.session_state.agents[new_chat_uuid] = ContextAwareAgent()
        st.session_state.current_chat = new_chat_uuid
        st.rerun()
    
    st.subheader("Ваши чаты")
    
    # if st.session_state.agents.get(st.session_state.current_chat):
    #     current_agent = st.session_state.agents[st.session_state.current_chat]
    #     completion = current_agent.document.get_completion_percentage()
    
    if st.session_state.chats:
        for chat_uuid in st.session_state.chats.keys():
            col1, col2 = st.columns([8, 1])
            
            with col1:
                button_style = "🔹" if chat_uuid == st.session_state.current_chat else "💬"
                short_uuid = chat_uuid[:10] + "..."
                
                agent = st.session_state.agents.get(chat_uuid)
                if agent and agent.document.get_completion_percentage() > 0:
                    completion = agent.document.get_completion_percentage()
                    status_emoji = "✅" if completion == 100 else f"{completion:.0f}%"
                    button_text = f"{button_style} {short_uuid} ({status_emoji})"
                else:
                    button_text = f"{button_style} {short_uuid}"
                
                if st.button(button_text, key=f"chat_{chat_uuid}", use_container_width=True):
                    st.session_state.current_chat = chat_uuid
                    st.rerun()
            
            with col2:
                if len(st.session_state.chats) > 1:
                    if st.button("🗑️", key=f"delete_{chat_uuid}", help="Удалить чат"):
                        chat_messages = st.session_state.chats[chat_uuid]
                        has_real_messages = len(chat_messages) > 1 or (
                            len(chat_messages) == 1 and 
                            chat_messages[0]["role"] != "assistant" or 
                            chat_messages[0]["content"] != GREETING_MESSAGE
                        )
                        
                        success = True
                        if has_real_messages:
                            success = delete_chat_from_api(chat_uuid)
                        
                        if success:
                            del st.session_state.chats[chat_uuid]
                            del st.session_state.chat_uuids[chat_uuid]
                            if chat_uuid in st.session_state.agents:
                                del st.session_state.agents[chat_uuid]
                            
                            if st.session_state.current_chat == chat_uuid:
                                st.session_state.current_chat = list(st.session_state.chats.keys())[0]
                            
                            st.success(f"Чат удален")
                        st.rerun()
    else:
        st.info("У вас пока нет чатов")

st.title("DocAgent")

if st.session_state.agents.get(st.session_state.current_chat):
    current_agent = st.session_state.agents[st.session_state.current_chat]

current_chat_short = st.session_state.current_chat

if st.session_state.current_chat in st.session_state.chats:
    current_messages = st.session_state.chats[st.session_state.current_chat]
    
    for msg in current_messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    if prompt := st.chat_input("Введите ваше сообщение..."):
        st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        current_agent = st.session_state.agents.get(st.session_state.current_chat)
        
        with st.spinner("Обрабатываю ваш запрос..."):
            try:
                ai_response = asyncio.run(current_agent.analyze_user_intent(prompt, current_agent.conversation_history))
                print("AI_RESPONSE", ai_response)
                st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": ai_response})
                st.chat_message("assistant").write(ai_response)

                chat_uuid = st.session_state.current_chat
                save_result = save_message_to_api(chat_uuid, prompt, ai_response)
               
                if current_agent.document.get_completion_percentage() == 100:
                    st.success("🎉 Доверенность готова! Вы можете скопировать текст и подписать документ.")
                    st.balloons()
                
            except Exception as e:
                st.error(f"Произошла ошибка: {str(e)}")
                st.session_state.chats[st.session_state.current_chat].append({
                    "role": "assistant", 
                    "content": "Извините, произошла ошибка при обработке вашего запроса. Попробуйте еще раз."
                })
                
        st.rerun()
else:
    st.error("Выбранный чат не найден")
