def _build_text_prompt(team_color: str) -> str:
    with open("./deepfoot/prompt.txt", "r") as file:
        prompt = file.read()
    prompt = prompt.replace("{TEAM_COLOR}", team_color)
    return prompt


def get_prompt_messages(team_color: str, base64Frames: list):
    return [
        {
            "role": "user",
            "content": [
                _build_text_prompt(team_color=team_color),
                *map(lambda x: {"image": x, "resize": 768}, base64Frames[0::20]),
            ],
        },
    ]
