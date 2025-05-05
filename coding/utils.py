import streamlit as st
from typing import List, Dict, Any, Optional

def display_session_msg(container_obj, user_image: Optional[str] = None):
    # Initialize messages list if not present
    messages = st.session_state.setdefault("messages", [])

    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        avatar = None

        # Determine avatar to use
        if role == "assistant":
            avatar = user_image
        elif role not in ["user", "assistant"]:
            avatar = msg.get("image", None)

        # Display message
        if avatar:
            container_obj.chat_message(role, avatar=avatar).markdown(content)
        else:
            container_obj.chat_message("ai").markdown(content)

def show_chat_history(container_obj, chat_history: List[Dict[str, Any]], user_image=None):
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for entry in chat_history:
        # 1. Skip any entries whose role is 'tool'
        if entry.get('role') == 'tool':
            continue

        content = entry.get('content')
        # 2. Skip entries with null or empty content
        if content is None:
            continue
        if isinstance(content, str):
            # 3. Replace 'ALL DONE' with empty string
            content = content.replace("ALL_DONE", "")
            if not content.strip():
                continue
        else:
            # non‐string content: skip
            continue

        role = entry.get('role', 'user')
        # Append to session history
        st.session_state.messages.append({"role": role, "content": content})

        # Display according to role
        if role == 'assistant':
            container_obj.chat_message("assistant", avatar=user_image).write(content)
        else:
            container_obj.chat_message(role).write(content)
