import requests
import datetime
import schedule
import time

def log(content):
    with open('./plan_log','a') as f: 
        now = datetime.datetime.now()
        ts = now.strftime('[%Y-%m-%d %H:%M:%S]')
        print(ts + content, file=f)

def update():
    try:
        response = requests.get('http://49.235.232.28/update')
        log('update done')
    except:
        log('update failed')


def update_daily():
    try:
        response = requests.get('http://49.235.232.28/update_daily')
        log('update_daily done')
    except:
        log('update_daily failed')


def tasklist():
    schedule.every(10).minutes.do(update)
    schedule.every(1).day.at("23:00").do(update_daily)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


tasklist()
