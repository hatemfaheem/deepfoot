import cv2  # We're using OpenCV to read video, to install !pip install opencv-python
import base64
from openai import OpenAI
import os
from dotenv import load_dotenv

video_file = "data/Build_Up_001_030824170544.mp4"
team_color: str = 'blue'


# Load environment variables from .env file
load_dotenv()


client = OpenAI(
    api_key=os.environ.get(
        "OPENAI_API_KEY", "<your OpenAI API key if not set as env var>"
    ),
    organization=os.environ.get(
        "OPENAI_ORGANIZATION", "<your OpenAI API Organization if not set as env var>"
    ),
)

video = cv2.VideoCapture(video_file)

base64Frames = []
while video.isOpened():
    success, frame = video.read()
    if not success:
        break
    _, buffer = cv2.imencode(".jpg", frame)
    base64Frames.append(base64.b64encode(buffer).decode("utf-8"))

video.release()
print(len(base64Frames), "frames read.")

PROMPT_MESSAGES = [
    {
        "role": "user",
        "content": [
            f"These are frames from a video that I want to upload. This is a snippet from a football match, focusing only on analyzing the {team_color} team. I'm trying to analyze whether the team is doing build up or high pressure. Reply with just a json file that has 2 keys build_up and high_pressure and each has a value between 0.0 and 1.0 that represents your confidence.",
            *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::50]),
        ],
    },
]
params = {
    "model": "gpt-4o",
    "messages": PROMPT_MESSAGES,
    "max_tokens": 200,
}

result = client.chat.completions.create(**params)
print(result.choices[0].message.content)
