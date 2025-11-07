import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# ---- 環境変数からキーを読む（絶対に直書きしない） ----
CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")

if not CHANNEL_ACCESS_TOKEN or notimport os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")

if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    raise RuntimeError("環境変数 LINE_CHANNEL_ACCESS_TOKEN / LINE_CHANNEL_SECRET が設定されていません。")

app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# ---- ヘルスチェック ----
@app.get("/")
def health():
    return "ok", 200

@app.get("/healthz")
def healthz():
    return "ok", 200

# ---- Webhook入口 ----
@app.post("/callback")
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

# ---- メッセージ応答 ----
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

# ---- RenderではPORTを使う ----
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
 CHANNEL_SECRET:
    # Render のログに出す用（起動失敗の原因が分かりやすくなる）
    raise RuntimeError("環境変数 LINE_CHANNEL_ACCESS_TOKEN / LINE_CHANNEL_SECRET が設定されていません。")

# ---- Flask & LINE SDK 初期化 ----
app = Flask(__name__)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# ---- ヘルスチェック（Renderの起動確認用）----
@app.get("/")
def health():
    return "ok", 200

# ---- Webhook 入口（LINE → あなたのサーバー）----
@app.post("/callback")
def callback():
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)  # 署名不一致

    return "OK"

# ---- メッセージを受け取ったらオウム返し ----
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=user_text)
    )

# ---- Render では PORT を環境変数から取得するのが超重要 ----
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
@app.get("/healthz")
def healthz():
    return "ok", 200
