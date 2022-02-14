import time
import traceback

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4

from config import TIME_SLEEP, CHROMEDRIVER_PATH
from flask_app_init import db
from mail import send_mail
from models import Invoice

url = 'https://business.dme.ru/cargo/'


def driver_init():
    options = webdriver.ChromeOptions()
    # options.binary_location = "/usr/bin/chromium-browser"
    options.add_argument("--headless")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("start-maximized")
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(
        options=options,
        # executable_path=CHROMEDRIVER_PATH
    )
    # display = Display(visible=0, size=(640, 480))
    # display.start()
    return driver


def get_status(status_text: str, departure_time: str):
    if status_text == 'Комплектация на рейс/Груз принят к перевозке':
        if departure_time == ' ':
            return 1
        else:
            return 2
    elif status_text == 'Перевозка выполнена/-Перевозка выполнена-':
        return 3
    else:
        return 0


def get_result(driver: webdriver.Chrome, number: str):
    driver.get(url)
    driver.find_element(by=By.ID, value='NumberFirstPart').send_keys(number.split('-')[0])
    driver.find_element(by=By.ID, value='NumberSecondPart').send_keys(number.split('-')[1])
    driver.find_element(by=By.CLASS_NAME, value='w155').click()

    time.sleep(2)

    soup = bs4(driver.page_source, 'html.parser')
    table = soup.find('table', class_='table_style_3 table_style_cargo')
    params = table.find_all('td')

    to = params[1].text
    status = params[2].text
    departure_time = params[3].text
    place = params[5].text
    weight = params[6].text
    print(to, status, departure_time, place, weight)

    return to, status, departure_time, place, weight


def parse_all():
    invoices = Invoice.query.all()
    driver = driver_init()
    exc = 0

    for invoice in invoices:
        time.sleep(20)
        exc = 0
        while exc < 2:
            print(invoice.number, flush=True)
            try:
                to, status, departure_time, place, weight = get_result(driver, invoice.number)
                status = get_status(status, departure_time)

                print(to, status, departure_time, place, weight, flush=True)

                if invoice.status == status:
                    break

                for i in range(len(invoice.email.split(' '))):
                    send_mail(
                        [invoice.email.split(' ')[i]],
                        status,
                        (invoice.place.split(' ')[i], invoice.weight.split(' ')[i], to)
                    )

                if status == 3:
                    db.session.delete(invoice)
                else:
                    invoice.status = status

                db.session.commit()
            except Exception as e:
                print(traceback.format_exc(), flush=True)

                exc += 1
                time.sleep(6)
            else:
                exc = 0
                break

    driver.close()
    # display.stop()


def parse_cycle():
    while True:
        parse_all()
        time.sleep(TIME_SLEEP)
