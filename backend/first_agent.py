from uagents import Agent, Context
import os
from models import Image
from dotenv import load_dotenv

load_dotenv()

user_interaction_agent = Agent(
    name="user-interaction-agent",  
    seed=os.getenv('AGENT1_SEED_PHRASE'), 
    port=8001,
    endpoint="http://localhost:8001/submit",  
)

@user_interaction_agent.on_query(model=Image, replies={Image})
async def handle_query(ctx: Context, sender: str, msg: Image):
    ctx.logger.info(f"Sending image path {msg.path} to Agent 2 : {os.getenv('AGENT2_ADDRESS')}")
    await ctx.send(os.getenv('AGENT2_ADDRESS'), Image(path=msg.path))
    
if __name__ == "__main__":
    user_interaction_agent.run()