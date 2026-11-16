import requests
import base64
from PIL import Image
from tkinter import filedialog, Tk

# --------------------
# 画像選択
# --------------------

root = Tk()
root.withdraw()

image_path = filedialog.askopenfilename(
    filetypes=[
        ("Image files", "*.png *.jpg *.jpeg *.webp")
    ]
)

if not image_path:
    print("画像が選択されませんでした")
    exit()

print("画像:", image_path)


# --------------------
# LM Studio (Qwen-VL)
# --------------------

lm_url = "http://localhost:1234/v1/chat/completions"

with open(image_path, "rb") as f:
    image_base64 = base64.b64encode(f.read()).decode()


message = {
    "model": "qwen2.5-vl-7b-instruct",
    "messages": [
        {
            "role": "system",
            "content":
    		"あなたは商品ロゴとアイコンデザイン専門のAIです。"
   		 "画像を分析し、Stable Diffusionで編集するための"
   		 "具体的なプロンプトを作成してください。"
   		 "シンプル化を優先してください。"
  		 "不要な細部を削除してください。"
    		 "小さいサイズでも認識できる形にしてください。"
    		 "太く明確な輪郭を使用してください。"
   		 "ベクターロゴ風のデザインにしてください。"
    		 "印刷物や商品ラベルに適したデザインを目指してください。"
    		 "リアルな描写ではなく、洗練されたミニマルデザインにしてください。"        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text":
                    "この画像を分析し、より良いロゴ・イラストに編集するための"
                    "英語プロンプトを作成してください。"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url":
                        f"data:image/png;base64,{image_base64}"
                    }
                }
            ]
        }
    ]
}


response = requests.post(
    lm_url,
    json=message
)

result = response.json()

prompt = result["choices"][0]["message"]["content"]

print("\n生成プロンプト:")
print(prompt)


# --------------------
# Stable Diffusion img2img
# --------------------

sd_url = "http://127.0.0.1:7860/sdapi/v1/img2img"


with open(image_path, "rb") as f:
    img = base64.b64encode(f.read()).decode()


prompt = prompt + ", single continuous line style, bold vector shape, high contrast, simple silhouette, recognizable as a rose even in black and white, no shading, no texture, professional logo design"

sd_data = {
    "init_images": [
        img
    ],
    "prompt": prompt,
    "denoising_strength": 0.25,
    "steps": 25,
    "width": 512,
    "height": 512
}

sd_response = requests.post(
    sd_url,
    json=sd_data
)

print("HTTP Status:", sd_response.status_code)

sd_result = sd_response.json()
print(sd_result)

output = base64.b64decode(
    sd_result["images"][0]
)

with open(
    "edited_result.png",
    "wb"
) as f:
    f.write(output)

print(sd_result)


print("\n編集完了: edited_result.png")