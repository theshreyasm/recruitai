# Import necessary modules
import aiohttp
import asyncio
import nest_asyncio
import time
import json
import os
import base64
from dotenv import load_dotenv
from PIL import Image

def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        img_data = img_file.read()
        base64_string = base64.b64encode(img_data).decode('utf-8')
        return base64_string

# Apply nest_asyncio
nest_asyncio.apply()

llava_endpoint = os.getenv("LLAVA_ENDPOINT")

async def fetch(session, url, data):
    async with session.post(url, data=data) as response:
        return await response.text()
    
async def analyze(response_count = 1):

    output_frame_folder = "video_frames"  # Change this to the output frame folder

    frame_count = 0
    good_frame = 0
    # Loop through all frames in the output_frames folder
    for filename in os.listdir(output_frame_folder):
        if filename.endswith(".jpg"):
            # Construct the full path to the frame
            frame_path = os.path.join(output_frame_folder, filename)
            frame_count += 1
            

        s = image_to_base64(frame_path)
        url = llava_endpoint
        data = json.dumps({
        "model": "llava:7b-v1.6-mistral-q5_K_M",
        "prompt": "if you had to categorize the emotion of this person as happy, sad, angry, fear, neutral or confident. what would it be? i need a precise one word answer",
        "stream": False,
        "images": [s]
        })
        headers = {'Content-Type': 'application/json'}

        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            
            for _ in range(response_count):
                task = asyncio.create_task(fetch(session, url, data))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

            data = json.loads(responses[0])
            print(data["response"])
            s = data["response"]

            if('happy' in s.lower() or 'confident' in s.lower()):
                good_frame += 1
            
            if('neutral' in s.lower()):
                good_frame += 0.5
    
    return good_frame/frame_count

