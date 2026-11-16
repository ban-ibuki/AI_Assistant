import requests
import base64
from tkinter import filedialog, Tk


# ====================
# 画像選択
# ====================

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


# ====================
# ユーザー指示入力
# ====================

instruction = input(
    "\n画像をどのように変更しますか？\n> "
)


# ====================
# 画像をBase64化
# ====================

with open(image_path, "rb") as f:
    image_base64 = base64.b64encode(
        f.read()
    ).decode()


# ====================
# LM Studio(Qwen-VL)
# ====================

lm_url = "http://localhost:1234/v1/chat/completions"


messages = {
    "model": "qwen2.5-vl-7b-instruct",
    "messages": [
        {
            "role": "system",
            "content":
            """
あなたは商品ロゴ・イラスト編集専門AIです。

画像を分析し、Stable Diffusion用の英語プロンプトを作成してください。

条件:
- シンプルなデザインを優先
- ロゴ用途を考える
- 不要な細部を削除
- 太く明確な線
- ベクターイラスト風
- 小さいサイズでも認識可能
- 影や質感を避ける
"""
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text":
                    f"""
この画像を編集してください。

ユーザーの希望:
{instruction}

Stable Diffusion用の編集プロンプトだけを作成してください。
"""
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
    json=messages
)

result = response.json()

prompt = result["choices"][0]["message"]["content"]

print("\n生成プロンプト:")
print(prompt)


# ====================
# Stable Diffusion img2img
# ====================

sd_url = "http://127.0.0.1:7860/sdapi/v1/img2img"


sd_data = {
    "init_images": [
        image_base64
    ],

    "prompt":
        prompt +
        ", single line art, bold clean strokes, "
        "simple silhouette, flat vector logo, "
        "no gradients, no shadows",

    "negative_prompt":
        "realistic photo, 3d, shading, "
        "complex details, messy lines",

    "denoising_strength": 0.65,

    "steps": 25,

    "width": 512,

    "height": 512
}


sd_response = requests.post(
    sd_url,
    json=sd_data
)


sd_result = sd_response.json()


output = base64.b64decode(
    sd_result["images"][0]
)


with open(
    "chat_edit_result.png",
    "wb"
) as f:
    f.write(output)


print("\n完成: chat_edit_result.png")


# ====================
# 生成画像を表示
# ====================

from PIL import Image

img = Image.open(
    "chat_edit_result.png"
)

img.show()