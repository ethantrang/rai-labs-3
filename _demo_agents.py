
from textwrap import dedent
import time 
from dotenv import load_dotenv
load_dotenv()

from relevanceai import RelevanceAI

client = RelevanceAI()

agent_id = "4889a5ae-7512-447f-8122-368be3a01a01" # Meeting Prep Agent
my_agent = client.agents.retrieve_agent(agent_id=agent_id)

message = dedent(f"""
Research the following person for my meeting:
Ethan Trang      
""")

task = my_agent.trigger_task(
    message=message
)

print("Current running task:", task.conversation_id)

while not my_agent.get_task_output_preview(task.conversation_id): 
    print("polling...\n")
    time.sleep(5)

task_output_preview = my_agent.get_task_output_preview(agent_id, task.conversation_id)

print(task_output_preview["answer"])
