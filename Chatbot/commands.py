HELP = ['--help', '-h']
CHAT_NAME = '--chat_name'
LIST_CHATS = '--list_chats'
INNIT_USER = '--init_user'
PROMPT = '--prompt'
READ_FILE = '--read_file'
EXIT = 'exit'


COMMANDS_DESCRIPTIONS = {
    HELP[0]: 
        """
            prints all commands and their descriptions.\n
            Usage: tauo --help or tauo -h
        """,
    CHAT_NAME: 
        """
            Creates a new chat with the given name.\n
            Usage: tauo --chat_name <chat_name>
        """,
    LIST_CHATS:
        """
            Lists all chats.\n
            Usage: tauo --list_chats
        """,
    INNIT_USER:
        """
            Creates a new user.\n
            Usage: tauo --innit_user -u <user_name> -p <password>
        """,
    PROMPT:
        """
            Propmts the ai and it gives a response.\n
            Usage: tauo --prompt <prompt>
            Note: The prompt must be in quotes.
        """,
    READ_FILE:
        """
            Reads a file and creates a chat with the given name.\n
            Usage: tauo --read_file <file_name>
        """,
    EXIT: 
        """
            Exits the program or chat.\n
            Usage: exit
        """
    
    
}

