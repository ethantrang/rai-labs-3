from relevanceai import RelevanceAI
from dotenv import load_dotenv
load_dotenv()

client = RelevanceAI()

tool_id = "600da11f-eba1-47cf-8d77-ed4f86fd48dd" # Google Search Tool
my_tool = client.tools.retrieve_tool(tool_id=tool_id)

result = my_tool.trigger(params={"search_query": "Ethan Trang"})

print(result)