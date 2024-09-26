from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction
import os

app = Flask(__name__)

# 從環境變量中讀取 LINE Bot API 和 Webhook Handler 的 TOKEN 和 SECRET
line_bot_api = LineBotApi(os.getenv('LINE_CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

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

    # 當用戶回傳 "醫師介紹" 或測驗結果總分為 5 到 10 時，回傳醫師介紹的按鈕模板訊息
    if user_message == "醫師介紹" or user_message in [
        "我的肌少症測驗結果總分為: 5", 
        "我的肌少症測驗結果總分為: 6", 
        "我的肌少症測驗結果總分為: 7", 
        "我的肌少症測驗結果總分為: 8", 
        "我的肌少症測驗結果總分為: 9", 
        "我的肌少症測驗結果總分為: 10",
    ]:
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
    
    # 當用戶回傳測驗結果總分為 0 到 4 時，回傳運動處方的按鈕模板訊息
    elif user_message == "運動處方" or user_message in [
        "我的肌少症測驗結果總分為: 0",
        "我的肌少症測驗結果總分為: 1",
        "我的肌少症測驗結果總分為: 2",
        "我的肌少症測驗結果總分為: 3",
        "我的肌少症測驗結果總分為: 4"
    ]:
        buttons_template = TemplateSendMessage(
            alt_text="我要做運動",
            template=ButtonsTemplate(
                thumbnail_image_url="https://images.unsplash.com/photo-1522898467493-49726bf28798?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA==",
                title="我要做運動",
                text="請選擇運動類別",
                actions=[
                    MessageAction(
                        label="居家運動處方",
                        text="居家運動處方"
                    ),
                    MessageAction(
                        label="核心運動處方",
                        text="核心運動處方"
                    ),
                    MessageAction(
                        label="靜態延伸運動處方",
                        text="靜態延伸運動處方"
                    ),
                    MessageAction(
                        label="負重訓練運動處方",
                        text="負重訓練運動處方"
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
    
    # 用戶選擇按鈕選項後的處理
    elif user_message in ["復健科醫師", "骨科醫師", "高齡醫學科醫師", "居家運動處方", "核心運動處方", "靜態延伸運動處方", "負重訓練運動處方"]:
        # 這裡可以選擇不做任何回應或進行其他處理
        pass

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
