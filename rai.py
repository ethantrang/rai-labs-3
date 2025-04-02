from relevanceai import RelevanceAI
import time
from dotenv import load_dotenv
load_dotenv()

class RelevanceAIClient:
    
    def __init__(self):
        self.client = RelevanceAI()
    
    def trigger_agent(self, message, agent_id=None, poll_interval=5):
        agent = self.client.agents.retrieve_agent(agent_id=agent_id)
        task = agent.trigger_task(message=message)
        
        while not agent.get_task_output_preview(task.conversation_id):
            print("Waiting for research results...")
            time.sleep(poll_interval)
        
        task_output = agent.get_task_output_preview(task.conversation_id)
        
        return task_output
    
    def trigger_tool(self, tool_id, params):
        tool = self.client.tools.retrieve_tool(tool_id=tool_id)
        tool_output = tool.trigger(params=params)
        
        return tool_output

rai_client = RelevanceAIClient()