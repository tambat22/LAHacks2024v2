from uagents import Agent, Context
import os
from models import Image

threat_detection_agent = Agent(name="threat-detection-agent", seed=os.getenv('AGENT3_SEED_PHRASE'),)

@threat_detection_agent.on_message(model=Image)
async def message_handler(ctx: Context, sender: str, msg: Image):
    ctx.logger.info(f"Received image path {msg.path} from Agent 1 : {os.getenv('AGENT1_ADDRESS')}")
    
