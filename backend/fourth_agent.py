from uagents import Agent, Context
import os
from models import Message

emergency_handling_agent = Agent(name="emergency-handling-agent", seed=os.getenv('AGENT4_SEED_PHRASE'),)

@emergency_handling_agent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received image path {msg.message} from Agent 3 : {os.getenv('AGENT3_ADDRESS')}")