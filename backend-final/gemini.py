import google.generativeai as genai
import PIL.Image
import os

from json_utils import extract_json_object

class GeminiAPI:

    def __init__(self, path):
        self.image_path = path
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])

        self.generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 0,
            "max_output_tokens": 8192,
        }

        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]

        self.system_instruction = """
            You are a visual speaker and identifier for a visually impaired user. Describe what the input image is and return a response of a specific direction (ie: left, right, 
            straight, back) a visually impaired user should walk in to avoid obstacles, such as cars. 
            DO NOT give a list as a response. Give the instructions in a short paragraph. For example 
            \"This is a car, you should walk left around the car to the sidewalk to move forward 
            to your destination\". DO NOT use the words \"visually impaired person\". You should refer 
            to the person as \"you\". 
            Provide the response in JSON format with the following fields: {'description': Describe what the input image is and a specific direction (ie: left, right, straight, back) a visually impaired user should walk in to avoid obstacles. For example 
            \"This is a car, you should walk left around the car to the sidewalk to move forward 
            to your destination\",
            'danger_detected': A boolean indicating whether any potential danger or threat is present in the image,
            'threat_level': A string that rates the level of any detected threat as 'low', 'mid', or 'high'. If no threat is detected, set this to 'none'.}
        """

    def generate_content(self):
        retries = 3

        while True:
            if retries == 0:
                raise Exception("Max retries exceeded. Unable to generate content.")
            
            try:
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-pro-latest",
                    generation_config=self.generation_config,
                    system_instruction=self.system_instruction,
                    safety_settings=self.safety_settings
                )

                input_img = PIL.Image.open(self.image_path)

                prompt = ""
                response = model.generate_content([prompt, input_img])
                extracted_json = extract_json_object(response.text)
                return extracted_json
            
            except Exception as e:
                retries -= 1
                print(f"Error generating content for retry count = {retries}: {str(e)}")
