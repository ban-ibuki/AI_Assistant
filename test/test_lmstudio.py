import requests

url = "http://localhost:1234/v1/chat/completions"

data = {
    "model": "qwen/qwen3.5-9b",
    "messages": [
        {
            "role": "user",
            "content": "こんにちは。自己紹介してください。"
        }
    ],
    "temperature": 0.7
}

response = requests.post(url, json=data)

print(response.json()["choices"][0]["message"]["content"])