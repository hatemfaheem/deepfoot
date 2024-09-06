from openai import OpenAI
import os
from dotenv import load_dotenv

from deepfoot.prompt import get_prompt_messages
from deepfoot.video_preprocessor import extract_video_frames

video_file = "data/Build_Up_001_030824170544.mp4"
team_color: str = "blue"


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


base64Frames = extract_video_frames(video_file=video_file)
prompt_messages = get_prompt_messages(team_color=team_color, base64Frames=base64Frames)
result = client.chat.completions.create(
    model="gpt-4o",
    messages=prompt_messages,
    max_tokens=500,
    response_format={"type": "json_object"},
)

print(result.choices[0].message.content)
