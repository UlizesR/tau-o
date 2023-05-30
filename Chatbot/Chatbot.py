import os
from colorama import Fore, Style
from dotenv import load_dotenv
import halo

from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import PostgresChatMessageHistory
from langchain import OpenAI, LLMChain
from langchain.utilities import GoogleSearchAPIWrapper

import Database.UserCredentials as uc
import Database.Chat as chat
import Chatbot.Commands as cmd

load_dotenv()

class Chatbot:
    def __init__(self):
        # get database url to connect to database
        self.db_url = os.getenv("DATABASE_URL")

        # create a connection to the Google Search API
        # create the tools that the chatbot will use
        search = GoogleSearchAPIWrapper()
        self.tools = [
            Tool(
                name = "Search",
                func=search.run,
                description="useful for when you need to answer questions about current events"
            )
        ]

        prefix = """
            Your name is Tau-O, a natural language processing chatbot that can answer questions.
            You should think step by step, be concise, and attempt to find the most logical solution by going about it step by step. 
            Use multiple sources to find and verify the answer, check your work for errors, and do not return multiple solutions or add unnecessary text in the response. 
            Finally, do not return a solution that is not relevant to the question and do not rush to a conclusion.
            You are allow to be creative in your responses, but you must be logical and concise and correct.
            You have access to the following tools:
        """
        suffix = """Begin!"

        {chat_history}
        Question: {input}
        {agent_scratchpad}"""

        self.prompt = ZeroShotAgent.create_prompt(
            self.tools, 
            prefix=prefix, 
            suffix=suffix, 
            input_variables=["input", "chat_history", "agent_scratchpad"]
        )  

    def start_chat(self, chat_name):
        # let the chat's name be the session id
        # create the chatbot's memory
        self.message_history = PostgresChatMessageHistory(
            connection_string=self.db_url,
            table_name="chat",
            session_id=chat_name
        )
        memory = ConversationBufferMemory(memory_key="chat_history", chat_memory=self.message_history)

        # create the chatbot's agent
        llm_chain = LLMChain(llm=OpenAI(temperature=0.3), prompt=self.prompt)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=self.tools)
        self.agent_chain = AgentExecutor.from_agent_and_tools(agent=agent, tools=self.tools, memory=memory)

        # start the chatbot
        self.start(chat_name=chat_name)

    def start(self, chat_name):
        print(Fore.CYAN + f"Chat Name: {chat_name}" + Style.RESET_ALL)
        print(Fore.CYAN + "Hello, I am Tau-O, the Terminal Assistant Using OpenAI" + Style.RESET_ALL)
        print(Fore.CYAN + "Type 'exit' to exit the chat." + Style.RESET_ALL)
        print()

        while True:
            user_input = input(Fore.BLUE + "You: " + Style.RESET_ALL)
            # self.message_history.add_user_message(user_input)
            if user_input == cmd.EXIT:
                break
            print()
            
            with halo.Halo(text='Loading Response', spinner='simpleDots', color='cyan'):
                ai_response = self.agent_chain.run(input=user_input)
            # self.message_history.add_ai_message(ai_response)
            print(Fore.RED + "TAU-O: " + Style.RESET_ALL + ai_response)
            print()
    
    