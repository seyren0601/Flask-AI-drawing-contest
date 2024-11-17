from openai import OpenAI
import dotenv
import os
import json
import string

dotenv.load_dotenv()

BEARER_TOKEN = os.environ['OPENAI_KEY']
PROJECT_ID = os.environ['OPENAI_PROJECT_ID']
ORGANIZATION_ID = os.environ['OPENAI_ORGANIZATION_ID']
client = OpenAI(
  organization=ORGANIZATION_ID,
  project=PROJECT_ID,
  api_key=BEARER_TOKEN
)

MODEL = "dall-e-2"
SIZE = "512x512"
QUALITY="standard"

def image_generate(prompt):
    response = client.images.generate(
        model=MODEL,
        prompt=prompt,
        size=SIZE,
        # quality=QUALITY,
        response_format='b64_json'
    )
    
    return response.data[0].b64_json