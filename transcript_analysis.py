# Import necessary modules
import aiohttp
import asyncio
import nest_asyncio
import time
import json

# Apply nest_asyncio
nest_asyncio.apply()

async def fetch(session, url, data):
    async with session.post(url, data=data) as response:
        return await response.text()

async def analyze(qualification, skills, experience, response_count = 1, result = []):

    with open('transcripts/transcript.txt', 'r') as file:
        s = file.read()
    
    s += "This is the transcript of a candidate that applied to our organization."

    prompts = [f"This is the minimum qualification required for the candidate - {qualification}. Does the candidate possess this qualification? Say yes if it explicitly mentioned that the candidate has either completed this qualification or a higher qualification, else say no. For reference, PhD > Masters > Bachelors > Undergraduate.",
               f"These are the skills we require - {skills}. If the candidate has explicitly mentioned these skills, say yes. If even one skill is not explicitly mentioned, say no.",
               f"This is the minimum work experience we expect - {experience}. Does the candidate have atleast these many years of experience?Say yes, if it explicitly says that the candidate's experience is equal to or more than the minimum experience, else say no."]
    
    for prompt in prompts:
        
        url = "http://8.12.5.48:11434/api/generate"
        data = json.dumps({
        "model": "llava:7b-v1.6-mistral-q5_K_M",
        "prompt": s + prompt,
        "stream": False,
        "images": []
        })

        headers = {'Content-Type': 'application/json'}

        async with aiohttp.ClientSession(headers=headers) as session:
            tasks = []
            
            for _ in range(response_count):
                task = asyncio.create_task(fetch(session, url, data))
                tasks.append(task)

            responses = await asyncio.gather(*tasks)

            # print(responses[0])
            
            data = json.loads(responses[0])
            str = data["response"]

            print(str)

            if('yes' in str.lower()):
                result.append(1)
            else:
                result.append(0)
    
    return result

