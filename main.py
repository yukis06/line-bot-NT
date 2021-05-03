# based on a sample code in https://github.com/line/line-bot-sdk-python

import os
from dotenv import load_dotenv
from pathlib import Path

from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage

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
    if os.path.exists(Path("static/content.jpg").absolute()):
        #img = Image.open(message_content.content)
        #img.save("./static/style.jpg")
        with open(Path("static/style.jpg").absolute(), "wb") as f:
            for chunk in message_content.iter_content():
                f.write(chunk)
        """
        transfer process
        """
        out_url = "static/content.jpg"
        
        #os.remove("static/content.jpg")
        os.remove(Path("static/style.jpg").absolute())
        app.logger.info(Path("https://genius-guy-bot.herokuapp.com/{main_image_path}").absolute())
        line_bot_api.reply_message(
            event.reply_token,
            ImageSendMessage(Path("https://genius-guy-bot.herokuapp.com/{out_url}").absolute(), Path("https://genius-guy-bot.herokuapp.com/{out_url}").absolute())
            )

    else:
        #img = Image.open(message_content.content)
        #img.save("./static/content.jpg")
        with open(Path("static/content.jpg").absolute(), "wb") as f:
            for chunk in message_content.iter_content():
                f.write(chunk)

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="スタイル画像をアップしてね")
            )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ["PORT"])