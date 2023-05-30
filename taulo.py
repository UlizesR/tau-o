import inquirer
import sys
import yaml

import Database.UserCredentials as uc
import Database.Chat as chat
import Database.Auth as auth
import Chatbot.Chatbot as cb
import Chatbot.Commands as cmd

def print_commands():
    for command, description in cmd.COMMANDS_DESCRIPTIONS.items():
        print(command + ":")
        print(description)

def init_user():
    questions = [
        inquirer.List('Innit User',
                      message="Login - Sign Up",
                      choices=['Login', 'Sign Up'],
                    ),
    ]
    answers = inquirer.prompt(questions)
    if answers['Innit User'] == 'Login':
        print("---------- Login ----------\n")
        username: str = input("Username: ")
        password: str = input("Password: ")
        auth.login_verification(username, password)
    else:   
        print("---------- Register ----------\n")
        email: str = input("Email: ")
        username: str = input("Username: ")
        password: str = input("Password: ")
        auth.register(email, username, password)

def init_chat(chat_name):
    chatbot = cb.Chatbot()
    chatbot.start_chat(chat_name)

def list_chats():
    user_chats = chat.get_chats()  # Use the correct function name
    
    chat_names = [chat[0] for chat in user_chats]  # Use an integer index instead of a string key
    print('Click the chat you want to start or click exit to exit')
    questions = [
        inquirer.List('List Chats',
                      message="Your Chats",
                      choices=chat_names + [cmd.EXIT],
                      ),
    ]
    answers = inquirer.prompt(questions)
    chat_name = answers['List Chats']
    if chat_name == cmd.EXIT:
        exit()
    init_chat(chat_name)

if __name__ == "__main__":
    args = sys.argv
    # iniitalize the auth class
    auth = auth.Auth()

    if len(args) > 1:
        if args[1] == cmd.HELP[0] or args[1] == cmd.HELP[1]:
            print_commands()
            exit()
        if args[1] == cmd.INIT_USER:
            init_user()
        if not uc.INITIALIZED:
            print("You need to initialize your account first before you can use the chatbot")
            print("type 'taulo --init_user' to initialize your account")
            exit()
        if args[1] == cmd.CHAT_NAME:
            if len(args) < 3:
                print("missing argument. Usage: taulo --chat_name <chat_name>")
                exit()
            chat_name = args[2]
            init_chat(chat_name)
        elif args[1] == cmd.LIST_CHATS:
            list_chats()
        elif args[1] == cmd.DELETE_CHAT:
            if len(args) < 3:
                print("missing argument. Usage: taulo --delete_chat <chat_name>")
                exit()
            chat_name = args[2]
            chat.get_chat(chat_name)
            chat.delete_chat(chat_name)
        else:
            # if a command is given that is not recognized, it prints a message saying that the command was not found
            print("Command not recognized, type 'taulo --help' for a help.")
    else:
        if not uc.INITIALIZED:
            print("You need to initialize your account first before you can use the chatbot")
            print("type 'taulo --init_user' to initialize your account")
            exit()
        # if no command is given, it exits the program
        print("No command was given, type 'taulo --help' or 'tauo -h' for help.")