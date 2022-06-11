import time
import cv2
import datetime
import telegram
import json

SECS_IN_30_MINS = 60 * 30


def take_picture(date_time: str):
    camera = cv2.VideoCapture(0)
    return_value, image = camera.read()
    filepath = 'output/' + date_time + '.png'
    cv2.imwrite(filepath, image)
    del camera
    return filepath


def get_date_time_str():
    return '{date:%Y-%m-%d--%H-%M-%S}'.format( date=datetime.datetime.now())


def read_configuration():
    with open('secrets.json') as config:
        dict_config = json.load(config)
        return dict_config


def send_telegram_pic(bot, config: dict, pic_file_path: str):
    bot.send_photo(chat_id=config['chat-id'], photo=open(pic_file_path, 'rb'))


def main():
    config: dict = read_configuration()
    bot = telegram.Bot(token=config['telegram-bot-token'])

    while True:
        this_date_time: str = get_date_time_str()
        pic_file_path = take_picture(this_date_time)
        send_telegram_pic(bot, config, pic_file_path)
        time.sleep(SECS_IN_30_MINS)


if __name__ == '__main__':
    main()
