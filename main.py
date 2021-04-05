#!/usr/bin/env python3
import configparser
import datetime
import requests
import urllib
import pprint
from bs4 import BeautifulSoup
import logging
import time
import random

logging.basicConfig(filename='alerting.log', filemode='w',
                    format='%(asctime)s %(process)d %(module)s:%(funcName)s %(levelname)s: %(message)s',
                    level=logging.INFO)


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
    send_ids = config.get('BASE', 'telegram_id').split(', ')
    for id in send_ids:
        logging.debug("Trying to send to: %s", id)
        URL = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=markdown'.format(
            config.get('BASE', 'telegram_webhook'),
            id,
            urllib.parse.quote_plus(message))
        if config.get('BASE', 'DEBUG') == 'true': pp.pprint(URL)
        r = requests.get(url=URL)
        data = r.json()

        if config.get('BASE', 'DEBUG') == 'true': pp.pprint(data)

        if not data['ok']:
            logging.error('Sending message failed, check config')
            print("Sending message failed, check config")
        time.sleep(2)

    return True


def scrape_supernt(url):
    pp = pprint.PrettyPrinter(indent=4)
    articles = config.get('BASE', 'articles').split(', ')

    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 '
        'Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 '
        'Safari/537.36 Edg/89.0.774.68',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 '
        'Safari/537.36 OPR/75.0.3969.149',
        'Mozilla/5.0 (Linux; Android 7.1.2; DSCS9 Build/NHG47L; wv) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Version/4.0 Chrome/80.0.3987.149 Safari/537.36 '
    ]
    headers = {
        'User-Agent': random.choice(agents)
    }

    try:
        r = requests.get(url, headers=headers)
    except Exception as e:
        logging.error("Failed to load shop website: %s", e)
        return 0

    soup = BeautifulSoup(r.text, features="html.parser")
    for article in articles:
        if soup.find(text=article).parent.parent.find(text="out of stock"):
            logging.debug('%s is out of stock', article)
        else:
            logging.info('%s is available!', article)
            articles.remove(article)
            str_articles = ', '.join(articles)
            if config.get('BASE', 'DEBUG') == 'true': pp.pprint(str_articles)
            config.set('BASE', 'articles', str_articles)
            with open('config.ini', 'w') as configfile:
                config.write(configfile)
            send_telegram("*SuperNT ALERT*\n" \
                          "{} is available!\n" \
                          "[Analogue Shop](https://www.analogue.co/store#super-nt)".format(article))
            return 0


if __name__ == '__main__':
    logging.info('Starting script...')
    scrape_supernt('https://www.analogue.co/store')
    while 1:
        now = datetime.datetime.now()
        if now.hour == 23 and now.minute == 5 and now.second == 0 and now.microsecond < 1000 and now.day % 7 == 0:
            logging.info("Heartbeat: it is: %s", now.strftime("%d/%m/%Y %H:%M:%S"))
        if now.minute % int(config.get('BASE', 'time')) == 0:
            if config.get('BASE', 'DEBUG') == 'true': print('shoot')
            scrape_supernt('https://www.analogue.co/store')
            time.sleep(60)
