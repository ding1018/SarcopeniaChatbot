from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 從環境變量中讀取 LINE Bot API 和 Webhook Handler 的 TOKEN 和 SECRET
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 LINE 傳送的簽名
    signature = request.headers['X-Line-Signature']

    # 獲取請求體
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 驗證簽名
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回應用戶的消息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"收到您的測驗結果: {event.message.text}")
    )

if __name__ == "__main__":
    app.run(port=3000)
