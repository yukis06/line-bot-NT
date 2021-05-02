# based on a sample code in https://github.com/line/line-bot-sdk-python

import os
from dotenv import load_dotenv

from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

switch = 1

load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="元画像をアップしてね"))

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    if switch ==1:
        switch = -1*switch
        with open("static/content.jpg", "wb") as f:
            f.write(message_content.content)
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="スタイル画像をアップしてね")
            )
    elif switch == -1:
        switch = -1*switch
        with open("static/style.jpg", "wb") as f:
            f.write(message_content.content)
        
        content_img = "./static/content.jpg"
        style_img = "./static/style.jpg"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content_img+" + "+style_img)
            )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ["PORT"])