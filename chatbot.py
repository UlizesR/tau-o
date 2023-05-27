from colorama import init, Fore, Style
import sqlite3

import commands

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI

init()  # Initialize colorama

class ChatBot:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.5)
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=ConversationBufferMemory(),
        )
        self.conn = sqlite3.connect('chats.db')
        self.cursor = self.conn.cursor()

    def start_chat(self, chat_name):
        self.chat_name = chat_name
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {chat_name} (user_input TEXT, ai_response TEXT)")
        self.start()

    def start(self):
        print(Fore.CYAN + f"Chat Name: {self.chat_name}" + Style.RESET_ALL)
        print(Fore.CYAN + "Hello, this is a chatbot for the terminal, type 'exit' to exit" + Style.RESET_ALL)
        print()
        while True:
            user_input = input(Fore.BLUE + "You: " + Style.RESET_ALL)
            if user_input == commands.EXIT:
                break
            print()
            ai_response = self.conversation.predict(input=user_input)
            print(Fore.RED + "AI: " + Style.RESET_ALL + ai_response)
            print()
            self.cursor.execute(f"INSERT INTO {self.chat_name} VALUES (?, ?)", (user_input, ai_response))
            self.conn.commit()

    def print_chat(self, chat_name):
        self.cursor.execute(f"SELECT * FROM {chat_name}")
        chat_contents = self.cursor.fetchall()
        for user_input, ai_response in chat_contents:
            print(Fore.BLUE + "You: " + Style.RESET_ALL + user_input)
            print()
            print(Fore.RED + "AI: " + Style.RESET_ALL + ai_response)
            print()

    def list_chats(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        chats = [chat[0] for chat in self.cursor.fetchall()]
        if not chats:
            print("No chats exist.")
        return chats

    def delete_chat(self, chat_name):
        self.cursor.execute(f"DROP TABLE IF EXISTS {chat_name};")
        self.conn.commit()

    def delete_all_chats(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for chat in self.cursor.fetchall():
            self.delete_chat(chat[0])

    def __del__(self):
        self.conn.close()