""""
LLM project made in Delta Munich.
Save file as main file:
Requiered files for this project:
    - tools.py
    - System_prompt.py
    - .env 
    - boot.py

"""
from langchain_mistralai import ChatMistralAI          # imports ai agent
from langchain.agents import create_agent              # will create an agent
from langgraph.checkpoint.memory import InMemorySaver  # creates memory for each user
from tools import author_call, book_call, subject_call # importing all tools for the agent
from dotenv import load_dotenv                         # browsing key from .env
import os                                              # pulls the key out of the env files
from System_prompt import SYSTEM_PROMPT                # safety information
import time                                            # optional (  usefull in the boot file if you make a discord bot or
#                                                                    here if you just runn it in the terminal  )
load_dotenv()                                          # browses the .env file
import sys                                             # for the error handling
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")         # saves the browsed key in a variable
assert MISTRAL_API_KEY, "MISTRAL_API_KEY is not set in the .env file" # reactes if varaible is not  found in the .env file



model = ChatMistralAI(model="mistral-large-latest", api_key=MISTRAL_API_KEY)
memory = InMemorySaver()
# creating the model with the memory 


agent = create_agent(
    model=model,
    tools=[author_call, book_call, subject_call],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=memory,
)
# setting up the actual agent with memory for each user
def invoke_agent(message: str, user_id):
    """
    Varaible explanaition:
        - message -> User prompt or input
        - user_id -> to respond unice for each user
    This tool invokes the agent which will later call tools an doutut data
    """
    try:
        config = {"configurable": {"thread_id": "some-id"}}
        response = agent.invoke(
            {"messages": [{"role": "user", "content": message}]},
            config={
                "configurable": {
                "thread_id": user_id
                    },
            }
        )
        return response["messages"][-1].content
    except:
           # the try except loop is for general errors too, so if the agent doesnt respond after 3 tries, 
           # it will return the same output as if itwas the 429 ( It will be handeled in the terminal part )
        return False


# the following part is only for the terminal part, 
# comment it out to use the bot as a discord bot
"""
if __name__ == "__main__":

    while True:
        calls = 3
        user_input = input("You: ")
        if user_input.lower() in ("quit", "exit"):
            break # checks if the user want to stop the converation

        while calls != 0: # repeats the loop 3 times if no output recived it will stop working automaticly 
            response = invoke_agent(user_input, calls)
            if response is False:
                calls -= 1
            else:
                break
            if call == 0:
                sys.exit()
            print("In waiting")
            time.sleep(30) # the period for a 429 error ( every 60 sec the error will be cleared, so we have 1/2 chance of escaping the error)
            # if after 1 1/2 min it wont respond it will stop the programm.

        print("Agent:", response)
"""  