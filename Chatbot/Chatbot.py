import os
from colorama import Fore, Style
from dotenv import load_dotenv
import halo

from langchain.agents import ZeroShotAgent, Tool, AgentExecutor
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_message_histories import PostgresChatMessageHistory
from langchain import OpenAI, LLMChain
from langchain.utilities import GoogleSearchAPIWrapper

import Database.UserCreds as uc
import Utils.Commands as cmd

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
            You can answer questions about current events, but you can also answer questions about anything else.
            You have access to the internet, so you can use Google to find answers to questions.
            You can use multiple sources to find and verify the answer.

            You are to follow these rules:
                If user introduces themselves, you should respond with "Hello, <user's name>." and introduce yourself. 
                Be concise and do not add unnecessary text in the response.
                Think step by step 
                Even if there is a lack of details, attempt to find the most logical solution by going about it step by step
                Do not return multiple solutions
                Do not add notes or intro sentences 
                Do not show multiple distinct solutions to the question
                Do not return what the question was 
                Do not repeat or paraphrase the question in your response 
                Do not return a solution that is not relevant to the question
                check your work for errors
                use multiple sources to find and verify the answer
                Do not rush to a conclusion
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
        print(Fore.CYAN + "Hello, I am Tau-O, the Terminal base chatbot" + Style.RESET_ALL)
        print(Fore.CYAN + "Type 'exit' to exit the chat." + Style.RESET_ALL)
        print()

        while True:
            user_input = input(Fore.BLUE + f"{uc.USER}: " + Style.RESET_ALL)
            if user_input == cmd.EXIT:
                break
            print()
            
            with halo.Halo(text='Loading Response...', spinner='simpleDots', color='cyan'):
                ai_response = self.agent_chain.run(input=user_input)
            print(Fore.RED + "Tau-O: " + Style.RESET_ALL + ai_response)
            print()