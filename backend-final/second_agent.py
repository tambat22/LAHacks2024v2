from uagents import Agent, Context
import os
from TwilioAPI import TwilioAPI
from json_utils import extract_json_object
from models import APIResponse, Image, Message
from gemini import GeminiAPI
from dotenv import load_dotenv
import asyncio

load_dotenv()

emergency_handling_agent = Agent(name="emergency-handling-agent", seed=os.getenv('AGENT2_SEED_PHRASE'), port=8002, endpoint="http://localhost:8002/submit",)

@emergency_handling_agent.on_message(model=APIResponse)
async def receive_message(ctx: Context, sender: str, msg: APIResponse):
    ctx.logger.info(f"Received APIResponse data from Agent 1 : {sender}")
    twilio = TwilioAPI()
    sid = twilio.make_call("+14085813036", "+18559406386")
    print("Making call with Call SID: ", sid)
    print("Sender :: ", msg.description)
    # await ctx.send(msg.description, Message(message="Alert sent to emergency services!"))

if __name__ == "__main__":
    emergency_handling_agent.run()