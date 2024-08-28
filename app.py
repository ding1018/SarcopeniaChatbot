from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction
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
    user_message = event.message.text

    if user_message == "醫師介紹":
        # 回應醫師介紹的按鈕模板訊息
        buttons_template = TemplateSendMessage(
            alt_text="醫師介紹",
            template=ButtonsTemplate(
                thumbnail_image_url="https://images.unsplash.com/photo-1597764690523-15bea4c581c9?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",  # 替換為你的圖片 URL
                image_aspect_ratio="rectangle",
                image_size="contain",
                image_background_color="#FFFFFF",
                title="醫師介紹",
                text="請選擇科別",
                actions=[
                    MessageAction(
                        label="復健科醫師",
                        text="復健科醫師"
                    ),
                    MessageAction(
                        label="骨科醫師",
                        text="骨科醫師"
                    ),
                    MessageAction(
                        label="高齡醫學科醫師",
                        text="高齡醫學科醫師"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
    else:
        # 回應用戶的測驗結果
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f"收到您的測驗結果: {user_message}")
        )

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
