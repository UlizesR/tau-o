# File holds all commands for the bot

INIT_USER = "--init_user"
UPDATE_USER = "--update_user"

UPDATE_BOT = "--update"

HELP = "--help"
HELP_SHORT = "-h"

CHAT_NAME = "--chat_name"
LIST_CHATS = "--list_chats"
DELETE_CHAT = "--delete_chat"

EXIT = "exit"

PROMPT = "--prompt"

COMMAND_DESCRIPTIONS = {
    INIT_USER:"Initializes a user in the database.\n"
            "Usage: taulo --init_user"
    ,
    UPDATE_USER:"Updates info a user in the database.\n"
                "Usage: taulo --update_user",

    UPDATE_BOT: "Checks for updates and updates the program.\n"
                "Usage: taulo --update",

    HELP: "Displays help.\n"
            "Usage: taulo --help or taulo -h",

    CHAT_NAME: "Creates a chat with the given name.\n"
                "Usage: taulo --chat_name <name>",
    LIST_CHATS: "Lists all chats.\n"
                "Usage: taulo --list_chats",
    DELETE_CHAT: "Deletes a chat.\n"
                "Usage: taulo --delete_chat <name>",

    PROMPT: "A one time prompt.\n"
            "Usage: taulo --prompt <prompt>",
}