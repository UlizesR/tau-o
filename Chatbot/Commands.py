# This file contains all the commands that the user can use.

HELP = ['--help', '-h']

CHAT_NAME = '--chat_name'
LIST_CHATS = '--list_chats'
DELETE_CHAT = '--delete_chat'

INIT_USER = '--init_user'

EXIT = 'exit'

COMMANDS_DESCRIPTIONS = {

    HELP[0]:"""
        prints all commands and their descriptions.
        Usage: taulo --help or taulo -h
    """,
    CHAT_NAME:"""
        Creates a new chat with the given name.
        Usage: taulo --chat_name <chat_name>
    """,
    LIST_CHATS:"""
        Lists all chats the user has.
        Usage: taulo --list_chats
    """,
    DELETE_CHAT:"""
        Deletes a chat with the given name.
        Usage: taulo --delete_chat <chat_name>
    """,
    INIT_USER:"""
        Initializes a user and prompts to login or register.
        Usage: taulo --init_user
    """,
    EXIT:"""
        Exits the program or chat.
        Usage: exit
    """
}