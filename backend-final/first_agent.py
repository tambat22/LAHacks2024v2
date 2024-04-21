from uagents import Agent, Context
import os
from gemini import GeminiAPI
from models import APIResponse, Image, Message
from dotenv import load_dotenv

load_dotenv()

image_processing_agent = Agent(
    name="user-interaction-agent",  
    seed=os.getenv('AGENT1_SEED_PHRASE'), 
    port=8001,
    endpoint="http://localhost:8001/submit",  
)

@image_processing_agent.on_query(model=Image, replies={APIResponse})
async def handle_query(ctx: Context, sender: str, msg: Image):
    try:
        ctx.logger.info(f"Received image path {msg.path} from Agent 1 : {os.getenv('AGENT1_ADDRESS')}")
        gemini = GeminiAPI(path=msg.path)
        extracted_json = gemini.generate_content()
        description, is_dangerous, risk_level = extracted_json["description"], extracted_json["danger_detected"], extracted_json["threat_level"].lower()
        await ctx.send(sender, APIResponse(description=description, is_dangerous=is_dangerous, risk_level=risk_level))
        
        if risk_level is not None and risk_level == "high":
            await ctx.send(os.getenv('AGENT2_ADDRESS'), APIResponse(description=description, is_dangerous=is_dangerous, risk_level=risk_level))

# @image_processing_agent.on_query(model=Image, replies={APIResponse})
# async def handle_query(ctx: Context, sender: str, msg: Image):
#     try:
#         ctx.logger.info(f"Received image path {msg.path} from Agent 1 : {os.getenv('AGENT1_ADDRESS')}")
#         gemini = GeminiAPI(path=msg.path)
#         extracted_json = gemini.generate_content()
#         print("Extracted JSON: ", extracted_json)
#         description, is_dangerous, risk_level = extracted_json["description"], extracted_json["danger_detected"], extracted_json["threat_level"].lower()
#         await ctx.send(sender, APIResponse(description=description, is_dangerous=is_dangerous, risk_level=risk_level))

        # if risk_level is not None and risk_level == "high":
        #     print("Sender :: ", sender)
        #     await ctx.send(sender, Message(message="Alert sent to emergency services!"))
        #     await ctx.send(os.getenv('AGENT2_ADDRESS'), Message(message=sender))
        # else:
        #     await ctx.send(sender, Message(message=description))
    
    except Exception as e:
        ctx.logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    image_processing_agent.run()