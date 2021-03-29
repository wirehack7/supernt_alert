#!/usr/bin/env python3
import configparser
import datetime
import requests
import urllib
import pprint
from bs4 import BeautifulSoup
import logging

logging.basicConfig(filename='alerting.log', filemode='w',
                    format='%(asctime)s %(process)d %(module)s:%(funcName)s %(levelname)s: %(message)s',
                    level=logging.DEBUG)


# TODO: add better check
def check_cfg():
    config = configparser.ConfigParser()
    config.read('config.ini')
    try:
        config.get('BASE', 'telegram_webhook')
        config.get('BASE', 'telegram_id')
    except:
        logging.error('No telegram settings')
        exit('Telegram settings not set')
    else:
        if not config.get('BASE', 'telegram_webhook') or not config.get('BASE', 'telegram_id'):
            logging.error('No telegram settings')
            exit("Telegram settings not set")
        elif not config.get('BASE', 'articles') or config.get('BASE', 'articles') == '':
            logging.error('no articles set')
            exit("Set articles to alert")
        else:
            logging.info('Config successfully read')
            return config


config = check_cfg()


def send_telegram(message):
    pp = pprint.PrettyPrinter(indent=4)
    URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=markdown'.format(
        config.get('BASE', 'telegram_webhook'),
        config.get('BASE', 'telegram_id'),
        urllib.parse.quote_plus(message))
    if config.get('BASE', 'DEBUG') == 'true': pp.pprint(URL)
    r = requests.get(url=URL)
    data = r.json()

    if config.get('BASE', 'DEBUG') == 'true': pp.pprint(data)

    if not data['ok']:
        exit("Sending message failed, check config")
    else:
        return data


def scrape_supernt(url, dom_element, text):
    pp = pprint.PrettyPrinter(indent=4)
    articles = config.get('BASE', 'articles').split(', ')

    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    for article in articles:
        if soup.find(text=article).parent.parent.find(text="out of stock"):
            logging.debug('%s is out of stock', article)
        else:
            logging.info('%s is available!', article)
            send_telegram("*SuperNT ALERT*\n" \
                          "{} is available!\n" \
                          "[Analogue Shop](https://www.analogue.co/store#super-nt)".format(article))


if __name__ == '__main__':
    logging.info('Starting script...')
    scrape_supernt('https://www.analogue.co/store', '', '')
    while 1:
        now = datetime.datetime.now()
        if now.minute % int(config.get('BASE', 'time')) == 0:
            scrape_supernt('https://www.analogue.co/store', '', '')
