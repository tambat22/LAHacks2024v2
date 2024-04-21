from uagents import Bureau
from first_agent import user_interaction_agent
from second_agent import image_processing_agent
from third_agent import threat_detection_agent
from fourth_agent import emergency_handling_agent

from dotenv import load_dotenv

load_dotenv()

bureau = Bureau(endpoint="http://localhost:8002/submit", port=8002)

bureau.add(image_processing_agent)
bureau.add(threat_detection_agent)
bureau.add(emergency_handling_agent)

if __name__ == "__main__":
    bureau.run()