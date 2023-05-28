import sys
import inquirer


from dotenv import load_dotenv
from Chatbot.chatbot import ChatBot
import Chatbot.commands as commands

load_dotenv()

if __name__ == '__main__':

    args = sys.argv

    if len(args) > 1:
        if args[1] == commands.HELP[0] or args[1] == commands.HELP[1]:
            # check if the user is asking for help, it then prints all commands and their descriptions
            print("Commands:")
            for command, description in commands.COMMANDS_DESCRIPTIONS.items():
                print(command + ":")
                print(description)
            exit()

        if args[1] == commands.CHAT_NAME:
            # check if the user is asking to create a new chat, it then creates a new chat with the given name
            if len(args) < 3:
                print("missing chat name. Usage: tauo --chat_name <chat_name>")
                exit()
            chat_name = args[2]
            print(f"Chat Name: {chat_name}")
            exit()
        
        if args[1] == commands.INNIT_USER:
            if len(args) < 6:
                print('missing arguments. Usage: tauo --innit_user -u <user_name> -p <password>')
                exit()
                
            if args[2] != '-u' or args[4] != '-p':
                print('missing -u or -p flag or both. Usage: tauo --innit_user -u <user_name> -p <password>')
                exit()

            user_name = args[3]
            password = args[5]    

            print(f"User Name: {user_name}")
            print(f"Password: {password}")
        else:
            # if a command is given that is not recognized, it prints a message saying that the command was not found
            print("Command not recognized, type 'tauo --help' for a list of commands.")
    else:
        # if no command is given, it exits the program
        print("No command was given, type 'tauo --help' for a list of commands.")