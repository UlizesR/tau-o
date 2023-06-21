from Database.Query import DB


def create_chat(chat_name: str) -> None:
    DB.insert("chat", "session_id", f"'{chat_name}'")

def get_all_chats() -> list:
    chat = DB.select("chat", "session_id")
    return chat 


def chat_exist(chat_name: str) -> bool:
    # check if chat exists
    chat = DB.select("chat", "session_id", f"session_id = '{chat_name}'")
    if chat:
        return True
    return False

def delete_chat(chat_name: str) -> None:
    DB.delete("chat", f"session_id = '{chat_name}'")

def create_message(chat_name: str, message: str) -> None:
    DB.insert("messages", "chat_name, message", f"'{chat_name}', '{message}'")
    
