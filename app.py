from flask import Flask, request
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from const import bot_url, bot_token, persistent_menu_mode, camera_url, camera_url_end
import cv2


try:
    from Queue import Queue
except ImportError:
    from queue import Queue

app = Flask(__name__)
TOKEN = bot_token
SECRET = '/bot' + TOKEN
URL = bot_url

UPDATE_QUEUE = Queue()
BOT = telepot.Bot(TOKEN)
print("I'm here!")


def start_menu():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="First camera", callback_data='camera1'),
                InlineKeyboardButton(text="Second camera", callback_data='camera2'),
            ]
        ]
    )

    return "Hey there! Use the inline keyboard to navigate.", keyboard


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    template = start_menu()
    BOT.sendMessage(chat_id, text=template[0], reply_markup=template[1])


def get_channel_frame(channel):
    print("retrieving a frame from channel " + str(channel))
    video = cv2.VideoCapture(
        camera_url + str(channel) + camera_url_end
    )
    success, image = video.read()
    cv2.imwrite('frame' + str(channel) + '.jpg', image)


def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
    if persistent_menu_mode:
        message_identifier = telepot.origin_identifier(msg)
    if query_data == 'camera1':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="Second camera", callback_data='camera2'),
                    InlineKeyboardButton(text="Menu", callback_data='menu'),
                ]
            ]
        )
        if persistent_menu_mode:
            BOT.editMessageText(message_identifier, "First Camera", reply_markup=keyboard)
        else:
            get_channel_frame(1)
            BOT.sendPhoto(from_id, photo=open('frame1.jpg', 'rb'), caption="First Camera 1")
            get_channel_frame(2)
            BOT.sendPhoto(from_id, photo=open('frame2.jpg', 'rb'), caption="First Camera 2")
            BOT.sendMessage(from_id, "Showing first camera...", reply_markup=keyboard)
    if query_data == 'camera2':
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text="First camera", callback_data='camera1'),
                    InlineKeyboardButton(text="Menu", callback_data='menu'),
                ]
            ]
        )
        if persistent_menu_mode:
            BOT.editMessageText(message_identifier, "Second Camera", reply_markup=keyboard)
        else:
            get_channel_frame(3)
            BOT.sendPhoto(from_id, photo=open('frame3.jpg', 'rb'), caption="Second Camera 1")
            get_channel_frame(4)
            BOT.sendPhoto(from_id, photo=open('frame4.jpg', 'rb'), caption="Second Camera 2")
            BOT.sendMessage(from_id, "Showing second camera...", reply_markup=keyboard)
    if query_data == 'menu':
        template = start_menu()
        if persistent_menu_mode:
            BOT.editMessageText(message_identifier, template[0], reply_markup=template[1])
        else:
            BOT.sendMessage(from_id, template[0], reply_markup=template[1])


BOT.message_loop({'chat': on_chat_message, 'callback_query': on_callback_query}, source=UPDATE_QUEUE)


@app.route(SECRET, methods=['GET', 'POST'])
def pass_update():
    print("Webhook")
    UPDATE_QUEUE.put(request.data)
    return 'OK'
