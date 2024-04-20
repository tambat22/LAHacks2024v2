import google.generativeai as genai
import PIL.Image
import os

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
            Given the attached image, analyze the contents and generate a detailed description suitable for a visually impaired person. Identify any potential dangers or threats in the image. Provide the response in JSON format with the following fields:
            1. 'description': A detailed text description of the image.
            2. 'danger_detected': A boolean indicating whether any potential danger or threat is present in the image.
            3. 'threat_level': A string that rates the level of any detected threat as 'low', 'mid', or 'high'. If no threat is detected, set this to 'none'.

            Ensure the description is clear and comprehensive enough to convey the scene accurately to someone visually impaired who cannot see the image.
            """

    def generate_content(self):
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            generation_config=self.generation_config,
            system_instruction=self.system_instruction,
            safety_settings=self.safety_settings
        )

        input_img = PIL.Image.open(self.image_path)

        prompt = ""
        response = model.generate_content([prompt, input_img])
        return response.text