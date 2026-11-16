import requests
import subprocess

lm_url = "http://localhost:1234/v1/chat/completions"

messages = [
    {
        "role": "system",
        "content": """
あなたは画像制作アシスタントAIです。
ロゴ、イラスト、キャラクターデザインを手伝います。

ユーザーが画像生成を希望したら画像生成モード、
画像編集を希望したら画像編集モード、
それ以外は普通に会話してください。
"""
    }
]

print("AIチャット開始")
print("終了する場合は exit と入力してください\n")

while True:

    user_input = input("あなた: ")

    if user_input.lower() == "exit":
        break

    # =====================
    # 画像生成
    # =====================
    if ("画像" in user_input or "イラスト" in user_input or "ロゴ" in user_input) and \
       ("作" in user_input or "生成" in user_input):

        print("\n画像生成モードを起動します...\n")

        subprocess.run(
            [
                "python",
                "../image/ai_generate.py",
                user_input
            ]
        )

        continue

    # =====================
    # 画像編集
    # =====================
    if ("編集" in user_input or
        "修正" in user_input or
        "変更" in user_input):

        print("\n画像編集モードを起動します...\n")

        subprocess.run(
            [
                "python",
                "../image/ai_image_chat_editor.py",
                user_input
            ]
        )

        continue

    # =====================
    # 通常チャット
    # =====================

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = requests.post(
        lm_url,
        json={
            "model": "qwen2.5-vl-7b-instruct",
            "messages": messages
        }
    )

    result = response.json()

    answer = result["choices"][0]["message"]["content"]

    print("\nAI:")
    print(answer)
    print()

    messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )