# Importing required libraries
import json
import asyncio
from uagents import Model
from uagents.query import query
 
# Define the agent's address to send queries to.
AGENT_ADDRESS = "agent1qfsp8ahahew609lnk4q85przx3uxgrx6kge54k3l0sd3488c3kpgv36hnn0"
 
# Define a model for the query request.
class QueryRequest(Model):
    message: str  
 
# Asynchronous function to send a query to the specified agent.
async def agent_query(req):
    response = await query(destination=AGENT_ADDRESS, message=req, timeout=15.0)
    data = json.loads(response.decode_payload())# Decode the payload from the response and load it as JSON.
    return data["text"]
 
# Asynchronous function to make a call to an agent and handle the response.
async def make_agent_call(req: QueryRequest):
    try:
        response = await agent_query(req)
        return f"successful call - agent response: {response}"
    except Exception:
        return "unsuccessful agent call"

# Main block to execute the script.
async def main():
    # Create a QueryRequest instance with your query and run make_agent_call with request
    request = QueryRequest(message="Hello, agent!")
    response = await make_agent_call(request)
    print(response)

if __name__ == "__main__":
    asyncio.run(main())
 