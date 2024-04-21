import re
import json

def extract_json_object(text):
    # Regex to find a basic JSON object; this needs refinement for more complex JSON structures
    json_match = re.search(r'{[^{}]*}', text)
    if json_match:
        json_string = json_match.group(0)
        try:
            json_data = json.loads(json_string)
            return json_data
        except json.JSONDecodeError:
            raise Exception("Error decoding JSON")
    else:
        return "No JSON found"

