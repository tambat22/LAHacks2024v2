from uagents import Agent, Context
import os
from models import Image
from gemini import GeminiAPI
from uagents import Bureau
from first_agent import user_interaction_agent

image_processing_agent = Agent(name="image-processing-agent", seed=os.getenv('AGENT2_SEED_PHRASE'), port=8002, endpoint="http://localhost:8002/submit",)

@image_processing_agent.on_message(model=Image)
async def receive_message(ctx: Context, sender: str, msg: Image):
    ctx.logger.info(f"Received image path {msg.path} from Agent 1 : {os.getenv('AGENT1_ADDRESS')}")

    gemini = GeminiAPI(path=msg.path)
    print(gemini.generate_content())
