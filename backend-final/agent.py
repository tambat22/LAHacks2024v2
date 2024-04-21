from uagents import Agent, Context, Model

from models import Image, Message
 
# Define the request and response model.

# Initialize the agent with its configuration.
QueryAgent = Agent(
    name="Query Agent",  
    seed="Query Agent Seed Phrase 2",
    port=8001,  
    endpoint="http://localhost:8001/submit",  
)
 
# Getting agent details on startup
@QueryAgent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Starting up {QueryAgent.name}")
    ctx.logger.info(f"With address: {ctx.address}")
    ctx.logger.info(f"And wallet address: {ctx.wallet.address()}")
 
# Decorator to handle incoming queries.
@QueryAgent.on_query(model=Image, replies={Message})
async def query_handler(ctx: Context, sender: str, _query: Image):
    ctx.logger.info("Query received")  # Log receipt of query.
    try:
        await ctx.send(sender, Message(text="success"))
    except Exception:
        await ctx.send(sender, Message(text="fail"))
 
# Main execution block to run the agent.
if __name__ == "__main__":
    QueryAgent.run()