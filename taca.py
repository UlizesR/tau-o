import argparse
import inquirer

from dotenv import load_dotenv
from chatbot import ChatBot
import commands

load_dotenv()


# Usage
parser = argparse.ArgumentParser(description='Manage chatbot conversations.')
parser.add_argument(commands.CHAT_NAME, type=str, help=commands.COMMANDS_HELP[commands.CHAT_NAME])
parser.add_argument(commands.CHAT_LIST, action='store_true', help=commands.COMMANDS_HELP[commands.CHAT_LIST])
parser.add_argument(commands.DELETE, type=str, help=commands.COMMANDS_HELP[commands.DELETE])
parser.add_argument(commands.DELETE_ALL, action='store_true', help=commands.COMMANDS_HELP[commands.DELETE_ALL])
args = parser.parse_args()

chatbot = ChatBot()

if args.chat_name:
    chatbot.start_chat(args.chat_name)
elif args.chat_list:
    chats = chatbot.list_chats()
    if chats:
        questions = [
            inquirer.List('selected_chat',
                          message="Choose a chat",
                          choices=chats,
                          ),
        ]
        answers = inquirer.prompt(questions)
        selected_chat = answers['selected_chat']
        chatbot.print_chat(selected_chat)
        chatbot.start_chat(selected_chat)
elif args.delete:
    chatbot.delete_chat(args.delete)
elif args.delete_all:
    chatbot.delete_all_chats()