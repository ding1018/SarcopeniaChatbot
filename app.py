from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 取自LINE Developers平台的CHANNEL_ACCESS_TOKEN和CHANNEL_SECRET
line_bot_api = LineBotApi('SWnTYljZDexfuVVILbVFZtYwSmwvETNtQ8VPThNLmW9lNNvBnEEoDDM39vLGx1eltiVqCumYtQyZvDE7HZd3X30Zob1Ec2puBXL+iPdq5mdbtfxKGq2GIMoqe5XIGRKeXi3uQ9YAHzp2BH5pdw+ACQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('9b2a0edc84246b578d1c1e9c37fe5896')

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取LINE傳送的簽名
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
    # 回應用戶的訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"收到您的測驗結果: {event.message.text}")
    )

if __name__ == "__main__":
    app.run(port=3000)
