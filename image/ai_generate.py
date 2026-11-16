import time
import requests
import json
import base64
import os

# ================= 配置設定 =================
LM_STUDIO_URL = "http://localhost:1234/v1"
SD_WEBUI_URL = "http://127.0.0"
# 画像を保存するフォルダ（デスクトップに保存されます）
SAVE_FOLDER = os.path.join(os.path.expanduser("~"), "Desktop")
# ============================================

def get_current_model():
    try:
        res = requests.get(f"{LM_STUDIO_URL}/models").json()
        return res['data'][0]['id']
    except:
        return "google/gemma-4-e4b"

def get_last_chat_message(model_name):
    # LM Studioのチャット履歴（履歴エンドポイント）から最新のメッセージを取得
    try:
        res = requests.get(f"{LM_STUDIO_URL}/chat/history").json()
        # 最新の会話ログを解析
        if 'messages' in res and len(res['messages']) > 0:
            last_msg = res['messages'][-1]
            # AI（assistant）が喋った最新の英語タグを抽出
            if last_msg['role'] == 'assistant':
                return last_msg['content']
    except Exception as e:
        pass
    return None

def send_to_stable_diffusion(prompt):
    print(f"\n[🎨 SD送信] 以下のプロンプトで画像を生成します:\n{prompt}")
    payload = {
        "prompt": prompt,
        "steps": 25,
        "width": 512,
        "height": 512,
        "cfg_scale": 7
    }
    try:
        response = requests.post(SD_WEBUI_URL, json=payload)
        r = response.json()
        
        # 返ってきた画像データをデコードして保存
        for i, img_data in enumerate(r['images']):
            image = base64.b64decode(img_data.split(",", 1)[0])
            filename = f"lm_sd_{int(time.time())}_{i}.png"
            filepath = os.path.join(SAVE_FOLDER, filename)
            with open(filepath, 'wb') as f:
                f.write(image)
            print(f"🎉 画像を保存しました: {filepath}")
    except Exception as e:
        print(f"❌ Stable Diffusionへの送信に失敗しました: {e}")

def main():
    model_name = get_current_model()
    print(f"🤖 LM Studio 監視システム起動完了 (使用モデル: {model_name})")
    print("LM Studioの『Chat』画面でGemmaにプロンプトを作らせると、自動で画像が生成されます。")
    print("※終了するには Ctrl + C を押してください。\n")
    
    last_seen_prompt = ""
    
    while True:
        current_prompt = get_last_chat_message(model_name)
        if current_prompt and current_prompt != last_seen_prompt:
            # 新しいプロンプトが生成されたら自動実行
            send_to_stable_diffusion(current_prompt)
            last_seen_prompt = current_prompt
        
        time.sleep(2) # 2秒ごとにLM Studioのチャット画面をパトロール

if __name__ == "__main__":
    main()
