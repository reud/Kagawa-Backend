import os

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    LocationMessage)

from network.state import check_server_data, ServerData, update_value, create_value

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_TOKEN_SECRET'))


@app.route("/")
def hello_world():
    return "hello world!"


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    state = check_server_data(event.source.user_id)
    print(f'state: {state}')
    ret = ''
    if state == ServerData.ERROR:
        ValueError('unexpected valued got')
    elif state == ServerData.USER_ID_AND_LOCATION:
        message = event.message.text
        update_value(event.source.user_id, {'comment': {'value': message}})
        ret = 'ありがとうございます。登録完了です！\n他にもオススメな場所があったら、位置情報を送信してくださいね！⭐'
    elif state == ServerData.EMPTY:
        ret = '先に、良いな！と思った香川のお店や場所を位置情報が欲しいな！'
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ret))


@handler.add(MessageEvent, message=LocationMessage)
def handle_location(event):
    state = check_server_data(event.source.user_id)
    print(f'state: {state}')
    ret = ''
    if event.message.title == '':
        ret = '名前のついた場所を指定してください⭐️'
        print(event.message.title)
    elif state == ServerData.ERROR:
        ValueError('unexpected valued got')
    elif state == ServerData.USER_ID_AND_LOCATION:
        ret = '先に1つ前の場所の感想が欲しいな！'
    elif state == ServerData.EMPTY:
        ret = '位置情報の送信ありがとうございます！⭐️ \n最後に、そのスポットの感想を送ってみましょう！！'
        create_value({'user_id': {'value': event.source.user_id}, 'location': {'value': event.message.title}})

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text=ret))


if __name__ == "__main__":
    app.run()
