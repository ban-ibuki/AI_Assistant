import requests
import base64

url = "http://127.0.0.1:7860/sdapi/v1/txt2img"

data = {
    "prompt": "A beautiful pink rose logo, minimalist design, black outline, white background",
    "negative_prompt": "low quality, blurry",
    "steps": 20,
    "width": 512,
    "height": 512
}

response = requests.post(url, json=data)

result = response.json()

image_data = result["images"][0]

image = base64.b64decode(image_data)

with open("rose_test.png", "wb") as f:
    f.write(image)

print("画像生成完了")