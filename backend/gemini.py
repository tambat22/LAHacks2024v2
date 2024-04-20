import google.generativeai as genai
import PIL.Image
import os
from dotenv import load_dotenv
load_dotenv()

def img_to_text(image_path):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    # Set up the model
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 0,
        "max_output_tokens": 8192,
    }

    safety_settings = [
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

    system_instruction = """You are a visual speaker and identifier for a visually impaired user. 
    Describe what the input image is and return a response of a specific direction (ie: left, right, 
    straight, back) a visually impaired user should walk in to avoid obstacles, such as cars. 
    DO NOT give a list as a response. Give the instructions in a short paragraph. For example 
    \"This is a car, you should walk left around the car to the sidewalk to move forward 
    to your destination\". DO NOT use the words \"visually impaired person\". You should refer 
    to the person as \"you\". """

    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                generation_config=generation_config,
                                system_instruction=system_instruction,
                                safety_settings=safety_settings)

    input_img = PIL.Image.open(image_path)
    input_img

    prompt = ""
    response = model.generate_content([prompt, input_img])
    return response.text
    
if __name__ == '__main__':
    #TODO: FIGURE OUT WHY THIS IS DIFFERENT FROM BEFORE
    print(img_to_text('backend/test_imgs/road_img.jpeg'))

