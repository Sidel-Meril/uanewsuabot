#! /usr/bin/env python
# -*- coding: utf-8 -*-


import requests
from lxml import html
from datetime import datetime
import re

def get_source(source_link, save = True):
    r = requests.get(source_link.replace('https://t.me/','https://t.me/s/'))
    source = html.fromstring(r.text)
    if save is True: file=open('test.html', 'w', encoding='utf-8').write(r.text)
    return source

def parse_messages(source_link, sec_interval = 30):
    convert_date = lambda date: datetime.fromisoformat(date).timestamp()

    messages=[]
    print(datetime.now().isoformat())
    last_update = datetime.now().timestamp() - sec_interval
    _messages = get_source(source_link, save=False).xpath(".//div[@class='tgme_widget_message_bubble']")

    for message in _messages:
        _time = message.xpath("./div[@class='tgme_widget_message_footer compact js-message_footer']"
                              "/div[@class='tgme_widget_message_info short js-message_info']"
                              "/span[@class='tgme_widget_message_meta']"
                              "/a[@class='tgme_widget_message_date']/time/@datetime")[0]
        if convert_date(_time) > last_update:
            _link = message.xpath("./div[@class='tgme_widget_message_footer compact js-message_footer']"
                                  "/div[@class='tgme_widget_message_info short js-message_info']"
                                  "/span[@class='tgme_widget_message_meta']"
                                  "/a[@class='tgme_widget_message_date']/@href")[0]
            try:
                _text = html.tostring(message.xpath("./div[@class='tgme_widget_message_text js-message_text']")[0],
                                      encoding='utf-8').decode('utf8').replace('<br>', '\n')
                _text = re.sub(r'<.*?>', '', _text)
            except IndexError:
                _text = ''
            _message = {'channel': source_link, 'id': _link, 'date': datetime.fromisoformat(_time).timestamp(),
                    'text': _text,
                    'media': {'photo': None, 'file': None, 'audio': None, 'video': None}}
            messages.append(_message)
    return messages

def compare_time(last_update):
    _now = datetime.now().timestamp()
    try:
        _for_compare = datetime.fromisoformat(last_update).timestamp()
    except ValueError:
        _for_compare = 0
    if _now - _for_compare > 30:
        return True
    else:
        return False




def main():
    update_messages()

if __name__=='__main__':
    # main()
    pass
