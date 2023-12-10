import json
import requests
from json import JSONDecodeError


def prompt(input_message):
    url = "https://ai.fakeopen.com/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "authorization": "Bearer pk-this-is-a-real-free-pool-token-for-everyone",
        "Origin": "https://chat.geekgpt.org",
        "Referrer": "https://chat.geekgpt.org/"
    }
    payload = {
        "frequency_penalty": 0,
        "messages": [
            {
                "content": input_message,
                "role": "user"
            }
        ],
        "model": "gpt-3.5-turbo",
        "presence_penalty": 0,
        "stream": True,
        "temperature": 1,
        "top_p": 1
    }
    payload_json = json.dumps(payload)
    response = requests.post(url, headers=headers,
                             data=payload_json, stream=True)

    if response.status_code == 200:
        content_lines = []
        for line in response.iter_lines():
            line_str = line.decode('utf-8')
            if "data:" not in line_str:
                continue
            json_str = line_str.split("data: ")[1]
            try:
                data_dict = json.loads(json_str)
                content = data_dict['choices'][0]['delta'].get('content', None)
                if content is not None:
                    content_lines.append(content)
            except JSONDecodeError as e:
                pass
        return ''.join(content_lines)

    elif response.status_code == 401 or response.status_code == 429:
        print(f"Error: {response.status_code}, Trying again.")
        response = prompt(input_message)
    else:
        return (f"Error: {response.status_code}, {response.text}")